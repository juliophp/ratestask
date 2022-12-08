## Startup
1. Run 
```bash 
git clone https://github.com/juliophp/ratestask
```
2. Run 
``` bash
docker compose up
```
3. Launch browser and copy url or run the command below on the terminal
```bash
    curl "http://127.0.0.1:8000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
```



## Challenges
1. Avoiding unneccesary query processing in the application side
2. Benchmarking query efficiency on the database, especially the recursive cte
