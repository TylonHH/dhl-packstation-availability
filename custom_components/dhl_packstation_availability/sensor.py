"""Free compartment count sensors."""

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_LOCATION_TYPE, DOMAIN, STATION_NAMES


async def async_setup_entry(hass, entry, async_add_entities):
    """Create four size sensors and one total sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(PackstationSensor(coordinator, entry.data["station_id"], size) for size in ("s", "m", "l", "xl", "total"))


class PackstationSensor(CoordinatorEntity, SensorEntity):
    """One free compartment count."""

    _attr_icon = "mdi:package-variant"
    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator, station_id, size):
        super().__init__(coordinator)
        self._size = size
        self._attr_unique_id = f"{station_id}_{size}"
        self._attr_translation_key = f"free_{size}"
        location_type = coordinator.data.get("location_type", DEFAULT_LOCATION_TYPE)
        model = STATION_NAMES[location_type]
        name = coordinator.data["name"] if location_type == DEFAULT_LOCATION_TYPE else station_id[-3:]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, station_id)},
            name=f"DHL {model} {name}",
            manufacturer="DHL",
            model=model,
            configuration_url=f"https://www.dhl.de/de/privatkunden/dhl-standorte-finden.html?primaryKeyPF={station_id}",
        )

    @property
    def native_value(self):
        """Return a size count, or total only when every size is known."""
        counts = self.coordinator.data["counts"]
        if self._size == "total":
            return sum(counts.values()) if all(value is not None for value in counts.values()) else None
        return counts[self._size]

    @property
    def available(self):
        """Missing counts must not look like zero."""
        return super().available and self.native_value is not None

    @property
    def extra_state_attributes(self):
        """Expose source time and station address."""
        data = self.coordinator.data
        return {"source_timestamp": data["updated"].isoformat() if data["updated"] else None, "address": data["address"]}

