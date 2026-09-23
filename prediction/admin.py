from django.contrib import admin
from .models import RentalPrediction


@admin.register(RentalPrediction)
class RentalPredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "bike_type",
        "customer_age",
        "rental_days",
        "predicted_price_per_day",
        "total_rental_price",
        "created_at",
    )

    list_filter = (
        "bike_type",
        "season",
        "weather_condition",
        "location",
    )

    search_fields = (
        "bike_type",
        "location",
        "season",
    )

    ordering = ("-created_at",)