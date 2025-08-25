#!/usr/bin/env bash
set -euo pipefail

echo "== ClipKitAI Webhook Smoke =="

: "${REPL_WEBHOOK_URL:?Set REPL_WEBHOOK_URL to https://<your-repl>.repl.co/webhook/sale}"
: "${STRIPE_API_KEY:?Set STRIPE_API_KEY to your Stripe *test* secret key (sk_test_...)}"

HEALTH_URL="$(echo "$REPL_WEBHOOK_URL" | sed 's|/webhook/sale$|/health|')"

echo "[1/3] Health check -> $HEALTH_URL"
curl -sf "$HEALTH_URL" | sed 's/.*/✅ Health OK/'
echo

echo "[2/3] Trigger payment_intent.succeeded"
STRIPE_API_KEY="$STRIPE_API_KEY" stripe trigger payment_intent.succeeded >/dev/null
echo "✅ Triggered payment_intent.succeeded"

echo "[3/3] Trigger checkout.session.completed"
STRIPE_API_KEY="$STRIPE_API_KEY" stripe trigger checkout.session.completed >/dev/null
echo "✅ Triggered checkout.session.completed"

cat <<'NOTE'

Next:
- Watch your Replit console for verified events written by the webhook.
- If nothing arrives, confirm:
  * Replit app is running.
  * Stripe Dashboard → Developers → Webhooks has an endpoint pointing to your REPL /webhook/sale.
  * STRIPE_WEBHOOK_SECRET in Replit matches the signing secret shown on the Stripe endpoint.
NOTE
