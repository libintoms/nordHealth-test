from collections.abc import Callable

from playwright.sync_api import Dialog, Page


def click_and_capture_alert(
    page: Page, click_action: Callable[[], None], settle_ms: int = 1000
) -> str | None:
    """Click and return alert text if a browser dialog appears; otherwise None."""
    captured: dict[str, str] = {}

    def on_dialog(dialog: Dialog) -> None:
        captured["message"] = dialog.message
        dialog.accept()

    page.on("dialog", on_dialog)
    try:
        click_action()
        page.wait_for_timeout(settle_ms)
    finally:
        page.remove_listener("dialog", on_dialog)

    return captured.get("message")
