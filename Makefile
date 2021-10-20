run:
	docker run -d --env-file .env --restart always mailing_bot python run.py
