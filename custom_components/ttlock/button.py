"""Button setup for our Integration."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import lock_coordinators
from .entity import BaseLockEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a refresh button for each lock."""

    async_add_entities(
        Refresh(coordinator) for coordinator in lock_coordinators(hass, entry)
    )


class Refresh(BaseLockEntity, ButtonEntity):
    """Button that forces a fresh fetch of the lock's state from the API."""

    _attr_icon = "mdi:refresh"

    def _update_from_coordinator(self) -> None:
        """Fetch state from the device."""
        self._attr_name = f"{self.coordinator.data.name} Refresh"

    async def async_press(self) -> None:
        """Force the coordinator to re-fetch the lock's current state."""
        await self.coordinator.async_force_state_refresh()
