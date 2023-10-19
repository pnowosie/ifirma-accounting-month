# Don't afraid of the Makefile

.DEFAULT_GOAL := help
PYTHON := .venv/bin/python

.PHONY: help check previous next adjust

##@ iFirma API calls
check: ## check current accounting month
	@env $$(cat .env) ${PYTHON} accounting_month.py

previous: ## move to previous accounting month than is actually set
	@env $$(cat .env) ${PYTHON} accounting_month.py prev

next: ## move to next accounting month than is actually set
	@env $$(cat .env) ${PYTHON} accounting_month.py next

adjust: ## set accounting month to current calendar month (if it's not already set)
	@env $$(cat .env) ${PYTHON} accounting_month.py auto

##@ How-To
help: ## display this helpful message
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
