from numpy import genfromtxt
from sklearn.linear_model import LogisticRegression


def act():
  my_data = genfromtxt(response, delimiter=',')
  X = [my_data[i][:-1] for i in range(350)]
  y = [my_data[i][-1] for i in range(350)]

  model.fit(X, y)
  y_test = model.predict_proba([my_data[i][:-1] for i in range(301,363)])[:,1]
  mse = ((y_test-[my_data[i][-1] for i in range(301,363)])**2).mean()
  return mse
