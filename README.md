# clipkitai

## Getting Started
1. Copy `.env.example` to `.env` and fill in your tokens.
2. Add the same tokens to **GitHub \u2192 Settings \u2192 Secrets \u2192 Actions** with the names used above.
3. Trigger the *ClipKitAi nightly run* workflow manually once to verify end-to-end.

## Getting Started (Week-0 MVP)

Prereqs: [Stripe CLI](https://stripe.com/docs/stripe-cli), `curl`.

Environment:
- Copy `.env.example` to `.env` for local development.
- In Replit, set secrets for `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET`.

Webhook URL: ensure Stripe Dashboard → Webhooks points to `${REPL_WEBHOOK_URL}`.

Run tests:

```sh
export $(grep -v '^#' .env | xargs)   # optional
make webhook-test
```

### Acceptance checklist

- `/health` returns 200 with `{ "status": "ok" }`.
- Stripe triggers succeed; events appear in Replit logs (buyer/product/amount/timestamp captured).
- Payhip product page publicly loads and checkout completes.

### Secrets matrix

Canonical names: `HUGGINGFACE_API_TOKEN`, `PAYHIP_API_KEY`. Back-compat shims for `HUGGINGFACE_TOKEN` & `PAYHIP_TOKEN` until code aligned.

Pinterest automation is Week-3 (manual pinning OK meanwhile).
