.ONESHELL:

PROJECT_ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.DEFAULT_GOAL := start

start: ml_service db_service krakend nginx tg_client
		@echo "All services have launched"

down_all: down_ml_service down_db_service down_krakend down_nginx down_tg_client
		@echo "All services have stopped"

ml_service:
	cd $(PROJECT_ROOT)/ml_service && docker compose up -d --build

db_service:
	cd $(PROJECT_ROOT)/db_service && docker compose up -d --build

krakend:
	cd $(PROJECT_ROOT)/krakend && docker compose up -d --build

nginx:
	cd $(PROJECT_ROOT)/nginx && docker compose up -d --build

tg_client:
	cd $(PROJECT_ROOT)/tg_client && docker compose up -d --build

down_ml_service:
	cd $(PROJECT_ROOT)/ml_service && docker compose down

down_db_service:
	cd $(PROJECT_ROOT)/db_service && docker compose down

down_krakend:
	cd $(PROJECT_ROOT)/krakend && docker compose down

down_nginx:
	cd $(PROJECT_ROOT)/nginx && docker compose down

down_tg_client:
	cd $(PROJECT_ROOT)/tg_client && docker compose down


.PHONY: start ml_service db_service krakend nginx tg_client down_ml_service down_db_service down_krakend down_krakend down down_tg_client

