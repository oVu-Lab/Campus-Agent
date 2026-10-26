# CampusAgent

CampusAgent is a Streamlit demo for campus marketplace negotiations. Gemini handles the conversation, seller controls set the listing and protected floor, PayPal Sandbox creates an approval order after an agreement, and Zapier can receive a deal event after order creation.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run APP.py
```

For local testing, enter credentials in the password fields in the private Seller dashboard. They remain in the current Streamlit session. For repeatable local setup, add them to `.streamlit/secrets.toml` (that file is git-ignored):

```toml
GEMINI_API_KEY = "..."
PAYPAL_CLIENT_ID = "..."
PAYPAL_SECRET = "..."
ZAPIER_WEBHOOK_URL = "..."
```

Deployment environment variables take precedence over Streamlit secrets and session inputs. Zapier is optional; Gemini and PayPal Sandbox credentials are needed for live negotiation and checkout.

## Deploy on Render

The repository includes a `render.yaml` Blueprint for the Streamlit app. Connect the repository in Render and provide `GEMINI_API_KEY`, `PAYPAL_CLIENT_ID`, and `PAYPAL_SECRET` in the service environment. Add `ZAPIER_WEBHOOK_URL` if deal notifications are enabled. The app binds to Render's `PORT` and uses the Streamlit health endpoint.

PayPal Sandbox checkout creates an approval link. The app does not capture payment or claim that an order has been paid. Zapier receives a `DEAL_FINALIZED` event with status `PAYPAL_CHECKOUT_CREATED` after the order and approval link are created.

## Integrations

- **AG Grid:** Seller inventory table with editable listing price and protected floor. Changes sync into Streamlit session state and the same guardrails used by Gemini and PayPal.
- **Gemini:** Negotiation responses and an agreement-only PayPal checkout tool call.
- **PayPal Sandbox:** Creates an order and returns the buyer approval URL.
- **Zapier:** Optional asynchronous webhook notification after PayPal order creation.
