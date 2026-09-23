from django.db import models


class RentalPrediction(models.Model):

    # Customer information
    customer_age = models.PositiveIntegerField()
    license_years = models.PositiveIntegerField()

    # Rental information
    rental_days = models.PositiveIntegerField()
    distance_km = models.FloatField()

    # Bike information
    engine_cc = models.PositiveIntegerField()
    mileage_kmpl = models.FloatField()
    bike_age_years = models.PositiveIntegerField()

    # Customer history
    previous_rentals = models.PositiveIntegerField()
    customer_rating = models.FloatField()

    # Categorical information
    season = models.CharField(max_length=20)
    weather_condition = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    bike_type = models.CharField(max_length=50)

    # Machine learning prediction
    predicted_price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_rental_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Date/time
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bike_type} - ₹{self.predicted_price_per_day}/day"