# How to test

Run vertica in docker

```shell
docker run -p 5433:5433 jbfavre/vertica:latest 
```

Install dependencies

```shell
python3 -m venv .venv
./.venv/bin/activate
pip install -r requirements.txt
```

Create table and generate test data

```shell
main.py create
main.py generate
```

Script will generate 100 000 000 entries. Run bench to fetch info filtered by movie id and ordered by user_id and timestamp

```shell
main.py bench --movie_id ttKa0wwnZYkd
```