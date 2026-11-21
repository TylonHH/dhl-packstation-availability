"""Exercise setup with Home Assistant 2026.2.3 and its real config entries."""

from unittest.mock import AsyncMock, MagicMock, call

import pytest
from homeassistant.config_entries import SOURCE_USER, ConfigEntryState
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.dhl_packstation_availability import config_flow
from custom_components.dhl_packstation_availability.const import BASE_URL, DOMAIN


@pytest.fixture
def dhl_session(monkeypatch):
    """Mock the HTTP session for both config flow and coordinator requests."""
    session = MagicMock()
    monkeypatch.setattr(config_flow, "async_get_clientsession", lambda hass: session)
    monkeypatch.setattr(f"custom_components.{DOMAIN}.async_get_clientsession", lambda hass: session)
    return session


def mock_station(session, station_id, location_type, postal_code, station_number):
    response = MagicMock()
    response.status = 200
    response.raise_for_status = MagicMock()
    response.json = AsyncMock(return_value={
        "primaryKeyPF": station_id,
        "locationType": location_type,
        "zipCode": postal_code,
        "primaryKeyZipRegion": station_number,
        "liveStatus": {
            "freeCompartmentsS": 0,
            "freeCompartmentsM": 2,
            "freeCompartmentsL": 3,
            "freeCompartmentsXl": 4,
        },
    })
    session.get.return_value.__aenter__.return_value = response


def assert_sensors(hass, entry, station_id):
    assert entry.state is ConfigEntryState.LOADED
    registry = er.async_get(hass)
    for size, expected in {"s": "0", "m": "2", "l": "3", "xl": "4", "total": "9"}.items():
        entity_id = registry.async_get_entity_id("sensor", DOMAIN, f"{station_id}_{size}")
        assert entity_id is not None
        state = hass.states.get(entity_id)
        assert state is not None
        assert state.state == expected


@pytest.mark.parametrize(
    ("location_type", "postal_code", "station_number", "station_id", "title"),
    [
        ("PACKSTATION", "01067", "003", "1-1067003", "Packstation 003 (01067)"),
        ("DEIN_FACH", "12345", "101", "13-12345101", "DeinFach 101 (12345)"),
    ],
)
async def test_config_flow_sets_up_sensors(
    hass, enable_custom_integrations, dhl_session,
    location_type, postal_code, station_number, station_id, title,
):
    mock_station(dhl_session, station_id, location_type, postal_code, station_number)
    form = await hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_USER})
    assert form["type"] is FlowResultType.FORM
    data = {"location_type": location_type, "postal_code": postal_code, "station_number": station_number}
    result = await hass.config_entries.flow.async_configure(form["flow_id"], data)
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == title
    entry = result["result"]
    assert entry.unique_id == station_id
    assert entry.data == {"station_id": station_id, **data}
    assert_sensors(hass, entry, station_id)
    assert dhl_session.get.call_args_list == [call(BASE_URL + station_id, timeout=15)] * 2


async def test_existing_packstation_sets_up_sensors(hass, enable_custom_integrations, dhl_session):
    station_id = "1-1067003"
    mock_station(dhl_session, station_id, "PACKSTATION", "01067", "003")
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Packstation 003 (01067)",
        data={"station_id": station_id, "postal_code": "01067", "station_number": "003"},
        unique_id=station_id,
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert_sensors(hass, entry, station_id)
    dhl_session.get.assert_called_once_with(BASE_URL + station_id, timeout=15)
