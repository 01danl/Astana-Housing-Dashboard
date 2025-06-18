from sklearn.model_selection import train_test_split
X = df_enc.drop('Price', axis=1)
y = df_enc['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Model (Linear Regression)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_pred, y_test))
print(f"RMSE: {rmse}")
r2 = r2_score(y_pred, y_test)
print(f"R^2: {r2}") 
#P.S: I know about RMSE, it's very bad, i guess it's temporary until I don't solve this problem
