from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from cheatsh import CheatShError, build_cheatsh_url, join_description, normalize_query, query_cheatsh

ICON = "images/icon.svg"


class CheatShExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = normalize_query(event.get_argument())

        if not query:
            return RenderResultListAction(help_items())

        try:
            result = query_cheatsh(query)
        except (CheatShError, ValueError) as exc:
            return RenderResultListAction(error_items(query, str(exc)))

        items = []

        items.extend(
            ExtensionResultItem(
                icon=ICON,
                name=item.title,
                description=item.description or "Enter copies this item",
                on_enter=ActionList(
                    [
                        CopyToClipboardAction(item.copy_text or item.description or item.title),
                        HideWindowAction(),
                    ]
                ),
            )
            for item in result.preview_items
        )

        items.append(
            ExtensionResultItem(
                icon=ICON,
                name="Copy full answer",
                description=f"All cheat.sh output for {result.query}",
                on_enter=ActionList(
                    [
                        CopyToClipboardAction(result.text),
                        HideWindowAction(),
                    ]
                ),
            )
        )

        items.append(
            ExtensionResultItem(
                icon=ICON,
                name="Open in browser",
                description=result.url,
                on_enter=OpenUrlAction(result.url),
            )
        )

        return RenderResultListAction(items)


def help_items():
    return [
        ExtensionResultItem(
            icon=ICON,
            name="Type a cheat.sh query",
            description="Examples: cht tar | cht python list comprehension | cht python/random list elements",
            on_enter=HideWindowAction(),
        )
    ]


def error_items(query, message):
    items = [
        ExtensionResultItem(
            icon=ICON,
            name="Could not load cheat.sh results",
            description=message,
            on_enter=HideWindowAction(),
        )
    ]

    try:
        url = build_cheatsh_url(query)
    except ValueError:
        return items

    items.append(
        ExtensionResultItem(
            icon=ICON,
            name="Open cheat.sh in browser",
            description=url,
            on_enter=OpenUrlAction(url),
        )
    )
    return items


if __name__ == "__main__":
    CheatShExtension().run()
