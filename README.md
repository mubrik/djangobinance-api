# djangobinance-api

Project using Binance API to fetch a symbol market data from binance

1. install requirements.txt
2. start django server
3. send GET request with JSON body object 
{
    "pair" : "btcusdt" #required
} to server links:
/get/avgprice/
/get/currentprice/
4. send GET request with JSON body object 
{
    "pair" : "btcusdt" #required
    "interval": "1h"  # 1m 5m
    "limit": 8 # max 10
} to server link:
/get/candle/ 
5. check server status send GET request to /get/status/