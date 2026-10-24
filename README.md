# Scikit-learn test

## What you'll learn

In this project, we'll use the California Housing dataset to learn:

1. Loading a real dataset
2. Splitting data into training and testing sets
3. Creating a baseline model
4. Building a machine learning pipeline
5. Evaluating models with cross-validation
6. Tuning hyperparameters with `RandomizedSearchCV`
7. Evaluating the final model using MAE and RMSE

---

## 1. Setup

Install the required packages:

```bash
pip install scikit-learn pandas
```

The dataset download requires an internet connection the first time.

## 2. Load the dataset

```python
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing(as_frame=True)

X = housing.data
y = housing.target

print("Dataset shape:", X.shape)
print("Features:", X.columns.tolist())
print(X.head())
print(y.head())
```

### Understanding the data

- `X`: input features used to make predictions.
- `y`: target values that the model learns to predict.
- The dataset contains eight features describing California housing areas.
- Target values are expressed in units of $100,000.

For example, a target value of `2.0` corresponds to $200,000.

## 3. Split the data

We keep a separate test set to estimate how well the model performs on unseen examples.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
```

- `test_size=0.2`: reserve 20% of observations for testing.
- `random_state=42`: make the split reproducible.

**Important:** Do not use the test set to select models or tune hyperparameters.

## 4. Create a baseline model

A baseline gives us a simple benchmark to beat.

```python
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error

baseline = DummyRegressor(strategy="median")

baseline.fit(X_train, y_train)

baseline_predictions = baseline.predict(X_test)

baseline_mae = mean_absolute_error(
    y_test,
    baseline_predictions
)

print("Baseline MAE:", round(baseline_mae, 3))
```

`DummyRegressor` ignores the input features and predicts the median target value from the training data.

A useful model should perform better than this simple baseline.

## 5. Build a pipeline with Linear Regression

A pipeline combines data transformations and a model into one reusable object.

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

linear_model = make_pipeline(
    StandardScaler(),
    LinearRegression()
)

linear_model.fit(X_train, y_train)

linear_predictions = linear_model.predict(X_test)

linear_mae = mean_absolute_error(
    y_test,
    linear_predictions
)

print("Linear Regression MAE:", round(linear_mae, 3))
```

### What does `StandardScaler` do?

It standardizes each feature using statistics learned from the training data.

A pipeline ensures the scaler is fitted on the appropriate training data when used with cross-validation. This helps prevent data leakage.

## 6. Evaluate using cross-validation

A single validation split can give a misleading estimate of model performance.

Cross-validation evaluates the model on multiple folds of the training data.

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(
    linear_model,
    X_train,
    y_train,
    cv=5,
    scoring="neg_mean_absolute_error"
)

mae_scores = -scores

print("MAE for each fold:", mae_scores.round(3))
print("Average CV MAE:", round(mae_scores.mean(), 3))
print("Standard deviation:", round(mae_scores.std(), 3))
```

Scikit-learn returns negative values for loss metrics when using its scoring interface because higher scores are defined as better. We multiply by `-1` to display positive MAE values.

Interpretation:

- **Average CV MAE:** average absolute prediction error across folds.
- **Standard deviation:** how much the error varies across folds.
- Lower MAE generally indicates better predictions.

## 7. Tune a Random Forest

A Random Forest combines predictions from multiple decision trees.

We'll use `RandomizedSearchCV` to evaluate a selection of hyperparameter combinations.

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

forest = RandomForestRegressor(
    random_state=42,
    n_jobs=1
)

pipeline = make_pipeline(forest)

param_distributions = {
    "randomforestregressor__n_estimators": [100, 200],
    "randomforestregressor__max_depth": [10, 20, None],
    "randomforestregressor__min_samples_leaf": [1, 2, 4],
    "randomforestregressor__max_features": [0.7, 1.0]
}

search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_distributions,
    n_iter=8,
    cv=3,
    scoring="neg_mean_absolute_error",
    random_state=42,
    n_jobs=-1,
    verbose=1
)

search.fit(X_train, y_train)

print("Best parameters:")
print(search.best_params_)

print("Best CV MAE:", round(-search.best_score_, 3))
```

### Understanding the hyperparameters

- `n_estimators`: number of trees in the forest.
- `max_depth`: maximum depth allowed for each tree.
- `min_samples_leaf`: minimum number of training examples required at a leaf.
- `max_features`: number or proportion of features considered when splitting.

The double underscore in `randomforestregressor__max_depth` allows us to configure the Random Forest inside the pipeline.

`n_iter=8` means the search evaluates eight sampled combinations, each using three-fold cross-validation. This is a demonstration, not an exhaustive search.

## 8. Evaluate the final model

After tuning, evaluate the selected model on the held-out test set.

```python
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error
)

best_model = search.best_estimator_

test_predictions = best_model.predict(X_test)

mae = mean_absolute_error(y_test, test_predictions)
rmse = root_mean_squared_error(y_test, test_predictions)

print(f"Test MAE: ${mae * 100_000:,.0f}")
print(f"Test RMSE: ${rmse * 100_000:,.0f}")
```

If your scikit-learn version does not support `root_mean_squared_error`, calculate RMSE like this:

```python
from sklearn.metrics import mean_squared_error

rmse = mean_squared_error(
    y_test,
    test_predictions
) ** 0.5
```

### MAE vs. RMSE

**Mean Absolute Error (MAE)** is the average absolute difference between predictions and actual values.

**Root Mean Squared Error (RMSE)** squares the errors before averaging them and taking the square root. This gives larger errors more influence.

Both metrics are in the same units as the target. Here, multiplying by 100,000 converts them to dollars.

Lower values indicate better predictions, but metrics should always be interpreted in context.

## 9. Important lessons

1. Establish a baseline before using complex models.
2. Keep test data separate from model selection.
3. Use pipelines to combine preprocessing and modeling.
4. Use cross-validation to estimate performance more robustly.
5. Tune hyperparameters using training data only.
6. Evaluate the selected model on the test set after tuning.
7. More complex models are not necessarily better.

## 10. Limitations

The California Housing dataset is a historical educational dataset. Its target values are capped, and its observations should not be treated as current property valuations.

Model performance can also vary with the dataset version, split, and hyperparameters.

## Project workflow summary

```text
Load dataset
    ↓
Separate features and target
    ↓
Split training and test data
    ↓
Evaluate baseline
    ↓
Build pipeline
    ↓
Run cross-validation
    ↓
Tune hyperparameters
    ↓
Evaluate on held-out test data
```

## Next steps

After completing this project, try:

- Classification with logistic regression
- Feature engineering
- Saving and loading a model with `joblib`
- Understanding decision trees and random forests
- Building a small prediction application
