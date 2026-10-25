from django.urls import include, path

urlpatterns = [
    path("", include("assignment.urls")),
]
