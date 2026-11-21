"""Small regression check for live compartment parsing."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock


class ClientError(Exception):
    pass


ROOT = Path(__file__).parents[1] / "custom_components" / "dhl_packstation_availability"
sys.modules["aiohttp"] = types.SimpleNamespace(ClientError=ClientError)
package = types.ModuleType("packstation_test")
package.__path__ = [str(ROOT)]
sys.modules[package.__name__] = package
for name in ("const", "api"):
    spec = importlib.util.spec_from_file_location(f"packstation_test.{name}", ROOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

from packstation_test.api import (  # noqa: E402
    PackstationError,
    StationNotFoundError,
    build_station_id,
    fetch_station,
    parse_station,
)


class FetchStationTest(unittest.IsolatedAsyncioTestCase):
    async def test_no_content_and_not_found_raise_station_not_found(self):
        for status in (204, 404):
            with self.subTest(status=status):
                session = MagicMock()
                session.get.return_value.__aenter__.return_value.status = status
                with self.assertRaises(StationNotFoundError):
                    await fetch_station(session, "1-23611202")


class ParseStationTest(unittest.TestCase):
    def test_station_ids_are_independent_and_postal_zero_is_removed(self):
        self.assertEqual(build_station_id("23611", "202"), "1-23611202")
        self.assertEqual(build_station_id("01067", "103"), "1-1067103")
        self.assertEqual(build_station_id("01067", "240"), "1-1067240")
        self.assertNotEqual(build_station_id("01067", "103"), build_station_id("01067", "240"))

    def test_deinfach_has_its_own_prefix(self):
        self.assertEqual(build_station_id("12345", "101", "DEIN_FACH"), "13-12345101")
        self.assertEqual(build_station_id("01067", "003", "PACKSTATION"), "1-1067003")

    def test_unsupported_location_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            build_station_id("12345", "101", "POSTFILIALE")

    def test_invalid_postal_code_or_station_number(self):
        for postal_code, number in (("1067", "103"), ("01067", "10"), ("01A67", "103")):
            with self.subTest(postal_code=postal_code, number=number), self.assertRaises(ValueError):
                build_station_id(postal_code, number)

    def test_zero_and_missing_are_distinct(self):
        station = parse_station({
            "primaryKeyPF": "1-23611202", "locationType": "PACKSTATION",
            "liveStatus": {"freeCompartmentsS": 0, "freeCompartmentsM": 2,
                           "sourceTimestamp": "2026-11-13T11:58:03+0100"},
        }, "1-23611202")
        self.assertEqual(station["counts"], {"s": 0, "m": 2, "l": None, "xl": None})
        self.assertIsNotNone(station["updated"])

    def test_deinfach_uses_the_same_counts_and_timestamp(self):
        payload = {
            "primaryKeyPF": "13-12345101", "locationType": "DEIN_FACH",
            "liveStatus": {"freeCompartmentsS": 0, "freeCompartmentsM": 2,
                           "freeCompartmentsL": 3, "freeCompartmentsXl": 4,
                           "sourceTimestamp": "2026-11-13T11:58:03+0100"},
        }
        station = parse_station(payload, "13-12345101")
        self.assertEqual(station["location_type"], "DEIN_FACH")
        self.assertEqual(station["counts"], {"s": 0, "m": 2, "l": 3, "xl": 4})
        self.assertEqual(station["updated"].isoformat(), "2026-11-13T11:58:03+01:00")
        with self.assertRaises(PackstationError):
            parse_station(payload, "1-12345101")

    def test_rejects_unsupported_location_type(self):
        with self.assertRaises(PackstationError):
            parse_station({
                "primaryKeyPF": "1-23611202", "locationType": "POSTFILIALE",
                "liveStatus": {"freeCompartmentsS": 1},
            }, "1-23611202")

    def test_rejects_key_prefix_that_does_not_match_location_type(self):
        for key, location_type in (("1-12345101", "DEIN_FACH"), ("13-12345101", "PACKSTATION")):
            with self.subTest(key=key, location_type=location_type), self.assertRaises(PackstationError):
                parse_station({
                    "primaryKeyPF": key, "locationType": location_type,
                    "liveStatus": {"freeCompartmentsS": 1},
                }, key)

    def test_rejects_wrong_station_and_missing_live_data(self):
        for payload in ({"primaryKeyPF": "other", "locationType": "PACKSTATION", "liveStatus": {"freeCompartmentsS": 1}},
                        {"primaryKeyPF": "1-23611202", "locationType": "PACKSTATION"}):
            with self.subTest(payload=payload), self.assertRaises(PackstationError):
                parse_station(payload, "1-23611202")


if __name__ == "__main__":
    unittest.main()
