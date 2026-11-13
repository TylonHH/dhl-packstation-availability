"""DHL Packstation Availability integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PackstationError, fetch_station
from .const import DOMAIN, SCAN_INTERVAL


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up one Packstation."""
    session = async_get_clientsession(hass)

    async def update():
        try:
            return await fetch_station(session, entry.data["station_id"])
        except PackstationError as error:
            raise UpdateFailed(str(error)) from error

    coordinator = DataUpdateCoordinator(
        hass, logger=logging.getLogger(__name__), name=DOMAIN,
        update_method=update, update_interval=SCAN_INTERVAL,
    )
    await coordinator.async_refresh()
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady(coordinator.last_exception)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload one Packstation."""
    if await hass.config_entries.async_unload_platforms(entry, ["sensor"]):
        hass.data[DOMAIN].pop(entry.entry_id)
        return True
    return False

