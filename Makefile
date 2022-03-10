up:
	docker-compose -f docker-compose.yml up --build --remove-orphans --detach
down:
	docker-compose -f docker-compose.yml down --rmi local --remove-orphans
