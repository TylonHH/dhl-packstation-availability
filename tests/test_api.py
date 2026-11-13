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

from packstation_test.api import PackstationError, parse_station  # noqa: E402


class ParseStationTest(unittest.TestCase):
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
