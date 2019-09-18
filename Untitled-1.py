# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
import pandas as pd
from constants import *
from helpers import normalise_number_data, normalise_word_data
import numpy as np
from sklearn import preprocessing


#%%
google_products = pd.read_csv(GOOGLE_SMALL_PATH)
amazon_products = pd.read_csv(AMAZON_SMALL_PATH)


#%%
google_products['price'] = normalise_number_data(google_products['price'])
amazon_products['price'] = normalise_number_data(amazon_products['price'])


#%%
google_products[['name']]
google_word_columns = ['name', 'description', 'manufacturer']
amazon_word_columns = ['title', 'description', 'manufacturer']


#%%
google_products[google_word_columns] = normalise_word_data(google_products[google_word_columns].astype(str))
amazon_products[amazon_word_columns] = normalise_word_data(amazon_products[amazon_word_columns].astype(str))


#%%



#%%
yeast_data = pd.read_csv(YEAST_PATH)


#%%
yeast_data['Class'] = yeast_data.Class.replace(to_replace=yeast_data.Class.unique(), value=[0, 1])


#%%
from sklearn.impute import SimpleImputer    


#%%
mean_imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
median_imputer = SimpleImputer(missing_values=np.nan, strategy='median')


#%%



#%%
X_mean = pd.DataFrame(mean_imputer.fit_transform(yeast_data.drop('Class', axis=1)))
X_median = pd.DataFrame(median_imputer.fit_transform(yeast_data.drop('Class', axis=1)))
Y = yeast_data['Class']


#%%
X_mean_mean = X_mean.mean()
X_mean_median = X_mean.median()
X_mean_std = X_mean.std()
X_mean_max = X_mean.max()
X_mean_max = X_mean.min()


#%%
X_median_mean = X_median.mean()
X_median_median = X_median.median()
X_median_std = X_median.std()
X_median_max = X_median.max()
X_median_max = X_median.min()


