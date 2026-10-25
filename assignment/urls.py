from django.urls import path

from assignment import views

urlpatterns = [
    path("", views.cost_estimate, name="cost"),
]
