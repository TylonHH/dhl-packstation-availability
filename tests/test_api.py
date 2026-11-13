"""Small regression check for live compartment parsing."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1] / "custom_components" / "dhl_packstation_availability"
sys.modules["aiohttp"] = types.SimpleNamespace(ClientError=Exception)
package = types.ModuleType("packstation_test")
package.__path__ = [str(ROOT)]
sys.modules[package.__name__] = package
for name in ("const", "api"):
    spec = importlib.util.spec_from_file_location(f"packstation_test.{name}", ROOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

from packstation_test.api import PackstationError, build_station_id, parse_station  # noqa: E402


class ParseStationTest(unittest.TestCase):
    def test_station_ids_are_independent_and_postal_zero_is_removed(self):
        self.assertEqual(build_station_id("23611", "202"), "1-23611202")
        self.assertEqual(build_station_id("01067", "103"), "1-1067103")
        self.assertEqual(build_station_id("01067", "240"), "1-1067240")
        self.assertNotEqual(build_station_id("01067", "103"), build_station_id("01067", "240"))

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

    def test_rejects_wrong_station_and_missing_live_data(self):
        for payload in ({"primaryKeyPF": "other", "locationType": "PACKSTATION", "liveStatus": {"freeCompartmentsS": 1}},
                        {"primaryKeyPF": "1-23611202", "locationType": "PACKSTATION"}):
            with self.subTest(payload=payload), self.assertRaises(PackstationError):
                parse_station(payload, "1-23611202")


if __name__ == "__main__":
    unittest.main()
