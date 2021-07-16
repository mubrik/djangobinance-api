from binance.spot import Spot
from binance.error import ClientError, ServerError
from decouple import config
import decimal as dec

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
        self.instance = Spot(self.key, self.secret, base_url=self.uri)

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
        kline_data = self.instance.klines(symbol=pair, interval=interval, limit=main_limit)
        result = []
        for candlestick in kline_data:
            new_dict = {
                "open_time": candlestick[0],
                "open": candlestick[1],
                "high": candlestick[2],
                "low": candlestick[3],
                "close": candlestick[4],
                "volume": candlestick[5],
                "close_time": candlestick[6],
                "trades": candlestick[8],
            }
            result.append(new_dict)
        return {
            "pair": pair,
            "data": result
        }

    def get_avg_price(self, pair):
        avg_price = self.instance.avg_price(pair)
        return avg_price

    def get_latest_price(self, pair):
        price = self.instance.ticker_price(pair)
        return price

    def get_status(self):
        status = self.instance.system_status()
        return status

    def ping_server(self):
        status = self.instance.ping()
        return status

market = MarketFetch(api, key, base_uri)