run:
	docker-compose up -d

stop:
	docker-compose down

init_cluster:
	sh ./init.sh

seed_db:
	export PYTHONPATH="${PYTHONPATH}:${PWD}/../.." \
	&& python -m src.seed_db

run_benchmarks:
	export PYTHONPATH="${PYTHONPATH}:${PWD}/../.." \
	&& python -m src.main