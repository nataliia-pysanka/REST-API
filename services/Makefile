cnf ?= .env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

up:
	sudo docker-compose -f docker-compose.yml up --build

down:
	sudo docker-compose -f docker-compose.yml down

init:
	sudo docker-compose --env-file ./.env exec web flask db init
migrate:
	sudo docker-compose --env-file ./.env xec web flask db migrate
upgrade:
	sudo docker-compose --env-file ./.env exec web flask db upgrade
seed:
	sudo docker-compose --env-file ./.env exec web flask seed

drop:
	sudo docker-compose --env-file ./.env exec web flask drop

ps:
	sudo docker-compose ps -a

db:
	sudo docker-compose --env-file ./.env exec db psql -U postgres -c "CREATE DATABASE ${POSTGRES_DB};"

clear:
	sudo docker system prune -a

