from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import joblib

def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(X_train, y_train)

    xgb = XGBRegressor(n_estimators=200)
    xgb.fit(X_train, y_train)

    print("RF MAE:", mean_absolute_error(y_test, rf.predict(X_test)))
    print("XGB MAE:", mean_absolute_error(y_test, xgb.predict(X_test)))

    joblib.dump(xgb, "models/xgb_model.pkl")

    return xgb