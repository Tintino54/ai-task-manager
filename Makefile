.PHONY: server stop logs

server:
	docker compose up --build -d
	docker compose exec ollama ollama pull qwen3.5:4b

stop:
	docker compose down

logs:
	docker compose logs -f app ollama