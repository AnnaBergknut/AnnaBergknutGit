import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Generate the x_data and y_data
x_data = np.linspace(-0.5, 0.5, 200)[:, np.newaxis]
noise = np.random.normal(0, 0.02, x_data.shape)
y_data = np.square(x_data) + noise

# Create a linear regression model
model = LinearRegression()

# Fit the model to the data
model.fit(x_data, y_data)

# Make predictions
y_pred = model.predict(x_data)

# Plot the data and the regression line
plt.scatter(x_data, y_data, c='b', label='Actual Data')
plt.plot(x_data, y_pred, c='r', label='Regression Line')
plt.xlabel('X Data')
plt.ylabel('Y Data')
plt.legend()
plt.show()