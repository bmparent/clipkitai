.PHONY: health webhook-test lint
health:
	@curl -i $${REPL_WEBHOOK_URL%/webhook/sale}/health

webhook-test:
	bash scripts/test_webhook.sh

lint:
	@echo "No code lint yet; shellcheck on scripts"; command -v shellcheck >/dev/null && shellcheck scripts/*.sh || true
