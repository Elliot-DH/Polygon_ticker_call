#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import urllib
import requests
from requests.auth import HTTPBasicAuth
import json
import os
import pandas as pd
import ast
import matplotlib.pyplot as plt
from datetime import date
from dateutil.relativedelta import relativedelta


# In[2]:


#Input Ticker

ticker = input("Enter Ticker:")


# In[5]:


#today

today = date.today()

print(today)

#1 Replative year

one_ry = today - relativedelta(years=1)


# In[7]:


#Defining the Autorisation header as a dictionary.

headers = {
    "Authorization": "Bearer NPjKvm5T0ibFESLA9Tp6GYcPuQ1pnpOv"  
}


# In[9]:


api = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{one_ry}/{today}" #The request URL


# In[11]:


response = requests.get(api, headers=headers)#The important bit. Using requests package to send get call

print(response.status_code)

if response.status_code == 200:
    print("Great Success")

else:
    print(f"Failed with status code : {response.status_code}")


# In[13]:


try:
    response_json = response.json()
    print(json.dumps(response_json, indent=4))  # Pretty-printed JSON
except ValueError:
    print("The response is not in JSON format")


# In[15]:


# Get the path to the Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Define the file path directly on the Desktop
json_file_path = os.path.join(desktop_path, "Polygon.json")

if response.status_code == 200:
    try:
        # Parse the JSON data
        response_json = response.json()

        # Save the JSON data to a .json file
        with open(json_file_path, "w") as json_file:
            json.dump(response_json, json_file, indent=4)

        print(f"File downloaded successfully as {json_file_path}")

    except ValueError:
        print("The response is not in JSON format.")
else:
    print(f"Failed to fetch the file. Status code: {response.status_code}")


# In[17]:


full_df = pd.read_json(json_file_path)

print(full_df.head())


# In[19]:


full_df.to_csv(os.path.join(desktop_path, "Polygon.csv"), index=False)


# In[21]:


full_df['results']


# In[23]:


res_arr = full_df['results'].to_numpy()    # Make array of dictionary collumn 

print(res_arr)


# In[25]:


type(res_arr[0]) #elements in res_arr are alrady dict and not string so do not need to ast.literal_eval


# In[27]:


keys = (res_arr[0]).keys()   # Find the dictionary keys

print(keys) #These keys will make up columns in new df


# In[29]:


new_dict = {k:[] for k in keys} #new dictionary that will have a key for every k in keys^ and an empty list value pair for each key


# In[31]:


#loop through the original array and pass values to keys
for r in res_arr:
    
    dict_keys = r.keys()
    
    for key in dict_keys:      # Loop through the keys in that dictionary
        new_dict[key].append(r[key]) # Append value corresponding to key to that keys list in result dictionary


# In[33]:


result = pd.DataFrame(new_dict)


# In[35]:


result.head()


# In[37]:


x = result.index  # Index as x
y = result['c']   # Opening price as y
coefficients = np.polyfit(x, y, 1)  # Linear fit (degree 1)
linear_regression = np.poly1d(coefficients)  # Create regression line
regression_line = linear_regression(x)

# Plot
plt.figure(figsize=(20, 10))
plt.plot(x, y, marker='o', label='Opening Price', linestyle='--', color='b')  # Data points
plt.plot(x, regression_line, label='Linear Regression', color='r')  # Regression line

# Customization
plt.title('Index vs Opening Price with Linear Regression', fontsize=14)
plt.xlabel('Index', fontsize=12)
plt.ylabel('Opening Price', fontsize=12)
plt.grid(True)
plt.legend()
plt.show()


# In[39]:


#slope

print(regression_line[result.index.max()], regression_line[0])

slope = (regression_line[result.index.max()] - regression_line[0]) / (x[result.index.max()] - x[0])

print("The slope of the line of best fit is", slope)


# In[ ]:





# In[ ]:




