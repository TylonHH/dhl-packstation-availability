"""Exercise the config flow without a running Home Assistant instance."""

import importlib.util
import json
import sys
import types
import unittest
from unittest.mock import AsyncMock, Mock, patch

import voluptuous as vol

from test_api import ROOT


class ConfigFlow:
    def __init_subclass__(cls, **kwargs):
        pass


homeassistant = types.ModuleType("homeassistant")
homeassistant.config_entries = types.SimpleNamespace(ConfigFlow=ConfigFlow)
client = types.ModuleType("homeassistant.helpers.aiohttp_client")
client.async_get_clientsession = Mock(return_value=object())
spec = importlib.util.spec_from_file_location("packstation_test.config_flow", ROOT / "config_flow.py")
config_flow = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {"homeassistant": homeassistant, client.__name__: client}):
    spec.loader.exec_module(config_flow)


class ConfigFlowTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.flow = config_flow.PackstationConfigFlow()
        self.flow.hass = object()
        self.flow.async_show_form = Mock(side_effect=lambda **kwargs: kwargs)
        self.flow.async_create_entry = Mock(side_effect=lambda **kwargs: kwargs)
        self.flow.async_set_unique_id = AsyncMock()
        self.flow._abort_if_unique_id_configured = Mock()
        self.fetch = AsyncMock(return_value={"postal_code": "01067", "station_number": "003"})
        self.addCleanup(patch.stopall)
        patch.object(config_flow, "fetch_station", self.fetch).start()

    def assert_serializable(self, form):
        if vol.Schema.__module__.startswith("probatio"):
            from probatio.codecs.fields import to_field_list as serialize
        else:
            from voluptuous_serialize import convert as serialize
        fields = serialize(form["data_schema"])
        self.assertEqual({field["name"]: field["type"] for field in fields},
                         {"postal_code": "string", "station_number": "string"})
        json.dumps(fields)

    async def test_initial_form_serializes(self):
        form = await self.flow.async_step_user()
        self.assert_serializable(form)
        self.fetch.assert_not_awaited()

    async def test_invalid_input_returns_field_errors_without_fetching(self):
        for field, invalid_values in {
            "postal_code": ("", "1067", "001067", "01A67", "０１０６７", " 01067", "01067\n"),
            "station_number": ("", "03", "0003", "0A3", "００３", "003 ", "003\n"),
        }.items():
            for value in invalid_values:
                with self.subTest(field=field, value=value):
                    data = {"postal_code": "01067", "station_number": "003", field: value}
                    form = await self.flow.async_step_user(data)
                    self.assertEqual(form["errors"], {field: f"invalid_{field}"})
                    self.assertEqual(form["data_schema"]({}), data)
                    self.assert_serializable(form)
        form = await self.flow.async_step_user({"postal_code": "1", "station_number": "2"})
        self.assertEqual(form["errors"], {"postal_code": "invalid_postal_code",
                                          "station_number": "invalid_station_number"})
        self.fetch.assert_not_awaited()

    async def test_valid_input_preserves_leading_zeros(self):
        for postal_code, station_number, key in (("01067", "003", "1-1067003"),
                                                  ("23611", "202", "1-23611202")):
            with self.subTest(postal_code=postal_code, station_number=station_number):
                self.fetch.return_value = {"postal_code": postal_code, "station_number": station_number}
                entry = await self.flow.async_step_user({"postal_code": postal_code,
                                                        "station_number": station_number})
                self.assertEqual(entry["data"], {"station_id": key, "postal_code": postal_code,
                                                "station_number": station_number})
                self.fetch.assert_awaited_with(client.async_get_clientsession.return_value, key)
                self.flow.async_set_unique_id.assert_awaited_with(key)
                self.flow._abort_if_unique_id_configured.assert_called()

    async def test_connection_error_returns_serializable_form(self):
        self.fetch.side_effect = config_flow.PackstationError("Unavailable")
        form = await self.flow.async_step_user({"postal_code": "01067", "station_number": "003"})
        self.assertEqual(form["errors"], {"base": "cannot_connect"})
        self.assert_serializable(form)

    def test_validation_errors_have_translations(self):
        for path in (ROOT / "strings.json", *(ROOT / "translations").glob("*.json")):
            errors = json.loads(path.read_text(encoding="utf-8"))["config"]["error"]
            self.assertIn("invalid_postal_code", errors)
            self.assertIn("invalid_station_number", errors)
