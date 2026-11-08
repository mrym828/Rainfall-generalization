import numpy as np

class RidgeRegressionGD:
    """
    Batch Gradient Descent solution
    """
    def __init__(self, learning_rate=0.01, iterations=1000, lambda_=0.01):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.lambda_ = lambda_
        self.theta = None
        self.cost_history = []

    def calculate_cost(self, X, y):
        """
         J(theta) = 1/2m sum((hat yi - yi)^2) + lambda/2m sum(thetaj^2)
        """
        m = len(y)

        y_hat = X @ self.theta
        errors = y_hat - y
        mse_ = (1 / (2*m)) * np.sum(errors ** 2)
        regularization = (self.lambda_ / (2*m)) * np.sum(self.theta[1:] ** 2)

        return mse_ + regularization

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)

        m = len(y)
        X = np.c_[np.ones(m), X] # adding intercept

        self.theta = np.zeros(X.shape[1]) # initializing weights with 0
        self.cost_history = []

        for _ in range(self.iterations):
            y_hat = X @ self.theta
            errors = y_hat - y
            gradient = (1/m) * (X.T @ errors)
            theta_reg = self.theta.copy()
            theta_reg[0]= 0

            gradient += (self.lambda_ / m) * theta_reg
            self.theta = self.theta - self.learning_rate * gradient

            self.cost_history.append(self.calculate_cost(X,y))

        return self

    def predict(self, X):
        X = np.asarray(X, dtype=float)

        if self.theta is None:
            raise ValueError("Model must be fitted before prediction.")

        m = len(X)
        X = np.c_[np.ones(m), X]

        y_hat = X @ self.theta

        return y_hat


