from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Home
    path(
        "",
        TemplateView.as_view(template_name="home.html"),
        name="home",
    ),

    # Accounts
    path("accounts/", include("accounts.urls")),

    # Prediction
    path("prediction/", include("prediction.urls")),
]