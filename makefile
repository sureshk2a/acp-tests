.PHONY: up down

down:
	docker-compose -f router_agent/docker-compose.yml down
	timeout 10
	docker-compose -f agent_one/docker-compose.yml down
	timeout 10
	docker-compose -f agent_two/docker-compose.yml down

up: down
	docker-compose -f router_agent/docker-compose.yml up -d
	timeout 10
	docker-compose -f agent_one/docker-compose.yml up -d
	timeout 10
	docker-compose -f agent_two/docker-compose.yml up -d