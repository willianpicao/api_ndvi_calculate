# Delete all containers using the following command:
#docker rm -f $(docker ps -a -q)
docker rm -f api_ndvi_calculate-redis_1
docker rm -f api_ndvi_calculate-webapp_1
docker rm -f api_ndvi_calculate-controller_1
docker rm  -f api_ndvi_calculate-worker-math_1
docker rm -f api_ndvi_calculate-gateway_1
# Delete all containers using the following command:
#docker volume rm $(docker volume ls -q)
# docker image prune -a
docker image rm api_ndvi_calculate-redis
docker image rm api_ndvi_calculate-webapp
docker image rm api_ndvi_calculate-controller
docker image rm api_ndvi_calculate-worker-math
docker image rm api_ndvi_calculate-gateway
