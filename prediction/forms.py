from django import forms


class PredictionForm(forms.Form):

    customer_age = forms.IntegerField(
        label="Customer Age",
        min_value=18,
        max_value=100
    )

    license_years = forms.IntegerField(
        label="License Years",
        min_value=0,
        max_value=80
    )

    rental_days = forms.IntegerField(
        label="Rental Days",
        min_value=1,
        max_value=365
    )

    distance_km = forms.FloatField(
        label="Distance (KM)",
        min_value=0
    )

    engine_cc = forms.IntegerField(
        label="Engine CC",
        min_value=50
    )

    mileage_kmpl = forms.FloatField(
        label="Mileage (KMPL)",
        min_value=1
    )

    previous_rentals = forms.IntegerField(
        label="Previous Rentals",
        min_value=0
    )

    customer_rating = forms.FloatField(
        label="Customer Rating",
        min_value=0,
        max_value=5
    )

    bike_age_years = forms.FloatField(
        label="Bike Age (Years)",
        min_value=0
    )

    season = forms.ChoiceField(
        label="Season",
        choices=[
            ("Spring", "Spring"),
            ("Summer", "Summer"),
            ("Autumn", "Autumn"),
            ("Winter", "Winter"),
        ]
    )

    weather_condition = forms.ChoiceField(
        label="Weather Condition",
        choices=[
            ("Clear", "Clear"),
            ("Cloudy", "Cloudy"),
            ("Rainy", "Rainy"),
            ("Hot", "Hot"),
        ]
    )

    location = forms.ChoiceField(
        label="Location",
        choices=[
            ("City Center", "City Center"),
            ("University Area", "University Area"),
            ("Airport", "Airport"),
            ("Market Area", "Market Area"),
        ]
    )

    bike_type = forms.ChoiceField(
        label="Bike Type",
        choices=[
            ("Scooter", "Scooter"),
            ("Standard Bike", "Standard Bike"),
            ("Electric Bike", "Electric Bike"),
            ("Sports Bike", "Sports Bike"),
        ]
    )

    rental_price_per_day = forms.FloatField(
        label="Rental Price Per Day",
        min_value=0
    )