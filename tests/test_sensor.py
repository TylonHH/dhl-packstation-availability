"""Check numeric sensor metadata without a running Home Assistant instance."""

import importlib.util
import sys
import types
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from test_api import ROOT


class SensorEntity:
    @property
    def state_class(self):
        return self._attr_state_class

    @property
    def suggested_display_precision(self):
        return self._attr_suggested_display_precision


class CoordinatorEntity:
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def available(self):
        return self.coordinator.last_update_success


sensor_base = types.ModuleType("homeassistant.components.sensor")
sensor_base.SensorEntity = SensorEntity
sensor_base.SensorStateClass = types.SimpleNamespace(MEASUREMENT="measurement")
entity_base = types.ModuleType("homeassistant.helpers.entity")
entity_base.DeviceInfo = dict
coordinator_base = types.ModuleType("homeassistant.helpers.update_coordinator")
coordinator_base.CoordinatorEntity = CoordinatorEntity
spec = importlib.util.spec_from_file_location("packstation_test.sensor", ROOT / "sensor.py")
sensor_module = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {module.__name__: module
                             for module in (sensor_base, entity_base, coordinator_base)}):
    spec.loader.exec_module(sensor_module)


class SensorTest(unittest.TestCase):
    def setUp(self):
        self.coordinator = types.SimpleNamespace(
            data={"name": "Example", "counts": {"s": 0, "m": 2, "l": 3, "xl": 1}},
            last_update_success=True,
        )

    def test_all_five_counts_are_measurements_with_integer_display(self):
        for size, value in (("s", 0), ("m", 2), ("l", 3), ("xl", 1), ("total", 6)):
            with self.subTest(size=size):
                sensor = sensor_module.PackstationSensor(self.coordinator, "1-23611202", size)
                self.assertEqual(sensor.state_class, "measurement")
                self.assertEqual(sensor.suggested_display_precision, 0)
                self.assertIs(type(sensor.native_value), int)
                self.assertEqual(sensor.native_value, value)
                self.assertTrue(sensor.available)
                self.assertEqual(sensor._attr_unique_id, f"1-23611202_{size}")
                self.assertEqual(sensor._attr_device_info["configuration_url"],
                                 "https://www.dhl.de/de/privatkunden/dhl-standorte-finden.html?primaryKeyPF=1-23611202")

    def test_each_station_has_its_own_public_link(self):
        for station_id in ("1-23611202", "1-1067103", "1-1067240"):
            with self.subTest(station_id=station_id):
                sensor = sensor_module.PackstationSensor(self.coordinator, station_id, "total")
                url = urlsplit(sensor._attr_device_info["configuration_url"])
                self.assertEqual((url.scheme, url.netloc, url.path),
                                 ("https", "www.dhl.de", "/de/privatkunden/dhl-standorte-finden.html"))
                self.assertEqual(parse_qs(url.query), {"primaryKeyPF": [station_id]})

    def test_missing_counts_and_update_failures_remain_unavailable(self):
        self.coordinator.data["counts"]["s"] = None
        for size in ("s", "total"):
            sensor = sensor_module.PackstationSensor(self.coordinator, "1-23611202", size)
            self.assertIsNone(sensor.native_value)
            self.assertFalse(sensor.available)
        self.coordinator.last_update_success = False
        sensor = sensor_module.PackstationSensor(self.coordinator, "1-23611202", "m")
        self.assertFalse(sensor.available)
