# 🚲 Bike Rental Price Prediction System

A Machine Learning based web application that predicts the estimated rental price of a bike based on customer, bike, rental, and environmental information.

The trained Machine Learning model is integrated with a Django web application to provide predictions through an easy-to-use web interface.

---

## 📌 Project Overview

The Bike Rental Price Prediction System uses Machine Learning to estimate the rental price for a bike.

The user enters information such as:

- Customer Age
- License Years
- Rental Days
- Distance KM
- Engine CC
- Mileage KMPL
- Previous Rentals
- Customer Rating
- Bike Age
- Season
- Weather Condition
- Location
- Bike Type
- Rental Price Per Day

The trained model processes these inputs and generates an estimated rental price.

---

## 🎯 Objectives

- Predict bike rental prices using Machine Learning.
- Build a user-friendly web interface.
- Integrate the trained ML model with Django.
- Allow users to enter rental information.
- Display the predicted rental price instantly.
- Demonstrate practical use of Machine Learning in a web application.

---

## 🛠️ Technologies Used

### Programming Language

- Python

### Machine Learning

- Scikit-learn
- Pandas
- NumPy
- Joblib

### Web Development

- Django
- HTML
- CSS
- Bootstrap
- Bootstrap Icons

### Development Tools

- Visual Studio Code
- PowerShell
- Python Virtual Environment

---

## 🤖 Machine Learning

The project uses a trained Machine Learning regression model to predict rental prices.

### Input Features

1. Customer Age
2. License Years
3. Rental Days
4. Distance KM
5. Engine CC
6. Mileage KMPL
7. Previous Rentals
8. Customer Rating
9. Bike Age Years
10. Season
11. Weather Condition
12. Location
13. Bike Type
14. Rental Price Per Day

### Output

The model produces:

**Predicted Bike Rental Price**

---

## 🔄 Project Flow

```text
User
  ↓
Django Web Interface
  ↓
Enter Rental Information
  ↓
Django Form Validation
  ↓
Load Trained ML Model
  ↓
Prepare Input Data
  ↓
Machine Learning Model
  ↓
Price Prediction
  ↓
Display Predicted Rental Price