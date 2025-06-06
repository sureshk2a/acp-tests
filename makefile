.PHONY: up down build

down:
	docker-compose -f router_agent/docker-compose.yml down
	timeout 2
	docker-compose -f agent_one/docker-compose.yml down
	timeout 2
	docker-compose -f agent_two/docker-compose.yml down

build:
	(cd router_agent && uv sync)
	(cd agent_one && uv sync)
	(cd agent_two && uv sync)

up: down build
	docker-compose -f router_agent/docker-compose.yml up -d
	timeout 2
	docker-compose -f agent_one/docker-compose.yml up -d
	timeout 2
	docker-compose -f agent_two/docker-compose.yml up -d

