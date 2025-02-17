"""Base Entity for Roku."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import RokuDataUpdateCoordinator
from .const import DOMAIN


class RokuEntity(CoordinatorEntity):
    """Defines a base Roku entity."""

    coordinator: RokuDataUpdateCoordinator

    def __init__(
        self,
        *,
        device_id: str,
        coordinator: RokuDataUpdateCoordinator,
        description: EntityDescription | None = None,
    ) -> None:
        """Initialize the Roku entity."""
        super().__init__(coordinator)
        self._device_id = device_id

        if description is not None:
            self.entity_description = description
            self._attr_name = f"{coordinator.data.info.name} {description.name}"
            self._attr_unique_id = f"{device_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this Roku device."""
        if self._device_id is None:
            return None

        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self.coordinator.data.info.name,
            manufacturer=self.coordinator.data.info.brand,
            model=self.coordinator.data.info.model_name,
            hw_version=self.coordinator.data.info.model_number,
            sw_version=self.coordinator.data.info.version,
            suggested_area=self.coordinator.data.info.device_location,
        )
