up:
	docker-compose -f docker-compose.yml up --build --remove-orphans --detach
down:
	docker-compose -f docker-compose.yml down --rmi local --remove-orphans
sert:
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem

