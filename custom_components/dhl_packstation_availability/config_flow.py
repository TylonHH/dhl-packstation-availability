"""Configure a DHL station by type, postal code and station number."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import (
    POSTAL_CODE_PATTERN,
    STATION_NUMBER_PATTERN,
    PackstationError,
    StationNotFoundError,
    build_station_id,
    fetch_station,
)
from .const import DEFAULT_LOCATION_TYPE, DOMAIN, STATION_NAMES


class PackstationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for one station."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Ask for station type, postal code and station number and validate the location."""
        errors = {}
        location_type = (user_input or {}).get("location_type", DEFAULT_LOCATION_TYPE)
        if user_input is not None:
            postal_code = user_input["postal_code"]
            station_number = user_input["station_number"]
            if not isinstance(location_type, str) or location_type not in STATION_NAMES:
                errors["location_type"] = "invalid_location_type"
                location_type = DEFAULT_LOCATION_TYPE
            if not POSTAL_CODE_PATTERN.fullmatch(postal_code):
                errors["postal_code"] = "invalid_postal_code"
            if not STATION_NUMBER_PATTERN.fullmatch(station_number):
                errors["station_number"] = "invalid_station_number"
        if user_input is not None and not errors:
            key = build_station_id(postal_code, station_number, location_type)
            try:
                station = await fetch_station(async_get_clientsession(self.hass), key)
            except StationNotFoundError:
                errors["base"] = "not_found"
            except PackstationError:
                errors["base"] = "cannot_connect"
            else:
                if station["postal_code"] != postal_code or station["station_number"] != station_number:
                    errors["base"] = "wrong_station"
                else:
                    await self.async_set_unique_id(key)
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(
                        title=f"{STATION_NAMES[location_type]} {station_number} ({postal_code})",
                        data={
                            "station_id": key,
                            "postal_code": postal_code,
                            "station_number": station_number,
                            "location_type": location_type,
                        },
                    )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("location_type", default=location_type): vol.In(STATION_NAMES),
                vol.Required("postal_code", default=(user_input or {}).get("postal_code", "")): str,
                vol.Required("station_number", default=(user_input or {}).get("station_number", "")): str,
            }),
            errors=errors,
        )

