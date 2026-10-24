from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import root_mean_squared_error

housing = fetch_california_housing(as_frame=True)

X = housing.data
y = housing.target

print("Dataset shape:", X.shape)
print("\nFeatures:")
print(X.columns.tolist())
print("\nFirst five rows:")
print(X.head())
print("\nTarget values:")
print(y.head())



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

baseline = DummyRegressor(strategy="median")

linear_model = make_pipeline(
    StandardScaler(),
    LinearRegression()
)

baseline.fit(X_train, y_train)
linear_model.fit(X_train, y_train)

baseline_pred = baseline.predict(X_test)
linear_pred = linear_model.predict(X_test)

print("Baseline MAE:", round(
    mean_absolute_error(y_test, baseline_pred), 3
))
print("Linear regression MAE:", round(
    mean_absolute_error(y_test, linear_pred), 3
))



scores = cross_val_score(
    linear_model,
    X_train,
    y_train,
    cv=5,
    scoring="neg_mean_absolute_error"
)

# Scikit-learn negates loss metrics so higher scores are better.
mae_scores = -scores

print("MAE for each fold:", mae_scores.round(3))
print("Average CV MAE:", round(mae_scores.mean(), 3))
print("Standard deviation:", round(mae_scores.std(), 3))



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

print("Best CV MAE:",
      round(-search.best_score_, 3))



best_model = search.best_estimator_

test_predictions = best_model.predict(X_test)

mae = mean_absolute_error(y_test, test_predictions)
rmse = root_mean_squared_error(y_test, test_predictions)

print(f"Test MAE:  ${mae * 100_000:,.0f}")
print(f"Test RMSE: ${rmse * 100_000:,.0f}")
