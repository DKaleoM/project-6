# Makefile for the simple page server.
#

# Nothing to install for this project.
install:
	@(echo 'nothing to install')

restart:
	@(make clean; make install; make start)

start:
	@(docker compose up -d --build)

stop:
	@(docker compose down)

terminal:
	@(docker compose exec -it brevets /bin/bash)

test:
	@(docker compose exec -it brevets ./run_tests.sh)

run:
	@(make restart)

logs:
	@(docker compose logs brevets)

clean:
	@(docker stop $$(docker ps -a -q); docker rm $$(docker ps -a -q))


