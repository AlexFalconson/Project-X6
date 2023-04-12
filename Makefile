.SILENT:
.NOTPARALLEL:

## Settings
.DEFAULT_GOAL := help

## Colors
COLOR_RESET   = \033[0m
COLOR_INFO    = \033[32m
COLOR_COMMENT = \033[33m
COLOR_MAGENTA = \033[35m

export RUN_AS_USER=$(shell id -u)

include .env
export

## Help
help:
	printf "${COLOR_COMMENT}Usage:${COLOR_RESET}\n"
	printf " make [target]\n\n"
	printf "${COLOR_COMMENT}Available targets:${COLOR_RESET}\n"
	awk '/^[a-zA-Z\-\_0-9\.@]+:/ { \
	helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
				helpCommand = substr($$1, 0, index($$1, ":")); \
				helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
				printf " ${COLOR_INFO}%-30s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
		} \
		{ lastLine = $$0 }' $(MAKEFILE_LIST)

## Сборка/обновление контейнера
container@build:
	docker-compose pull
	docker-compose build --pull
	docker-compose run --rm -u root app sh -c "chown $(RUN_AS_USER):$(RUN_AS_USER) -R /opt/venv/"
	docker-compose run --rm app sh -c "rm -Rf /opt/venv/* && pipenv install --dev"
.PHONY: container@build

## Запуск контейнера
container@start:
	docker-compose up -d
.PHONY: container@start

## Остановка контейнера
container@stop:
	docker-compose down
.PHONY: container@stop

## Рестарт контейнера
container@restart: container@stop container@start
.PHONY: container@restart

## Console
container@console:
	docker-compose exec app pipenv run bash
.PHONY: container@console

## Просмотр логов запущенного контейнера
container@logs:
	docker-compose logs -f
.PHONY: container@logs

## Сборка проекта (DEV)
project@build-dev: container@start
	docker-compose run --rm app pipenv run build-dev
.PHONY: project@build-dev

## Сборка проекта (PROD)
project@build: container@start
	docker-compose run --rm app pipenv run build
.PHONY: project@build

## Тестирование проекта
project@test: container@start
	docker-compose run --rm app pipenv run test
.PHONY: project@test
