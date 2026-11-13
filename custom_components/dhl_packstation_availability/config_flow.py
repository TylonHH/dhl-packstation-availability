"""Configure a DHL Packstation by postal code and station number."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PackstationError, build_station_id, fetch_station
from .const import DOMAIN


class PackstationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for one station."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Ask for postal code and station number and validate the location."""
        errors = {}
        if user_input is not None:
            postal_code = user_input["postal_code"]
            station_number = user_input["station_number"]
            key = build_station_id(postal_code, station_number)
            try:
                station = await fetch_station(async_get_clientsession(self.hass), key)
            except PackstationError:
                errors["base"] = "cannot_connect"
            else:
                if station["postal_code"] != postal_code or station["station_number"] != station_number:
                    errors["base"] = "wrong_station"
                else:
                    await self.async_set_unique_id(key)
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(
                        title=f"Packstation {station_number} ({postal_code})",
                        data={"station_id": key, "postal_code": postal_code, "station_number": station_number},
                    )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("postal_code"): vol.All(str, vol.Match(r"^[0-9]{5}$")),
                vol.Required("station_number"): vol.All(str, vol.Match(r"^[0-9]{3}$")),
            }),
            errors=errors,
        )

