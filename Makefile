SHELL=/bin/bash -e

.DEFAULT_GOAL := help

COMPOSE := ./docker-compose.yml
DJANGO := ./src/manage.py


compose_v2_not_supported = $(shell command docker compose 2> /dev/null)
ifeq (,$(compose_v2_not_supported))
  DOCKER_COMPOSE_COMMAND = docker-compose
else
  DOCKER_COMPOSE_COMMAND = docker compose
endif

help:
	@echo "Make Application Docker Images and Containers using Docker-Compose files in 'docker' Dir."
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

upb:  ## compose up and build images
	${DOCKER_COMPOSE_COMMAND} -f ${COMPOSE} up -d --build

up:  ## compose up
	${DOCKER_COMPOSE_COMMAND} -f ${COMPOSE} up -d

downv:  ## compose down with volumes
	${DOCKER_COMPOSE_COMMAND} -f ${COMPOSE} down -v

down:  ## compose down
	${DOCKER_COMPOSE_COMMAND} -f ${COMPOSE} down

frun:  ## frist run with collectstatic and migrations
	python ${DJANGO} migrate
	python ${DJANGO} collectstatic --no-input
	python ${DJANGO} createsuperuserauto
	@make run

run:  ## run django local
	python ${DJANGO} runserver 8001

lup:  ## up local without app in docker
	@make up
	@make frun
