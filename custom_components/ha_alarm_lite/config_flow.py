from __future__ import annotations

from typing import Any, List
import os
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_INDICATOR,
    CONF_SIREN_PLAYER,
    CONF_SIREN_VOLUME,
    CONF_MP3_SOURCE,
    CONF_ENTRY_SENSORS,
    CONF_NFC_TAG_ID,
    CONF_EXIT_DELAY,
    CONF_ENTRY_DELAY,
    CONF_ACCEPT_ANY_WHEN_TRIGGERED,
    CONF_AUTO_DISARM_TIME,
    DEFAULT_EXIT_DELAY,
    DEFAULT_ENTRY_DELAY,
    DEFAULT_SIREN_VOLUME,
    DEFAULT_AUTO_DISARM_TIME,
)


def _normalize_media_source(path: str) -> str:
    """Accept raw file paths and convert to media-source://."""
    if not path:
        return path
    p = str(path).strip().replace("\\", "/")
    if p.startswith("media-source://"):
        return p
    # map /config/www and www/ to local media_source
    if "/www/" in p or p.startswith("www/") or p.startswith("/config/www/"):
        rel = p.split("/www/", 1)[1] if "/www/" in p else p.split("www/", 1)[1]
        return f"media-source://media_source/local/{rel}"
    # map /media to media_source
    if p.startswith("/media/") or p.startswith("media/"):
        rel = p.split("/media/", 1)[1] if "/media/" in p else p.split("media/", 1)[1]
        return f"media-source://media_source/{rel}"
    return p


def _mp3_select(hass) -> selector.SelectSelector:
    """Create a dropdown with discovered MP3 files (+ custom input)."""
    options: List[selector.SelectOptionDict] = []
    roots = [
        (hass.config.path("www"), "www"),
        (hass.config.path("media"), "media"),
        ("/media", "media"),  # HA OS mount (just in case)
    ]
    seen = set()
    for root, label_root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            for fn in sorted(filenames):
                if not fn.lower().endswith(".mp3"):
                    continue
                full = os.path.join(dirpath, fn)
                try:
                    rel = os.path.relpath(full, root).replace("\\", "/")
                except ValueError:
                    # if relpath fails due to different drive on Windows, skip
                    continue
                if label_root == "www":
                    uri = f"media-source://media_source/local/{rel}"
                    label = f"www/{rel}"
                else:
                    uri = f"media-source://media_source/{rel}"
                    label = f"media/{rel}"
                if uri in seen:
                    continue
                seen.add(uri)
                options.append(selector.SelectOptionDict(value=uri, label=label))

    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=options,
            custom_value=True,
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )


async def _tag_select(hass) -> selector.SelectSelector:
    """Create a dropdown with tags from Tag manager (+ custom input)."""
    options: List[selector.SelectOptionDict] = []
    try:
        # HA API for Tag manager
        from homeassistant.components.tag import async_get_manager  # type: ignore
        manager = await async_get_manager(hass)
        tags = await manager.async_list()
        for t in tags:
            # t can be dict or object depending on version
            tag_id = t.get("id") if isinstance(t, dict) else getattr(t, "id", None)
            tag_id = tag_id or (t.get("tag_id") if isinstance(t, dict) else getattr(t, "tag_id", None))
            name = (t.get("name") if isinstance(t, dict) else getattr(t, "name", None)) or tag_id
            if not tag_id:
                continue
            label = f"{name} ({tag_id})" if name and name != tag_id else tag_id
            options.append(selector.SelectOptionDict(value=tag_id, label=label))
    except Exception:
        # Silent fallback: empty list -> still allows custom value
        pass

    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=options,
            custom_value=True,
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )


class AlarmLiteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            if user_input.get(CONF_MP3_SOURCE):
                user_input[CONF_MP3_SOURCE] = _normalize_media_source(user_input[CONF_MP3_SOURCE])
            return self.async_create_entry(
                title="HA Alarm Lite",
                data={},
                options=user_input,
            )

        schema = vol.Schema({
            vol.Required(CONF_INDICATOR): selector.selector({"entity": {"domain": "light"}}),
            vol.Required(CONF_SIREN_PLAYER): selector.selector({"entity": {"domain": "media_player"}}),
            vol.Optional(CONF_SIREN_VOLUME, default=DEFAULT_SIREN_VOLUME): selector.selector({"number": {"min": 0, "max": 1, "step": 0.05}}),
            vol.Required(CONF_MP3_SOURCE): _mp3_select(self.hass),
            vol.Required(CONF_ENTRY_SENSORS): selector.selector({"entity": {"domain": "binary_sensor", "multiple": True}}),
            vol.Required(CONF_NFC_TAG_ID): await _tag_select(self.hass),
            vol.Optional(CONF_EXIT_DELAY, default=DEFAULT_EXIT_DELAY): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ENTRY_DELAY, default=DEFAULT_ENTRY_DELAY): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ACCEPT_ANY_WHEN_TRIGGERED, default=True): selector.selector({"boolean": {}}),
            vol.Optional(CONF_AUTO_DISARM_TIME, default=DEFAULT_AUTO_DISARM_TIME): selector.selector({"time": {}}),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AlarmLiteOptionsFlow(config_entry)


class AlarmLiteOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            if user_input.get(CONF_MP3_SOURCE):
                user_input[CONF_MP3_SOURCE] = _normalize_media_source(user_input[CONF_MP3_SOURCE])
            return self.async_create_entry(title="", data=user_input)

        o = self.config_entry.options

        schema = vol.Schema({
            vol.Required(CONF_INDICATOR, default=o.get(CONF_INDICATOR)): selector.selector({"entity": {"domain": "light"}}),
            vol.Required(CONF_SIREN_PLAYER, default=o.get(CONF_SIREN_PLAYER)): selector.selector({"entity": {"domain": "media_player"}}),
            vol.Optional(CONF_SIREN_VOLUME, default=o.get(CONF_SIREN_VOLUME, DEFAULT_SIREN_VOLUME)): selector.selector({"number": {"min": 0, "max": 1, "step": 0.05}}),
            vol.Required(CONF_MP3_SOURCE, default=o.get(CONF_MP3_SOURCE, "")): _mp3_select(self.hass),
            vol.Required(CONF_ENTRY_SENSORS, default=o.get(CONF_ENTRY_SENSORS, [])): selector.selector({"entity": {"domain": "binary_sensor", "multiple": True}}),
            vol.Required(CONF_NFC_TAG_ID, default=o.get(CONF_NFC_TAG_ID, "")): await _tag_select(self.hass),
            vol.Optional(CONF_EXIT_DELAY, default=o.get(CONF_EXIT_DELAY, DEFAULT_EXIT_DELAY)): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ENTRY_DELAY, default=o.get(CONF_ENTRY_DELAY, DEFAULT_ENTRY_DELAY)): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ACCEPT_ANY_WHEN_TRIGGERED, default=o.get(CONF_ACCEPT_ANY_WHEN_TRIGGERED, True)): selector.selector({"boolean": {}}),
            vol.Optional(CONF_AUTO_DISARM_TIME, default=o.get(CONF_AUTO_DISARM_TIME, DEFAULT_AUTO_DISARM_TIME)): selector.selector({"time": {}}),
        })

        return self.async_show_form(step_id="init", data_schema=schema)
