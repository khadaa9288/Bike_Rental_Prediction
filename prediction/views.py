from django.shortcuts import render
from django.conf import settings
import pandas as pd
import joblib
import os

from .forms import PredictionForm


MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "prediction",
    "bike_rental_model.pkl"
)


def predict(request):
    prediction = None

    if request.method == "POST":
        form = PredictionForm(request.POST)

        if form.is_valid():

            model = joblib.load(MODEL_PATH)

            input_data = pd.DataFrame([{
                "Customer_Age": form.cleaned_data["customer_age"],
                "License_Years": form.cleaned_data["license_years"],
                "Rental_Days": form.cleaned_data["rental_days"],
                "Distance_KM": form.cleaned_data["distance_km"],
                "Engine_CC": form.cleaned_data["engine_cc"],
                "Mileage_KMPL": form.cleaned_data["mileage_kmpl"],
                "Previous_Rentals": form.cleaned_data["previous_rentals"],
                "Customer_Rating": form.cleaned_data["customer_rating"],
                "Bike_Age_Years": form.cleaned_data["bike_age_years"],
                "Season": form.cleaned_data["season"],
                "Weather_Condition": form.cleaned_data["weather_condition"],
                "Location": form.cleaned_data["location"],
                "Bike_Type": form.cleaned_data["bike_type"],
                "Rental_Price_Per_Day": form.cleaned_data["rental_price_per_day"],
            }])

            result = model.predict(input_data)[0]

            prediction = round(max(0, float(result)), 2)

    else:
        form = PredictionForm()

    return render(
        request,
        "prediction/predict.html",
        {
            "form": form,
            "prediction": prediction,
        }
    )