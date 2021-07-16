from binance.spot import Spot
from binance.error import ClientError, ServerError
from decouple import config
import decimal as dec
import datetime

# local context for decimal
dec.getcontext().rounding = "ROUND_HALF_UP"

# import environment variables
api = config("BINANCE_KEY")
key = config("BINANCE_SECRET")
base_uri = config("BINANCE_BASE_URI")


class MarketFetch():

    """ class handles fetching and serving of data from binance apis """

    def __init__(self, key, secret, url):
        self.key = key
        self.secret = secret
        self.uri = url
        self.make_client()

    def make_client(self):
        self.binance = Spot(self.key, self.secret, base_url=self.uri)

    def get_price(self, pair, param):
        try:
            if param == "avg":
                result = self.get_avg_price(pair)
                return result
            elif param == "curr":
                result = self.get_latest_price(pair)
                return result
            elif param == "candle":
                result = self.get_kline_candlestick(**pair)
                return result
            
        except ClientError as error:
            status_code, err_code, err_msg, response = error.args
            return {
                "http_status": status_code,
                "error_code": err_code,
                "error": err_msg
            }

        except ServerError as error:
            return {
                "http_status": 500,
                "error_code": 500,
                "error": "server unreachable, check server status"
            }

    def get_kline_candlestick(self, pair, interval="1h", limit=2):
        # limit amount of candle sticks
        main_limit = limit if limit < 10 else 10
        kline_data = self.binance.klines(symbol=pair, interval=interval, limit=main_limit)
        # format candlestick
        result = []
        for candlestick in kline_data:
            open_time = self.format_time(candlestick[0])
            close_time = self.format_time(candlestick[6])

            new_dict = {
                "open_time": open_time,
                "open": candlestick[1],
                "high": candlestick[2],
                "low": candlestick[3],
                "close": candlestick[4],
                "volume": candlestick[5],
                "close_time": close_time,
                "trades": candlestick[8],
            }
            result.append(new_dict)
        return {
            "pair": pair,
            "data": result
        }

    def get_avg_price(self, pair):
        avg_price = self.binance.avg_price(pair)
        return avg_price

    def get_latest_price(self, pair):
        price = self.binance.ticker_price(pair)
        return price

    def get_status(self):
        status = self.binance.system_status()
        return status

    def get_server_time(self):
        obj = self.binance.time()
        time = self.format_time(obj["serverTime"])
        return {
            "time": time
        }

    def format_time(self, server_time):
        time = str(server_time)[0:10]
        res = datetime.datetime.fromtimestamp(int(time)).strftime("%a, %d %b %Y %H:%M:%S %p")
        return res

    def ping_server(self):
        status = self.binance.ping()
        return status

market = MarketFetch(api, key, base_uri)