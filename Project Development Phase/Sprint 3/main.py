# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QEZRFhZ_lDBEUm9-w_y3Nsi-IPskx6E9
"""

import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor

import warnings
warnings.filterwarnings('ignore')

# Importing Raw Files
train_raw = pd.read_csv('/content/test.csv')
test_raw = pd.read_csv('/content/test.csv')
meal = pd.read_csv('/content/meal_info.csv')
centerinfo = pd.read_csv('/content/fulfilment_center_info.csv')

# Analyzing Data
print("The Shape of Demand dataset :", train_raw.shape)
print("The Shape of Fulfillment Center Information dataset :", centerinfo.shape)
print("The Shape of Meal information dataset :", meal.shape)
print("The Shape of Test dataset :", test_raw.shape)

train_raw.head()

centerinfo.head()

meal.head()

test_raw.head()

train_raw.isnull().sum().sum()

test_raw.isnull().sum().sum()

print("The company  has", centerinfo["center_id"].nunique(), " warehouse ", "spreed into  ",
      centerinfo["city_code"].nunique(), "City and ", centerinfo["region_code"].nunique(), "Regions")
print("The products of the company are ", meal["meal_id"].nunique(), "unique meals , divided into  ",
      meal["category"].nunique(), "category and ", meal["cuisine"].nunique(), "cuisine")

train = pd.merge(train_raw, meal, on="meal_id", how="left")
train = pd.merge(train, centerinfo, on="center_id", how="left")
print("Shape of train data : ", train.shape)

train.head()

test = pd.merge(test_raw, meal, on="meal_id", how="outer")
test = pd.merge(test, centerinfo, on="center_id", how="outer")
print("Shape of test data : ", test.shape)

test.head()

col_names = ['center_id', 'meal_id', 'category', 'cuisine', 'city_code', 'region_code', 'center_type']
train[col_names] = train[col_names].astype('category')
test[col_names] = test[col_names].astype('category')
print("Train Datatype\n", train.dtypes)
print("Test Datatype\n", test.dtypes)

fig = px.pie(values=train["category"].value_counts(), names=train["category"].unique(),
             title="Most popular food category")

fig.show()

sns.boxplot(train["checkout_price"])

train['discount percent'] = ((train['base_price'] - train['checkout_price']) / train['base_price']) * 100

train['discount y/n'] = [1 if x > 0 else 0 for x in (train['base_price'] - train['checkout_price'])]

test['discount percent'] = ((test['base_price'] - test['checkout_price']) / test['base_price']) * 100
test['discount y/n'] = [1 if x > 0 else 0 for x in (test['base_price'] - test['checkout_price'])]
train.head(2)

plt.figure(figsize=(13, 13))
sns.heatmap(train.corr(), linewidths=.1, cmap='Reds', annot=True)
plt.title('Correlation Matrix')
plt.show()

def one_hot_encode(features_to_encode, dataset):
    encoder = OneHotEncoder(sparse=False)
    encoder.fit(dataset[features_to_encode])
    encoded_cols = pd.DataFrame(encoder.transform(dataset[features_to_encode]), columns=encoder.get_feature_names())
    dataset = dataset.drop(columns=features_to_encode)
    for cols in encoded_cols.columns:
        dataset[cols] = encoded_cols[cols]
    return dataset

ls = train.select_dtypes(include='category').columns.values.tolist()

features_to_encode = ls
data = one_hot_encode(features_to_encode, train)
data = data.reset_index(drop=True)

OH_test = one_hot_encode(features_to_encode, test)
test_final = OH_test.drop(["id", "base_price", "discount y/n"], axis=1)

RF_pipe = make_pipeline(StandardScaler(), RandomForestRegressor(n_estimators=100, max_depth=7))

Submission.to_csv('/content/sample_submission.csv', index=False)
print(Submission.shape)
print(Submission.head())