from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import market
from .scripts import json_deserialize

class AvgPriceView(View):
    """ View serves the avg price request """

    http_method_names = ['get']
    
    def get(self, request, *args, **kwargs):

        body_obj = json_deserialize(request.body)
        if body_obj["ok"]:
            response = market.get_price(body_obj["pair"].upper(), "avg")
            return JsonResponse(response)
        else:
            return JsonResponse({"json_error":body_obj["error"]})


class CurrentPriceView(View):
    """ View serves the current price request """

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):

        body_obj = json_deserialize(request.body)
        if body_obj["ok"]:
            response = market.get_price(body_obj["pair"].upper(), "curr")
            return JsonResponse(response)
        else:
            return JsonResponse({"json_error":body_obj["error"]})


class CandleStickView(View):
    """ View serves the kline/candlestick request """

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):

        body_obj = json_deserialize(request.body)
        if body_obj["ok"]:
            del body_obj["ok"]
            body_obj["pair"] = body_obj["pair"].upper()
            response = market.get_price(body_obj, "candle")
            return JsonResponse(response)
        else:
            return JsonResponse({"json_error":body_obj["error"]})


class StatusView(View):
    """ View for checking server status """

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        status = market.get_status()
        return JsonResponse(status)

            