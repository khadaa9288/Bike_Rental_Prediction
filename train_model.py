import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("dataset/bike_rental_prediction_dataset_100.csv")

print("First 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns)


# ==========================================
# 2. DEFINE FEATURES AND TARGET
# ==========================================

# Target column
target = "Total_Rental_Price"

# Input features
X = df.drop(target, axis=1)

# Target
y = df[target]


print("\nFeatures:")
print(X.columns)

print("\nTarget:")
print(target)


# ==========================================
# 3. IDENTIFY NUMERICAL AND CATEGORICAL COLUMNS
# ==========================================

categorical_columns = [
    "Season",
    "Weather_Condition",
    "Location",
    "Bike_Type"
]

numerical_columns = [
    "Customer_Age",
    "License_Years",
    "Rental_Days",
    "Distance_KM",
    "Engine_CC",
    "Mileage_KMPL",
    "Previous_Rentals",
    "Customer_Rating",
    "Bike_Age_Years",
    "Rental_Price_Per_Day"
]


# ==========================================
# 4. PREPROCESSING
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),
        (
            "numerical",
            "passthrough",
            numerical_columns
        )
    ]
)


# ==========================================
# 5. CREATE MACHINE LEARNING PIPELINE
# ==========================================

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ]
)


# ==========================================
# 6. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)


# ==========================================
# 7. TRAIN MODEL
# ==========================================

model.fit(X_train, y_train)

print("\nModel training completed successfully!")


# ==========================================
# 8. MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 9. EVALUATE MODEL
# ==========================================

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

r2 = r2_score(y_test, y_pred)


print("\n================================")
print("MODEL EVALUATION")
print("================================")

print("Mean Absolute Error (MAE):", mae)

print("Mean Squared Error (MSE):", mse)

print("R2 Score:", r2)


# ==========================================
# 10. ACTUAL VS PREDICTED
# ==========================================

results = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_pred
})

print("\n================================")
print("ACTUAL VS PREDICTED")
print("================================")

print(results)

# ==========================================
# 11. SAVE TRAINED MODEL
# ==========================================

joblib.dump(model, "bike_rental_model.pkl")

print("\nTrained model saved successfully!")
print("File: bike_rental_model.pkl")