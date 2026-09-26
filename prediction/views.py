from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

import pandas as pd
import joblib
import os

from .forms import PredictionForm
from .models import RentalPrediction


MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "prediction",
    "bike_rental_model.pkl"
)


# =========================
# HOME PAGE
# =========================

def home(request):
    return render(request, "home.html")


# =========================
# BIKE RENTAL PREDICTION
# =========================

@login_required(login_url="/accounts/login/")
def predict(request):

    prediction = None

    if request.method == "POST":

        form = PredictionForm(request.POST)

        if form.is_valid():

            # Load trained machine learning model
            model = joblib.load(MODEL_PATH)

            # Prepare input data
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
                "Rental_Price_Per_Day": form.cleaned_data[
                    "rental_price_per_day"
                ],
            }])

            # Make prediction
            result = model.predict(input_data)[0]

            # Prevent negative prediction
            prediction = round(
                max(0, float(result)),
                2
            )

            # Calculate total rental price
            rental_days = form.cleaned_data["rental_days"]

            total_rental_price = round(
                prediction * rental_days,
                2
            )

            # Save complete prediction
            RentalPrediction.objects.create(
                user=request.user,
                    
                customer_age=form.cleaned_data["customer_age"],
                license_years=form.cleaned_data["license_years"],
                rental_days=form.cleaned_data["rental_days"],
                distance_km=form.cleaned_data["distance_km"],
                engine_cc=form.cleaned_data["engine_cc"],
                mileage_kmpl=form.cleaned_data["mileage_kmpl"],
                bike_age_years=form.cleaned_data["bike_age_years"],
                previous_rentals=form.cleaned_data["previous_rentals"],
                customer_rating=form.cleaned_data["customer_rating"],
                season=form.cleaned_data["season"],
                weather_condition=form.cleaned_data["weather_condition"],
                location=form.cleaned_data["location"],
                bike_type=form.cleaned_data["bike_type"],
                predicted_price_per_day=prediction,
                total_rental_price=total_rental_price,
            )

    else:

        form = PredictionForm()

    return render(
        request,
        "predict.html",
        {
        "form": form,
        "prediction": prediction,
        "total_rental_price": total_rental_price
        if prediction is not None else None,
        }
    )


# =========================
# ADMIN DASHBOARD
# =========================

@login_required(login_url="/accounts/login/")
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect("home")

    return render(
        request,
        "admin_dashboard.html"
    )