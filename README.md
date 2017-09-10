
docker-compose build
docker-compose up
docker-compose down


## Create database
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET localhost:5000/create-database

curl -X GET localhost:5000/products/pending