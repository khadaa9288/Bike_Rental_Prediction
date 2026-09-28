from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

import pandas as pd
import joblib
import os

from .forms import PredictionForm
from .models import RentalPrediction


# ============================================================
# MACHINE LEARNING MODEL PATH
# ============================================================

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "prediction",
    "bike_rental_model.pkl"
)


# ============================================================
# HOME PAGE
# ============================================================

def home(request):
    return render(
        request,
        "home.html"
    )


# ============================================================
# BIKE RENTAL PREDICTION
# ============================================================

@login_required(login_url="/accounts/login/")
def predict(request):

    prediction = None
    total_rental_price = None

    # --------------------------------------------------------
    # POST REQUEST
    # --------------------------------------------------------

    if request.method == "POST":

        form = PredictionForm(request.POST)

        # ----------------------------------------------------
        # VALIDATE FORM
        # ----------------------------------------------------

        if form.is_valid():

            # =================================================
            # LOAD MACHINE LEARNING MODEL
            # =================================================

            try:

                model = joblib.load(
                    MODEL_PATH
                )

                print("==========================================")
                print("ML MODEL LOADED SUCCESSFULLY")
                print("MODEL PATH:", MODEL_PATH)
                print("==========================================")

            except Exception as e:

                print("==========================================")
                print("MODEL LOADING ERROR")
                print(e)
                print("==========================================")

                return render(
                    request,
                    "predict.html",
                    {
                        "form": form,
                        "prediction": None,
                        "total_rental_price": None,
                        "error": (
                            "Unable to load the machine "
                            "learning model: "
                            + str(e)
                        ),
                    }
                )

            # =================================================
            # PREPARE ML INPUT
            # =================================================

            input_data = pd.DataFrame([{

                "Customer_Age":
                    form.cleaned_data["customer_age"],

                "License_Years":
                    form.cleaned_data["license_years"],

                "Rental_Days":
                    form.cleaned_data["rental_days"],

                "Distance_KM":
                    form.cleaned_data["distance_km"],

                "Engine_CC":
                    form.cleaned_data["engine_cc"],

                "Mileage_KMPL":
                    form.cleaned_data["mileage_kmpl"],

                "Previous_Rentals":
                    form.cleaned_data["previous_rentals"],

                "Customer_Rating":
                    form.cleaned_data["customer_rating"],

                "Bike_Age_Years":
                    form.cleaned_data["bike_age_years"],

                "Season":
                    form.cleaned_data["season"],

                "Weather_Condition":
                    form.cleaned_data["weather_condition"],

                "Location":
                    form.cleaned_data["location"],

                "Bike_Type":
                    form.cleaned_data["bike_type"],

                "Rental_Price_Per_Day":
                    form.cleaned_data["rental_price_per_day"],

            }])

            # =================================================
            # DEBUG - SHOW INPUT IN TERMINAL
            # =================================================

            print("==========================================")
            print("MODEL INPUT")
            print(input_data)
            print("==========================================")

            # =================================================
            # MAKE ML PREDICTION
            # =================================================

            try:

                result = model.predict(
                    input_data
                )[0]

                # Convert prediction to float
                prediction = float(result)

                # Prevent negative prediction
                prediction = max(
                    0,
                    prediction
                )

                # Round to 2 decimal places
                prediction = round(
                    prediction,
                    2
                )

                print("==========================================")
                print("RAW MODEL RESULT:", result)
                print("FINAL PREDICTION:", prediction)
                print("==========================================")

            except Exception as e:

                print("==========================================")
                print("PREDICTION ERROR")
                print(e)
                print("==========================================")

                return render(
                    request,
                    "predict.html",
                    {
                        "form": form,
                        "prediction": None,
                        "total_rental_price": None,
                        "error": (
                            "Prediction failed: "
                            + str(e)
                        ),
                    }
                )

            # =================================================
            # CALCULATE TOTAL RENTAL PRICE
            # =================================================

            rental_days = form.cleaned_data[
                "rental_days"
            ]

            total_rental_price = round(
                prediction * rental_days,
                2
            )

            print("==========================================")
            print("RENTAL DAYS:", rental_days)
            print(
                "PRICE PER DAY:",
                prediction
            )
            print(
                "TOTAL RENTAL PRICE:",
                total_rental_price
            )
            print("==========================================")

            # =================================================
            # SAVE PREDICTION TO DATABASE
            # =================================================

            try:

                RentalPrediction.objects.create(

                    # ------------------------------
                    # USER
                    # ------------------------------

                    user=request.user,

                    # ------------------------------
                    # INPUT FIELDS THAT EXIST
                    # IN YOUR MODEL
                    # ------------------------------

                    bike_type=form.cleaned_data[
                        "bike_type"
                    ],

                    customer_age=form.cleaned_data[
                        "customer_age"
                    ],

                    rental_days=form.cleaned_data[
                        "rental_days"
                    ],

                    season=form.cleaned_data[
                        "season"
                    ],

                    weather_condition=form.cleaned_data[
                        "weather_condition"
                    ],

                    location=form.cleaned_data[
                        "location"
                    ],

                    distance_km=form.cleaned_data[
                        "distance_km"
                    ],

                    mileage_kmpl=form.cleaned_data[
                        "mileage_kmpl"
                    ],

                    customer_rating=form.cleaned_data[
                        "customer_rating"
                    ],

                    # ------------------------------
                    # PREDICTION RESULT
                    # ------------------------------

                    prediction=prediction,

                    predicted_price_per_day=prediction,

                    total_rental_price=total_rental_price,

                )

                print("==========================================")
                print("PREDICTION SAVED SUCCESSFULLY")
                print("USER:", request.user.username)
                print("==========================================")

            except Exception as e:

                print("==========================================")
                print("DATABASE SAVE ERROR")
                print(e)
                print("==========================================")

                return render(
                    request,
                    "predict.html",
                    {
                        "form": form,
                        "prediction": prediction,
                        "total_rental_price": total_rental_price,
                        "error": (
                            "Prediction was calculated, "
                            "but could not be saved: "
                            + str(e)
                        ),
                    }
                )

            # =================================================
            # SHOW RESULT
            # =================================================

            return render(
                request,
                "predict.html",
                {
                    "form": form,
                    "prediction": prediction,
                    "total_rental_price": total_rental_price,
                    "success": True,
                }
            )

        else:

            # =================================================
            # FORM VALIDATION ERROR
            # =================================================

            print("==========================================")
            print("FORM VALIDATION ERROR")
            print(form.errors)
            print("==========================================")

    else:

        # =====================================================
        # GET REQUEST
        # =====================================================

        form = PredictionForm()

    # ========================================================
    # RENDER PAGE
    # ========================================================

    return render(
        request,
        "predict.html",
        {
            "form": form,
            "prediction": prediction,
            "total_rental_price": total_rental_price,
        }
    )


# ============================================================
# PREDICTION HISTORY
# ============================================================

@login_required(login_url="/accounts/login/")
def history(request):

    predictions = RentalPrediction.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "history.html",
        {
            "predictions": predictions
        }
    )


# ============================================================
# CUSTOM ADMIN DASHBOARD
# ============================================================

@login_required(login_url="/accounts/login/")
def admin_dashboard(request):

    # --------------------------------------------------------
    # ONLY SUPERUSER CAN ACCESS
    # --------------------------------------------------------

    if not request.user.is_superuser:

        return redirect(
            "home"
        )

    # --------------------------------------------------------
    # GET ALL PREDICTIONS
    # --------------------------------------------------------

    predictions = RentalPrediction.objects.select_related(
        "user"
    ).order_by(
        "-created_at"
    )

    # --------------------------------------------------------
    # TOTAL PREDICTIONS
    # --------------------------------------------------------

    total_predictions = RentalPrediction.objects.count()

    # --------------------------------------------------------
    # TOTAL USERS WHO MADE PREDICTIONS
    # --------------------------------------------------------

    total_users = RentalPrediction.objects.values(
        "user"
    ).distinct().count()

    # --------------------------------------------------------
    # RENDER ADMIN DASHBOARD
    # --------------------------------------------------------

    return render(
        request,
        "admin_dashboard.html",
        {
            "predictions": predictions,
            "total_predictions": total_predictions,
            "total_users": total_users,
        }
    )