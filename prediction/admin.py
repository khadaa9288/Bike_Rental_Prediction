from django.contrib import admin
from .models import RentalPrediction


@admin.register(RentalPrediction)
class RentalPredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "bike_type",
        "customer_age",
        "rental_days",
        "predicted_price_per_day",
        "total_rental_price",
        "prediction",
        "created_at",
    )

    list_filter = (
        "bike_type",
        "season",
        "weather_condition",
        "location",
        "created_at",
    )

    search_fields = (
        "user__username",
        "bike_type",
        "location",
    )

    ordering = (
        "-created_at",
    )