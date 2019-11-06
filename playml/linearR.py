import numpy as np
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

class linearR:

    def __init__(self):
        #初始化模型
        self.coef_ = None
        self.interception_= None
        self._theta = None

    def fit_normal(self , X_train , y_train):
        assert X_train.shape[0] == y_train.shape[0], \
            "the size of X_train must be equal to the size of y_train"
        X_b = np.hstack([np.ones((len(X_train), 1)), X_train])
        self._theta = np.linalg.inv((X_b.T).dot(X_b)).dot(X_b.T).dot(y_train)
        self.interception_ = self._theta[0]
        self.coef_ = self._theta[1:]

        return self
    def fit_gd(self, X_train, y_train, eta = 0.01, n_iters = 1e4):
        assert X_train.shape[0] == y_train.shape[0], \
            "the size of X_train must be equal to the size of y_train"
        def j( theta , X_b, y):
            try:
                return np.sum((y - X_b.dot(theta)) ** 2 / len(y))
            except:
                return float('inf')
        def dj( theta, X_b , y):
            res = np.empty(len(theta))
            res[0] = np.sum(X_b.dot(theta) - y)
            for i in range(1, len(theta)):
                res[i] = (X_b.dot(theta) - y).dot(X_b[:, i])
            return res * 2 / len(X_b)
        def gradinet_descent( X_b, y, initial_theta, eta, n_iter= 1e4, epsilon = 1e-8):
            theta = initial_theta
            i_iter = 0

            while i_iter < n_iter:
                gradient = dj(theta, X_b, y)
                last_theta = theta
                theta = theta - eta * gradient

                if (abs(j(theta, X_b, y) - j(last_theta, X_b, y)) < epsilon):
                    break
                i_iter += 1
            return theta
        X_b = np.hstack([np.ones((len(X_train), 1)), X_train])
        initial_theta = np.zeros(X_b.shape[1])
        self._theta = gradinet_descent(X_b, y_train, initial_theta, eta, n_iter= 1e4, epsilon = 1e-8)

        self.interception_  = self._theta[0]
        self.coef_ = self._theta[1:]

        return self
    def predict(self, X_predict):
        #给定带预测数据集X_predict, 返回表示X_predict的结果向量
        assert self.interception_ is not None and self.coef_ is not None, \
            "must fit defore predict"
        assert X_predict.shape[1] == len(self.coef_), \
            "the feature number of X_predict must be equal to X_train"
        X_b = np.hstack([np.ones((len(X_predict), 1)), X_predict])
        return X_b.dot(self._theta)

    def r2_score(self, X_test, y_test):
        #预测模型准确度
        y_predict = self.predict(X_test)

        return r2_score(y_test, y_predict)
        #

    def MSE(self, X_test, y_test):

        y_predict = self.predict(X_test)
        return mean_squared_error(y_test, y_predict)
        #均方误差

    def MAE(self, X_test, y_test):

        y_predict = self.predict(X_test)
        return mean_absolute_error(y_test, y_predict)
        #平均绝对误差

    def __repr__(self):
        return "linearR()"

