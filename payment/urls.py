from django.urls import path
from django.views.generic import TemplateView
from payment import views as pv


urlpatterns = [
    path('', pv.index_view, name="index"),
    path('checkout/', pv.checkout_view, name="checkout"),
    path("success/", pv.success_view, name="success"),
    path("failed/", pv.failed_view, name="fail"),
    path("cancle/", pv.cancle_view, name="cancle"),
]
