from pathlib import Path

import pytest
import requests
from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).parents[1] / "APP.py"


class FakeResponse:
    status_code = 200

    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


def set_fake_credentials(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
    monkeypatch.setenv("PAYPAL_CLIENT_ID", "test-paypal-client")
    monkeypatch.setenv("PAYPAL_SECRET", "test-paypal-secret")
    monkeypatch.delenv("ZAPIER_WEBHOOK_URL", raising=False)


def mock_gemini_tool_call(monkeypatch, agreed_price):
    calls = []

    def fake_post(url, **kwargs):
        calls.append((url, kwargs))
        if "generateContent" in url:
            return FakeResponse(
                {
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {"text": "Sounds good—let's make it official."},
                                    {
                                        "functionCall": {
                                            "name": "request_paypal_checkout",
                                            "args": {"agreed_price": agreed_price},
                                        }
                                    },
                                ]
                            }
                        }
                    ]
                }
            )
        if url.endswith("/v1/oauth2/token"):
            return FakeResponse({"access_token": "test-access-token"})
        return FakeResponse(
            {
                "links": [
                    {
                        "rel": "approve",
                        "href": "https://www.sandbox.paypal.com/checkout?token=test",
                    }
                ]
            }
        )

    monkeypatch.setattr(requests, "post", fake_post)
    return calls


def submit_agreement(app, monkeypatch, agreed_price):
    set_fake_credentials(monkeypatch)
    calls = mock_gemini_tool_call(monkeypatch, agreed_price)
    app.chat_input[0].set_value(f"I agree to ${agreed_price}.").run()
    return calls


def test_app_renders_without_errors(monkeypatch):
    for name in ("GEMINI_API_KEY", "PAYPAL_CLIENT_ID", "PAYPAL_SECRET"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(
        requests,
        "post",
        lambda *args, **kwargs: pytest.fail("App made an unexpected API request"),
    )

    app = AppTest.from_file(str(APP_PATH)).run()

    assert not app.exception
    assert any("GEMINI_API_KEY" in warning.value for warning in app.warning)


def test_sidebar_accepts_session_only_credentials(monkeypatch):
    for name in ("GEMINI_API_KEY", "PAYPAL_CLIENT_ID", "PAYPAL_SECRET"):
        monkeypatch.delenv(name, raising=False)

    app = AppTest.from_file(str(APP_PATH)).run()
    for key, value in (
        ("local_gemini_api_key", "session-gemini-key"),
        ("local_paypal_client_id", "session-paypal-client"),
        ("local_paypal_secret", "session-paypal-secret"),
    ):
        app.text_input(key=key).set_value(value)
    app.run()

    assert not app.exception
    assert not any("GEMINI_API_KEY" in warning.value for warning in app.warning)


def test_agreed_price_creates_paypal_checkout(monkeypatch):
    app = AppTest.from_file(str(APP_PATH)).run()
    calls = submit_agreement(app, monkeypatch, 75)

    order_call = next(
        kwargs for url, kwargs in calls if url.endswith("/v2/checkout/orders")
    )
    assert not app.exception
    assert order_call["headers"]["Authorization"] == "Bearer test-access-token"
    assert order_call["json"]["purchase_units"][0]["amount"]["value"] == "75.00"
    assert any(
        button.label == "Pay with PayPal Sandbox" for button in app.link_button
    )


@pytest.mark.parametrize("agreed_price", [64.99, 90.01])
def test_prices_outside_seller_range_never_create_checkout(
    monkeypatch, agreed_price
):
    app = AppTest.from_file(str(APP_PATH)).run()
    calls = submit_agreement(app, monkeypatch, agreed_price)

    assert not app.exception
    assert not any(url.endswith("/v2/checkout/orders") for url, _ in calls)
    assert any(
        "lowest acceptable price" in element.value.lower()
        for element in app.markdown
    )
