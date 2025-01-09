#!/usr/bin/env python
# coding: utf-8

# # WELCOME TO THE NOTEBOOK
# ---
# 
# ### Exploratory vs Confirmatory Data Analysis
# In this project, we are going to learn about two important data analysis methods **EDA** (Exploratory Data Analysis) and **CDA** (Confirmatory Data Analysis).
# 

# ### Task 1: What Is Exploratory Data Analysis (EDA)?
# 
# Definition: EDA or Exploratory Data Analysis is one of the data analysis methods where we use different statistical summaries and graphical representations to perform initial investigations on the data to discover interesting patterns, spot anomalies, and overall for a better understanding of our data.

# Importing Modules

# In[1]:


# Pandas Module
import pandas as pd

# Data Visualization Module
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

# Setting some default settings
pd.set_option('mode.chained_assignment',None)
pyo.init_notebook_mode()


# Let's load our dataset

# In[2]:


#encoding specified
data = pd.read_csv('dataset.csv', engine='python', encoding='latin1')


# Checking the data size

# In[3]:


data.shape


# Checking the data

# In[4]:


data.head()


# ### Task 2: EDA - Where to start?
# 
# In this task, we are going to talk about How to start our exploration. 
# 
#     Different column data types
#     How are the columns related
#     What are the different information in our data
#     Make a list of the information and start from the first 
# 
# 

# Now let's start with checking the column data types 

# In[5]:


data.head()


# In[6]:


data.dtypes


# Now let's talk about what type of information do we have in this data
# 
# ### In our data, we have the following information:
#     
#     Time Information (Order Data)
#     Customer Information (Customer Name)
#     Place Information (State name)
#     Hierarchical Information about the products (Category, Sub-category, Product Name)
#     Sale Information (sales, profit, quantity)
# 
# <img width = 200px, height = 200px,  src='images/information cube.png'>
# now let's start our exploration

# ### Task 3: Data Exploration: Time Information 

# In[7]:


data.head()


# What is the timespan of our data?

# In[8]:


data['Order Date']= pd.to_datetime(data['Order Date'])
from_=data['Order Date'].min()
to_=data['Order Date'].max()
print('We have the sales information from',from_, 'to')


# Now let's sort our data by the date

# In[9]:


data = data.sort_values(by = 'Order Date')
data.head()


# Some data preparation: let's extract year, month, and day from the Order Date column

# In[10]:


data['Year']=pd.DatetimeIndex(data['Order Date']).year
data['Month']=pd.DatetimeIndex(data['Order Date']).month
data['Day']=pd.DatetimeIndex(data['Order Date']).day

data.head()


# Profit gained over time by different product categories

# In[11]:


data_time_yearly_profit = data.groupby(['Year','Category']).agg({'Profit':'sum'}).reset_index()

data_time_yearly_profit.head()


# Visualizing the results using a line chart

# In[12]:


px.line(data_time_yearly_profit , x = 'Year', y = 'Profit', color = 'Category')


# Exercise: Analyse the monthly profits gained from sales of different product categories. use a linechart to visualize your results. 

# In[13]:


data_time_monthly_profit = data.groupby(['Year','Month','Category']).agg({'Profit':'sum'}).reset_index()
data_time_monthly_profit['Date'] = data_time_monthly_profit.Year.astype(str) + '-' + data_time_monthly_profit.Month.astype(str) + '-01'
data_time_monthly_profit.head()


# In[14]:


px.line(data_time_monthly_profit, x = 'Date', y= 'Profit', color = 'Category')


# ### Data Exploration: Customer Aspect

# let's see how many unique costumers do we have

# In[15]:


len(data['Customer Name'].unique())


# let's see the yearly change in number of unique customers

# In[16]:


customer_data = data.groupby('Year').agg({'Customer Name': 'nunique'}).reset_index()
customer_data


# visualizing the result

# In[17]:


px.line(customer_data, x = 'Year',y = 'Customer Name')


# Top 10 customers who brought the highest profit 

# In[18]:


top10_customers = data.groupby('Customer Name').agg({'Profit':'sum'}).reset_index().sort_values('Profit' ,ascending = False).head(10)
top10_customers


# In[19]:


px.bar(top10_customers, x = 'Customer Name', y = 'Profit')


# In[ ]:





# ### Task 4: Data Exploration: Place (location) Aspect

# Let's analyze the profits gained in different states in the US

# In[20]:


geo_data = data.groupby('State').agg({'Profit':'sum'}).reset_index()
geo_data


# ### Let's create a choropleth map 
# Plotly uses abbreviated two-letter postal codes for state locations so it will be necessary to create a dictionary that contains conversions of the full names of states into abbreviations.

# In[21]:


state_codes = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
}


# let's map the abbreviated two-letter postal codes to the State column

# In[22]:


geo_data.State = geo_data.State.map(state_codes)


# In[23]:


px.choropleth(geo_data,
              locations ='State',
              color = 'Profit',
              locationmode = 'USA-states',
              scope = 'usa',
              title = 'Profit Gained In different states'
             )
              


# Exercise: Create a choropleth map to visualize the profit gained by selling technology(Category=technology) products in different states. 

# In[ ]:





# ### Task 5: Data Exploration - Hierarchical Information about the products

# In[24]:


data


# In[25]:


product_data = data.groupby(['Category','Sub-Category']).agg({'Profit':'sum'}).reset_index()
product_data =product_data[product_data.Profit > 0]
product_data['Sales'] = 'Any'
product_data


# In[26]:


px.sunburst(product_data, path = ['Sales','Category','Sub-Category'],values = 'Profit')


# In[27]:


px.treemap(product_data,path = ['Sales','Category','Sub-Category'],values = 'Profit')


# ### Task 6: Data Exploration: Product Sales information (Sales, Quantity, Profit)

# In[28]:


data.head()


# Distribution Analysis on **Quantity** column 

# Let's check the statistical summary of the column

# In[29]:


data.Quantity.describe()


# In[30]:


px.histogram(data,x = 'Quantity')


# In[31]:


px.box(data,y ='Quantity',x = 'Category', color = 'Year')


# Exercise: Apply distribution analysis using boxplot to the **Profit** column. using statistical summary and a box plot. 

# In[32]:


data.Profit.describe()


# In[33]:


px.box(data,y = 'Profit')


# ### Task 7: What Is Confirmatory Data Analysis (CDA)? 

# By definition, Confirmatory Data Analysis is the process of using statistical summary and graphical representations to evaluate the validity of an assumption about the data at hand.
# 
# We have the following assumption about our data, and we are going to use different exploration techniques we learned in the previous tasks to validate them. 
# 
#     Assumption 1 - Every summer technology products have the highest sale quantity compared to other product categories.
#     Assumption 2- In New York, there are many big companies, therefore, office supplies product has 
#     the highest sale quantity compared to other big states such as Texas, Illinois, and California. 
# 

# Assumption 1 - Every summer technology products have the highest sale quantity compared to other product categories.

# In[35]:


seasons = {
    1 : "Winter",
    2 : "Spring",
    3 : "Summer",
    4 : "Fall"
}


# Creating **Season** column

# In[36]:


data['Season'] = data.Month.astype(int)%12//3+1
data.Season = data.Season.map(seasons)
data.head()


# Extracting data related to summer every year

# In[37]:


summer_data = data[data.Season == 'Summer']
summer_data.head()


# Aggregating data based on Year, Category, and Season columns and summing up the Quantity

# In[38]:


summer_data_agg = summer_data.groupby(['Year','Category','Season']).agg({'Quantity':'sum'}).reset_index()
summer_data_agg.head()


# Let's visualize our result using a grouped bar chart

# In[51]:


px.bar(summer_data_agg, x = summer_data_agg.Year.astype('str'),
      y = 'Quantity',color = 'Category', barmode = 'group')


# Exercise: Use the analytical techniques that you've learned during the course to validate the following assumption:
#         
#         Assumption 2- In New York, there are many big companies, therefore, office supplies 
#         product has the highest sale quantity compared to other big states such as Texas, Illinois, and California. 

# In[ ]:





# 
# 
# ---
# 
# <img align=left width=20px height=20px src="images/luck.png">**Good Luck!**</img>
