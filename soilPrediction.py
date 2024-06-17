#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix,classification_report,accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV,RandomizedSearchCV
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.preprocessing import OrdinalEncoder,LabelEncoder,OneHotEncoder
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
import warnings

warnings.filterwarnings("ignore")


# In[3]:


crop = pd.read_csv('soil.csv')


# In[4]:


crop


# In[5]:


crop.shape


# In[6]:


crop.info()


# In[7]:


crop.isnull().sum()


# In[8]:


crop.duplicated().sum()


# In[9]:


crop.columns


# In[10]:


crop['label'].unique()


# In[11]:


crop['label'].value_counts()


# In[12]:


crop['label'].value_counts()


# In[13]:


plt.figure(figsize=(5,5))
crop['label'].value_counts().plot(kind='pie',autopct="%.1f%%")
plt.show()


# In[14]:


sns.histplot(crop['Temperature'],color='Orange')
plt.title('Histogram of Temperature')
plt.show()


# In[15]:


sns.histplot(crop['Humidity'],color='Red')
plt.title('Histogram of Humidity')
plt.show()


# In[16]:


sns.histplot(crop['SoilMoisture'],color='Brown')
plt.title('Histogram of SoilMoisture ')
plt.show()


# In[17]:


plt.figure(figsize=(12,12))
i=1
for col in crop.iloc[:,:-1]:
    plt.subplot(3,3,i)
    sns.kdeplot(crop[col])
    i+=1


# In[18]:


import scipy.stats as sm


# In[19]:


plt.figure(figsize=(12,12))
i=1
for col in crop.iloc[:,:-1]:
    plt.subplot(3,3,i)
    sm.probplot(crop[col],dist='norm',plot=plt)
    i+=1


# In[20]:


plt.figure(figsize=(12,12))
i=1
for col in crop.iloc[:,:-1]:
    plt.subplot(3,3,i)
    crop[[col]].boxplot()
    i+=1


# In[21]:


crop.iloc[:,:-1].skew()


# In[22]:


class_labels = crop['label'].unique().tolist()
class_labels


# In[23]:


le = LabelEncoder()
crop['label'] = le.fit_transform(crop['label'])


# In[24]:


crop['label']


# In[25]:


class_labels = le.classes_
class_labels


# In[26]:


crop


# In[27]:


x = crop.drop('label',axis=1)
y = crop['label']


# In[28]:


x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,shuffle=True)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)


# In[29]:


sns.heatmap(crop.corr(),annot=True)


# In[30]:


from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score


# create instances of all models
models = {
    'Logistic Regression': LogisticRegression(),
    'Naive Bayes': GaussianNB(),
    'Support Vector Machine': SVC(),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'Bagging': BaggingClassifier(),
    'Gradient Boosting': GradientBoostingClassifier(),
}

for name, md in models.items():
    md.fit(x_train,y_train)
    ypred = md.predict(x_test)
    
    print(f"{name}  with accuracy : {accuracy_score(y_test,ypred)}")


# In[31]:


rf_model = RandomForestClassifier(criterion = 'gini',
                                 max_depth = 8 ,
                                 min_samples_split = 10,
                                 random_state = 5)


# In[32]:


rf_model.fit(x_train , y_train)


# In[33]:


crop.columns


# In[34]:


y_pred = rf_model.predict(x_test)


# In[35]:


y_pred


# In[36]:


confusion_matrix(y_test , y_pred)


# In[37]:


print("accuracy: ", accuracy_score(y_test , y_pred));print()
print("Classification report: ")

print(classification_report(y_test,y_pred));print()


# In[38]:


label_dict = {}
for index,label in enumerate(class_labels):
    label_dict[label] = index
    
print(label_dict)


# In[42]:


Temperature = 25
Humidity =  89
SoilMoisture = 56
if not (10 <= Temperature <= 50 and 10 <= Humidity <= 100 and 30 <= SoilMoisture <= 95):
    print("Unknown crop  predicted")
else:
    pred = rf_model.predict([[Temperature, Humidity, SoilMoisture]])
    crop_label = le.inverse_transform(pred)
    print("Predicted Crop:", crop_label[0])


# In[40]:


import pickle
with open('crop_prediction_model.pkl', 'wb') as file:
    pickle.dump(rf_model, file)


# In[ ]:




