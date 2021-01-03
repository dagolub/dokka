### How to start

```
docker-compose up -d --build
```

### How to use
```
curl -F "file=@./data.csv" http://localhost:5000/api/address
curl "http://localhost:5000/api/result?request_id={uuid}"
```

#### RQ Dashboard
```
http://localhost:9181
```

#### Links
https://github.com/RandyDeng/rq-docker-supervisor