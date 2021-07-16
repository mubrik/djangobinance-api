from django.urls import path, include
from .views import StatusView, AvgPriceView, CurrentPriceView, CandleStickView

urlpatterns = [
    path("avgprice/", AvgPriceView.as_view(), name="get_avg_price"),
    path("currentprice/", CurrentPriceView.as_view(), name="get_current_price"),
    path("candle/", CandleStickView.as_view(), name="get_candle"),
    path("status/", StatusView.as_view(), name="get_status")
]