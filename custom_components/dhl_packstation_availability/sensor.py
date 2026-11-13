"""Free compartment count sensors."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Create four size sensors and one total sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(PackstationSensor(coordinator, entry.data["station_id"], size) for size in ("s", "m", "l", "xl", "total"))


class PackstationSensor(CoordinatorEntity, SensorEntity):
    """One free compartment count."""

    _attr_icon = "mdi:package-variant"
    _attr_has_entity_name = True

    def __init__(self, coordinator, station_id, size):
        super().__init__(coordinator)
        self._size = size
        self._attr_unique_id = f"{station_id}_{size}"
        self._attr_translation_key = f"free_{size}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, station_id)},
            name=f"DHL Packstation {coordinator.data['name']}",
            manufacturer="DHL",
            model="Packstation",
            configuration_url=f"https://www.dhl.de/int-postfinder/webservice/rest/v1/locationByPrimaryKeyPF/{station_id}",
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

