"""Conversation platform for n8n integration."""

import json
import logging
from typing import Any, Literal

import aiohttp

from homeassistant.components import conversation
from homeassistant.components.homeassistant import async_should_expose
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import (
    area_registry as ar,
    device_registry as dr,
    entity_registry as er,
)
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_OUTPUT_FIELD, CONF_WEBHOOK_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the integration from a config entry."""
    async_add_entities(
        [N8nConversationEntity(config_entry)],
    )


class N8nConversationEntity(
    conversation.ConversationEntity, conversation.AbstractConversationAgent
):
    """n8n conversation agent."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self._config_entry = config_entry
        self._webhook_url = config_entry.options[CONF_WEBHOOK_URL]
        self._attr_supported_features = conversation.ConversationEntityFeature.CONTROL
        self._attr_unique_id = config_entry.entry_id
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name=config_entry.title,
            manufacturer="n8n",
            entry_type=dr.DeviceEntryType.SERVICE,
        )

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def async_added_to_hass(self) -> None:
        """When entity is added to Home Assistant."""
        await super().async_added_to_hass()
        conversation.async_set_agent(self.hass, self._config_entry, self)

    async def async_will_remove_from_hass(self) -> None:
        """When entity will be removed from Home Assistant."""
        conversation.async_unset_agent(self.hass, self._config_entry)
        await super().async_will_remove_from_hass()

    async def _async_handle_message(
        self,
        user_input: conversation.ConversationInput,
        chat_log: conversation.ChatLog,
    ) -> conversation.ConversationResult:
        """Process the user input and call the API."""
        try:
            await chat_log.async_provide_llm_data(user_input.as_llm_context(DOMAIN))
        except conversation.ConverseError as err:
            return err.as_conversation_result()

        await self._async_handle_chat_log(user_input, chat_log)

        return conversation.async_get_result_from_chat_log(user_input, chat_log)

    async def _async_handle_chat_log(
        self,
        user_input: conversation.ConversationInput,
        chat_log: conversation.ChatLog,
    ) -> None:
        """Send the chat log to the n8n webhook and process the response."""
        messages = [
            self._convert_content_to_param(content) for content in chat_log.content
        ]
        user_messages = [
            user_message for user_message in messages if user_message["role"] == "user"
        ]

        if not user_messages:
            raise HomeAssistantError("No user message found in chat log")

        def set_default(obj: Any) -> Any:
            if isinstance(obj, set):
                return list(obj)
            return obj

        payload = {
            "user_id": user_input.context.user_id,
            "messages": messages,
            "query": user_messages[-1]["content"],
            "exposed_entities": json.dumps(
                self._get_exposed_entities(), default=set_default
            ),
        }

        async with (
            aiohttp.ClientSession() as session,
            session.post(self._webhook_url, json=payload, timeout=10) as response,
        ):
            if response.status != 200:
                raise HomeAssistantError(
                    f"Error contacting n8n webhook: HTTP {response.status} - {response.reason}"
                )

            data = await response.json()

            if not isinstance(data, dict):
                raise HomeAssistantError(
                    "Invalid response from n8n webhook, expected a JSON object"
                )

        output_field = self._config_entry.options[CONF_OUTPUT_FIELD]
        reply = data.get(output_field)

        if not reply:
            raise HomeAssistantError("No response found in n8n webhook data")

        async for content in chat_log.async_add_assistant_content(
            conversation.AssistantContent(
                self.entity_id,
                reply,
            )
        ):
            messages.extend(self._convert_content_to_param(content))

    def _convert_content_to_param(
        self, content: conversation.Content
    ) -> dict[str, Any]:
        """Convert any native chat message for this agent to the native format."""
        return {
            "role": content.role,
            "content": content.content,
        }

    def _get_exposed_entities(self) -> list[dict[str, Any]]:
        states = [
            state
            for state in self.hass.states.async_all()
            if async_should_expose(self.hass, conversation.DOMAIN, state.entity_id)
        ]
        entity_registry = er.async_get(self.hass)
        device_registry = dr.async_get(self.hass)
        area_registry = ar.async_get(self.hass)
        exposed_entities: list[dict[str, Any]] = []

        for state in states:
            entity_id = state.entity_id
            entity = entity_registry.async_get(entity_id)

            aliases = []
            if entity and entity.aliases:
                aliases = entity.aliases

            area_id = None
            area_name = None

            if entity and entity.area_id:
                area_id = entity.area_id
                area = area_registry.async_get_area(area_id)
                if area:
                    area_name = area.name
            elif entity and entity.device_id:
                device = device_registry.async_get(entity.device_id)
                if device and device.area_id:
                    area_id = device.area_id
                    area = area_registry.async_get_area(area_id)
                    if area:
                        area_name = area.name

            exposed_entities.append(
                {
                    "entity_id": entity_id,
                    "name": state.name,
                    "state": self.hass.states.get(entity_id).state,
                    "aliases": aliases,
                    "area_id": area_id,
                    "area_name": area_name,
                }
            )
        return exposed_entities
