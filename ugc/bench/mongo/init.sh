docker-compose exec mongocfg1 sh -c "mongo < /scripts/init_config_server.js"
docker-compose exec mongors1n1 sh -c "mongo < /scripts/init_shard_01.js"
docker-compose exec mongors2n1 sh -c "mongo  < /scripts/init_shard_02.js"

echo "Waiting..."
sleep 30

docker-compose exec mongos1 sh -c "mongo < /scripts/init_router.js"
docker-compose exec mongos1 sh -c "mongo < /scripts/init_db.js"