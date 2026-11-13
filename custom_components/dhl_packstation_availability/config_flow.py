"""Configure a DHL Packstation by Postfinder ID."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PackstationError, fetch_station
from .const import DOMAIN


class PackstationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for one station."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Ask for an ID and confirm that DHL knows it."""
        errors = {}
        if user_input is not None:
            key = user_input["station_id"].strip()
            await self.async_set_unique_id(key)
            self._abort_if_unique_id_configured()
            try:
                station = await fetch_station(async_get_clientsession(self.hass), key)
            except PackstationError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=f"{station['name']} ({key})", data={"station_id": key})
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({vol.Required("station_id"): str}), errors=errors,
        )

