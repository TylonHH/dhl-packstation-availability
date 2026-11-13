"""Read and validate DHL Postfinder data."""

import re
from datetime import datetime

from aiohttp import ClientError

from .const import BASE_URL

KEY_PATTERN = re.compile(r"^[0-9]+-[0-9]+$")
POSTAL_CODE_PATTERN = re.compile(r"^[0-9]{5}$")
STATION_NUMBER_PATTERN = re.compile(r"^[0-9]{3}$")
SIZES = {"s": "freeCompartmentsS", "m": "freeCompartmentsM", "l": "freeCompartmentsL", "xl": "freeCompartmentsXl"}


class PackstationError(Exception):
    """DHL response cannot be used."""


def build_station_id(postal_code: str, station_number: str) -> str:
    """Build DHL's key, dropping leading zeros only from the postal code."""
    if not POSTAL_CODE_PATTERN.fullmatch(postal_code):
        raise ValueError("Postal code must contain five digits")
    if not STATION_NUMBER_PATTERN.fullmatch(station_number):
        raise ValueError("Packstation number must contain three digits")
    return f"1-{int(postal_code)}{station_number}"


def parse_station(payload: object, key: str) -> dict:
    """Validate a location and keep only values needed by entities."""
    if not isinstance(payload, dict) or payload.get("primaryKeyPF") != key:
        raise PackstationError("DHL returned an unexpected location")
    if payload.get("locationType") != "PACKSTATION":
        raise PackstationError("Location is not a Packstation")
    status = payload.get("liveStatus")
    if not isinstance(status, dict):
        raise PackstationError("Live compartment data is unavailable")
    counts = {}
    for size, field in SIZES.items():
        value = status.get(field)
        counts[size] = value if type(value) is int and value >= 0 else None
    if all(value is None for value in counts.values()):
        raise PackstationError("No live compartment counts were returned")
    timestamp = status.get("sourceTimestamp")
    try:
        updated = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
    except (TypeError, ValueError):
        updated = None
    return {
        "name": payload.get("locationName") or payload.get("keyWord") or key,
        "postal_code": payload.get("zipCode"),
        "station_number": payload.get("primaryKeyZipRegion"),
        "address": ", ".join(filter(None, [" ".join(filter(None, [payload.get("street"), payload.get("houseNo")])), " ".join(filter(None, [payload.get("zipCode"), payload.get("city")]))])),
        "counts": counts,
        "updated": updated,
    }


async def fetch_station(session, key: str) -> dict:
    """Fetch one station. A 204 means its key is unknown."""
    if not KEY_PATTERN.fullmatch(key):
        raise PackstationError("Invalid Packstation ID")
    try:
        async with session.get(BASE_URL + key, timeout=15) as response:
            if response.status == 204 or response.status == 404:
                raise PackstationError("Packstation ID was not found")
            response.raise_for_status()
            return parse_station(await response.json(), key)
    except (ClientError, TimeoutError, ValueError) as error:
        raise PackstationError(str(error)) from error

