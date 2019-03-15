import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
from sklearn.kernel_ridge import KernelRidge

df = pd.read_csv('data.csv')

X = df.iloc[:,3:8]
Y = df.iloc[:,10]

FEATURES = X.columns 
LABEL = Y.name

scaler = MinMaxScaler()
X = pd.DataFrame(scaler.fit_transform(X), columns=FEATURES)
Y = pd.DataFrame(scaler.fit_transform(Y.values.reshape(-1, 1)), columns=[LABEL])


# Kernel Ridge Regression using an rbf kernel

best_score = 0
best_alpha = 0
best_gamma = 0
for _alpha in [0.001, 0.005, 0.01, 0.05, .1, .2, .3, .4, .5, .6]:
    for _gamma in range(1,11):
        reg = KernelRidge(kernel="rbf", alpha=_alpha, gamma=_gamma)
        reg.fit(X,Y)
        current_score = reg.score(X,Y)
        print("Alpha: {} | Gamma : {} | Score: {}".format(_alpha, _gamma, current_score))
        if current_score > best_score:
            best_score = current_score
            best_alpha = _alpha
            best_gamma = _gamma
print("Best Score: {} ".format(best_score))
print("Best Alpha: {} ".format(best_alpha))
print("Best Gamma: {} ".format(best_gamma))

# Kernel Ridge Regression using a polynomial kernel 

reg = KernelRidge(kernel="polynomial", alpha=0.001, gamma=10, degree=5)
info = reg.fit(X,Y)
pred_val = reg.predict(X)
plt.plot(range(len(pred_val)), pred_val, 'r--', range(len(pred_val)), Y, 'b--')
plt.show()

