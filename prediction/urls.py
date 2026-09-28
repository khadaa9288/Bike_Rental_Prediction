from django.urls import path
from . import views


urlpatterns = [
    path("", views.predict, name="predict"),
    path("history/", views.history, name="history"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]