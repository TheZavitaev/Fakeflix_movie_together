[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![workflow](https://github.com/medik88/ugc_sprint_2/workflows/ugc_deploy/badge.svg)](https://github.com/medik88/ugc_sprint_2/actions)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

# Проектная работа 9 спринта

# перед пушем делаем `make linters` !

## API

Сервис перенаправляет запросы от пользователя в kafka. Сервис идентифицирует пользователя по полю user_id, который берется из JWT токена, без проверки его подписи. В системе присутствует **Gateway**, который роутит все входящие запросы и проверяет подпись токенов. Все нижестоящие сервисы доверяют токенам в запросах.

## How to run locally

### Run kafka in docker

```shell
docker-compose up kafka zookeeper api
```

Create topic `movie_progress`. You can use this script

```shell
cd utils
python kafka_create_topic.py
```

## Run api locally

Set ENV variable

```shell
MONGO_DSN: mongodb://root:pass123@localhost:27017
```

```shell
cd api
pip install -r requirements.txt
cd src
python main.py
```

### Run mongodb in docker

docker-compose up mongo mongo-express

### Run postman tests

Install [newman tool](https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/) to run postman tests from terminal.

Run tests

```shell
newman run tests/postman/UGCAPI.postman_collection.json
```


## CI
The artifact loading mechanism is built into the continuous integration process.
At the bottom of the workflow summary page, there is a dedicated section for artifacts.

There is a trashcan icon that can be used to delete the artifact. This icon will only appear for users who have 
write permissions to the repository.

The size of the artifact is denoted in bytes. The displayed artifact size denotes the raw uploaded artifact size 
(the sum of all the individual files uploaded during the workflow run for the artifact), not the compressed size. 
When you click to download an artifact from the summary page, a compressed zip is created with all the contents of 
the artifact and the size of the zip that you download may differ significantly from the displayed size. 
Billing is based on the raw uploaded size and not the size of the zip.

# How to run:
## For m1:
### install confluent_kafka
1) `brew install librdkafka`
2) `C_INCLUDE_PATH=/opt/homebrew/Cellar/librdkafka/1.7.0/include LIBRARY_PATH=/opt/homebrew/Cellar/librdkafka/1.7.0/lib pip install confluent_kafka`

### clickhouse
Officially nothing, but uncomment `image: kolsys/clickhouse-server:21.3.15.4-lts-arm` in docker-compose ;)
