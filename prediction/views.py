from django.shortcuts import render, redirect
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import pandas as pd
import joblib
import os

from .forms import PredictionForm
from .models import PredictionHistory


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
# LOGIN
# =========================

def user_login(request):

    if request.user.is_authenticated:

        if request.user.is_staff or request.user.is_superuser:
            return redirect("/admin/")

        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Admin / Superuser
            if user.is_staff or user.is_superuser:
                return redirect("/admin/")

            # Normal customer
            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


# =========================
# LOGOUT
# =========================

def user_logout(request):

    logout(request)

    return redirect("home")


# =========================
# BIKE RENTAL PREDICTION
# =========================

@login_required(login_url="/login/")
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
                "Rental_Price_Per_Day": form.cleaned_data[
                    "rental_price_per_day"
                ],
            }])

            result = model.predict(input_data)[0]

            prediction = round(
                max(0, float(result)),
                2
            )

            # Save prediction for logged-in user
            PredictionHistory.objects.create(
                user=request.user,
                prediction=prediction
            )

    else:

        form = PredictionForm()

    return render(
        request,
        "predict.html",
        {
            "form": form,
            "prediction": prediction,
        }
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Admin / Superuser
            if user.is_superuser:
                return redirect("admin_dashboard")

            # Normal User
            return redirect("home")

        else:
            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username or password."
                }
            )

    return render(request, "login.html")

@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect("home")

    return render(
        request,
        "admin_dashboard.html"
    )