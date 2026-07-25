"""Test the TTLock refresh button."""

from unittest.mock import patch

from homeassistant.components.button import DOMAIN as BUTTON_DOMAIN, SERVICE_PRESS
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant


def _button_entity_id(coordinator) -> str:
    """Return the refresh button entity id for a lock coordinator."""
    return next(
        entity.entity_id
        for entity in coordinator.entities
        if entity.entity_id.startswith("button.")
    )


async def test_refresh_button_created(
    hass: HomeAssistant, mock_api_responses, component_setup
):
    """A refresh button is created for the lock."""
    mock_api_responses("default")
    coordinator = await component_setup()

    entity_id = _button_entity_id(coordinator)
    assert hass.states.get(entity_id) is not None


async def test_refresh_button_forces_state_refresh(
    hass: HomeAssistant, mock_api_responses, component_setup
):
    """Pressing the button clears cached state and re-fetches from the API."""
    mock_api_responses("default")
    coordinator = await component_setup()
    entity_id = _button_entity_id(coordinator)

    with patch.object(coordinator, "async_refresh") as mock_refresh:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            SERVICE_PRESS,
            {ATTR_ENTITY_ID: entity_id},
            blocking=True,
        )
        await hass.async_block_till_done()

        assert mock_refresh.called
        # locked is cleared so _async_update_data re-queries the lock state.
        assert coordinator.data.locked is None
