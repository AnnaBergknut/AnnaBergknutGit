import matplotlib.pyplot as mpl
import pandas as pd
import numpy  as np
import scipy as scp

from sklearn.preprocessing import StandardScaler

df = pd.read_csv("winequality-white.csv", sep = ";")
df.isnull().values.any()

df.head(20)
