from django.db import models
from django.contrib.auth.models import User


class RentalPrediction(models.Model):

    # ============================================================
    # USER
    # ============================================================

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rental_predictions",
        null=True,
        blank=True,
    )

    # ============================================================
    # INPUT DATA
    # ============================================================

    bike_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    customer_age = models.IntegerField(
        null=True,
        blank=True,
    )

    rental_days = models.IntegerField(
        null=True,
        blank=True,
    )

    season = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    weather_condition = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    distance_km = models.FloatField(
        null=True,
        blank=True,
    )

    mileage_kmpl = models.FloatField(
        null=True,
        blank=True,
    )

    customer_rating = models.FloatField(
        null=True,
        blank=True,
    )

    # ============================================================
    # PREDICTION RESULT
    # ============================================================

    prediction = models.FloatField(
        null=True,
        blank=True,
    )

    predicted_price_per_day = models.FloatField(
        null=True,
        blank=True,
    )

    total_rental_price = models.FloatField(
        null=True,
        blank=True,
    )

    # ============================================================
    # TIMESTAMP
    # ============================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # ============================================================
    # META
    # ============================================================

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        username = self.user.username if self.user else "Guest"
        return f"{username} - {self.prediction}"