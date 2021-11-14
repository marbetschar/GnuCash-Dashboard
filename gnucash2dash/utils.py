import os
import numpy
import config

from datetime import datetime

def sign(i):
    return (i > 0) - (i < 0)

def linear_regression_coefficients(y):
  y_len = len(y)

  x = numpy.zeros(y_len)
  for i in range(0, y_len):
    x[i] = i

  # Linear Regression: Fitting using Least-Squares Method
  A = numpy.vstack([x, numpy.ones(y_len)]).T
  a, b = numpy.linalg.lstsq(A, y, rcond=None)[0]

  return a, b, x

def now():
    env_now = os.environ.get('GNUCASH2DASH_NOW', config.now)

    if not env_now is None:
        return datetime.fromisoformat(env_now)
    return datetime.now()
