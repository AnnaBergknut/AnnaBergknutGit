import matplotlib.pyplot as mpl
import pandas as pd
import numpy  as np
import scipy as scp

from sklearn.preprocessing import StandardScaler
import csv

df = pd.read_csv("C:/Users/annan/repos/AnnaBergknutGit/BTH/ML/Assigment 1/winequality-white.csv", sep = ";")
"""
with open('winequality-white.csv','r') as file:
    df = csv.reader(file)
# df = open("C:\Users\annan\repos\AnnaBergknutGit\BTH\ML\Assigment 1\winequality-white.csv", "r") """

df.isnull().values.any()

df.head(20)
