#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 21:48:45 2019

@author: Boyao
"""
import pandas as pd
import numpy as np
import os
import statsmodels.formula.api as sm
os.chdir('/Users/Boyao/Desktop/UAB/Development/PS1Final')
#from data_functions_albert import remove_outliers
os.chdir('/Users/Boyao/Desktop/UAB/Development/PS1Final')
from statsmodels.iolib.summary2 import summary_col
pd.options.display.float_format = '{:,.2f}'.format
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

dollars = 2586.89    #https://data.worldbank.org/indicator/PA.NUS.FCRF

#   QUESTION 1.1:
data = pd.read_stata("Uganda.dta")
data['inctotal'] = data['hh_ttincome_2013'].fillna(0)
urban = data.loc[data["urban2"]==2,["HHID","hh_consumption_year_2013","Total","hh_ttincome_2013"]]
urban.columns = ['hh','urban consumption','urban wealth', 'urban income']
urban=urban.groupby(by = "hh")[["urban consumption","urban wealth","urban income"]].mean()/dollars
rural = data.loc[data["urban2"]==1,["HHID","hh_consumption_year_2013","Total","hh_ttincome_2013"]]
rural.columns = ['hh','rural consumption','rural wealth', 'rural income']
rural=rural.groupby(by = "hh")[["rural consumption","rural wealth","rural income"]].mean()/dollars


curban = urban[["urban consumption"]]
curban = curban.dropna()
wurban = urban[["urban wealth"]]
iurban = urban[["urban income"]]
sum_urb=urban[["urban consumption","urban wealth", "urban income"]]
sum_urb=sum_urb.describe()
print(sum_urb.to_latex())


crural = rural[["rural consumption"]]
crural = crural.dropna()
wrural = rural[["rural wealth"]]
irural = rural[["rural income"]]
sum_rur=rural[["rural consumption","rural wealth", "rural income"]]
sum_rur=sum_rur.describe()
print(sum_rur.to_latex())



# QUESTION 1.2:
#Comparation:
# IMPORTANT NOTE: WE NEED TO SEEE IF SCALES ARE CORRECT, SINCE INCOME IS 
# IN HUNDRED THOUSAND AND CONSUMPTION IN THOUSANDS.

#CIW combined in one histogram per area

#Convert to array
iu=np.asarray(iurban)
cu=np.asarray(curban)
wu=np.asarray(wurban)
cr=np.asarray(crural)
ir=np.asarray(irural)
wr=np.asarray(wrural)

#Urban hist
plt.figure
plt.subplots_adjust(top=0.9, bottom=0, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('CIW Histograms')
bins=25 #Adjust the number of bins

plt.subplot(2,2,1)
plt.hist(cu, bins, alpha=0.5, label='Urban_C')
plt.hist(iu, bins, alpha=0.5, label='Urban_I')
#pyplot.hist(wu, bins, alpha=0.5, label='Wealth')
plt.legend(loc='upper right')

plt.subplot(2,2,2)
plt.hist(cu, bins, alpha=0.5, label='Urban_C')
plt.hist(wu, bins, alpha=0.5, color='r', label='Urban_W')
#pyplot.hist(wu, bins, alpha=0.5, label='Wealth')
plt.legend(loc='upper right')

plt.subplot(2,2,3)
plt.hist(cr, bins, alpha=0.5,label='Rural_C')
plt.hist(ir, bins, alpha=0.5, label='Rural_I')
#pyplot.hist(wu, bins, alpha=0.5, label='Wealth')
plt.legend(loc='upper right')

plt.subplot(2,2,4)
plt.hist(cr, bins, alpha=0.5, label='Rural_C')
plt.hist(wr, bins, alpha=0.5, color='r', label='Rural_W')
#pyplot.hist(wu, bins, alpha=0.5, label='Wealth')
plt.legend(loc='upper right')
plt.show()


# VARIANCES:
###RURAL.
#Since logarithm of 0 is menus infinite, I convert these values to 0. Variance will be undervaluated.
lncrural = np.log(crural)
varcrural =  np.var(lncrural)
irural = irural.replace(0, 1)
lnirural = np.log(irural)
varirural =  np.var(lnirural)
wrural = wrural.replace(0, 1)
lnwrural = np.log(wrural)
varwrural =  np.var(lnwrural)

### Urban.
lncurban = np.log(curban)
varcurban = np.var(lncurban)
iurban = iurban.replace(0, 1)
lniurban = np.log(iurban)
iurban = lniurban.fillna(0)
variurban = np.var(lniurban)
wurban = wurban.replace(0, 1)
lnwurban = np.log(wurban)
wurban = lniurban.fillna(0)
varwurban = np.var(lnwurban)



# QUESTION 1.3: CROSS-SECTION
#I remove 0 consumption people:
urban = urban.dropna()
rural = rural.dropna()

#1- Correlations Matrix (CM)
CIW_R=rural[["rural consumption","rural wealth", "rural income"]]
CM_R= CIW_R.corr()
print(CM_R.to_latex())

CIW_U=urban[["urban consumption","urban wealth", "urban income"]]
CM_U= CIW_U.corr()
print(CM_U.to_latex())

#2.- Joint density graphs
with sns.axes_style('white'):
    sns.jointplot("rural income", "rural consumption", rural, kind='kde');

with sns.axes_style('white'):
    sns.jointplot("urban income", "urban wealth", rural, kind='kde');

with sns.axes_style('white'):
    sns.jointplot("urban income", "urban consumption", urban, kind='kde');

with sns.axes_style('white'):
    sns.jointplot("urban income", "urban wealth", urban, kind='kde');
    

    
#QUESTION 1.4: LIFECYCLE CIW:
# Uganda
A = data.groupby(by = "age")[["hh_consumption_year_2013","Total","hh_ttincome_2013"]].mean()
A['age'] = A.index

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Age')
ax1.set_ylabel('CI', color=color)
ax1.plot(A['age'],A[['hh_consumption_year_2013']] , color='g',label='consumption')
ax1.plot(A['age'],A[['hh_ttincome_2013']] , color=color,label='income')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Wealth', color=color)  # we already handled the x-label with ax1
ax2.plot(A['age'],A[['Total']] , color=color, label='wealth')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.legend(loc='best')
plt.title('Uganda CIW life-cycle profile')
plt.show()

#Urban
Urban_data=data.loc[data["urban"]=='Urban',["hh_consumption_year_2013","Total","hh_ttincome_2013","age"]]
A = Urban_data.groupby(by = "age")[["hh_consumption_year_2013","Total","hh_ttincome_2013"]].mean()
A['age'] = A.index

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Age')
ax1.set_ylabel('CI', color=color)
ax1.plot(A['age'],A[['hh_consumption_year_2013']] , color='g',label='consumption')
ax1.plot(A['age'],A[['hh_ttincome_2013']] , color=color,label='income')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Wealth', color=color)  # we already handled the x-label with ax1
ax2.plot(A['age'],A[['Total']] , color=color, label='wealth')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.legend(loc='best')
plt.title('Urban CIW life-cycle profile')
plt.show()


#Rural
Rural_data=data.loc[data["urban"]=='Rural',["hh_consumption_year_2013","Total","hh_ttincome_2013","age"]]
A = Rural_data.groupby(by = "age")[["hh_consumption_year_2013","Total","hh_ttincome_2013"]].mean()
A['age'] = A.index

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Age')
ax1.set_ylabel('CI', color=color)
ax1.plot(A['age'],A[['hh_consumption_year_2013']] , color='g',label='consumption')
ax1.plot(A['age'],A[['hh_ttincome_2013']] , color=color,label='income')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Wealth', color=color)  # we already handled the x-label with ax1
ax2.plot(A['age'],A[['Total']] , color=color, label='wealth')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.legend(loc='best')
plt.title('Rural CIW life-cycle profile')
plt.show()


#1.5 EXTREME BEHAVIOUR
#Rank by income percentile
data['inctotal'] = data["hh_ttincome_2013"].replace(0,float('NaN'))
data['I_Percentile_rank']=data.inctotal.rank(pct=True)

#Get the consumption/wealth share of the income top and bottom 10%. 
#Consumption
C_bottom=data.loc[data["I_Percentile_rank"]<0.1,["hh_consumption_year_2013"]]
C_bottom_10share=C_bottom.sum()/data["hh_consumption_year_2013"].sum()
C_top=data.loc[data["I_Percentile_rank"]>0.9,["hh_consumption_year_2013"]]
C_top_10share=C_top.sum()/data["hh_consumption_year_2013"].sum()
#The bottom 10% consumes only about 6% and the top 10% about 12%. 

#Wealth
W_bottom=data.loc[data["I_Percentile_rank"]<0.1,["Total"]]
W_bottom_10share=W_bottom.sum()/data["Total"].sum()
W_top=data.loc[data["I_Percentile_rank"]>0.9,["Total"]]
W_top_10share=W_top.sum()/data["Total"].sum()

#%%QUESTION 2 DATA
data2 = pd.read_stata("gsec1.dta")
dataurban = data2[["HHID","urban"]]
dataurban = dataurban.replace(['Urban', 'Rural'], 
                     [1, 0])

'''in Gender, 1 if women, 0 if men '''
data2 = pd.read_stata("gsec2.dta")
dataage = data2[["HHID","h2q8", "h2q3"]]
dataage.columns = [["HHID","Age1", "Gender"]]
dataage = dataage.replace(['Female', 'Male'], 
                     [1, 0])
dataage.columns = ['HHID','Age1', 'Gender']

age = pd.read_stata("GSEC2.dta")
age = age[['HHID','h2q8', 'h2q4']]
age = age.loc[age['h2q4'].isin(['Head']),['HHID','h2q8']]
age.columns = ['HHID', 'age']
dataage = dataage.merge(age, on='HHID', how='left')
dataage = dataage[['HHID', 'age', 'Gender']]
data2 = dataage.merge(dataurban, on="HHID", how="left")


'''Less than primary is 0, primary is 1, and more or equal than secundary is 2 .
Don't know is understood as less than primary.'''
school = pd.read_stata("gsec3.dta")
school = school[["HHID","h3q3"]].dropna()
school.columns = ["HHID","school"]
school = school.replace(['No formal education (*OLD*)', 'Less than primary (*OLD*)', 
                           'Some schooling but not Completed P.1','DK','Completed P.1','Completed P.2'
                           ,'Completed P.3', 'Completed P.4', 'Completed P.5', 'Completed P.6','Completed P.7'
                           ,'Completed J.1', 'Completed J.2', 'Completed J.3', '	Completed primary (*OLD*)'
                           ,'Completed S.1', 'Completed S.2', 'Completed S.3', 'Completed S.4'
                           ,'Completed S.5', 'Completed S.6', 'Completed Post primary Specialized training or Certificate'
                           ,'Completed Post secondary Specialized training or diploma', 'Completed Degree and above'
                           , 'Some secondary', 'Some primary', 'Never attended school', 'Completed O-level (*OLD*)'
                           ,'Completed A-level (*OLD*)', 'Completed University (*OLD*)', 'Don\'t know (*OLD*)', 'Completed primary (*OLD*)', '	Other (Specify) (*OLD*)'], 
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 2, 0, 1, 0])

data1 = data2.merge(school, on="HHID", how="left")

'''METHOD: I took for intensive labour hours worked the whole week and 
I add iit '''
age.columns = ['hh','age']

data2 = pd.read_stata("gsec8_1.dta")
data2 = data2.merge(data1, on="HHID", how="left") 
data2 = data2[["HHID","h8q5","h8q7","h8q9","h8q13", "urban","age"]]
data2.columns = ["hh", "paid", "busines", "non-paid", "farm", "urban", "age"]
data2 = data2.replace(['No', 'Yes', 'nan'], 
                     [0, 1, float('NaN')]).dropna()
#data2 = data2.merge(age, on="HHID", how="left")
dataurban = data2.loc[data2["urban"].isin([1]),["hh", "paid", "busines", "non-paid", "farm","age"]]
datarural = data2.loc[data2["urban"].isin([0]),["hh", "paid", "busines", "non-paid", "farm", "age"]]


dataurban = dataurban.groupby(by = "hh")[["paid", "busines", "non-paid", "farm"]].sum()
dataurban.reset_index(inplace=True)
dataurban = dataurban.merge(age, on='hh', how='left')
extensivelaboururban = dataurban[['hh',"paid", "busines", "non-paid", "farm", "age"]]
extensivelaboururban['totalextensiveurban']= extensivelaboururban["paid"]+extensivelaboururban["busines"]+extensivelaboururban["non-paid"]+extensivelaboururban["farm"]
extensivelaboururban.columns = ['HHID',"paid", "busines", "non-paid", "farm","age", "totalextensiveurban"]

extensivelaboururban = extensivelaboururban[['HHID','totalextensiveurban', 'age']]

datarural = datarural.groupby(by = "hh")[["paid", "busines", "non-paid", "farm"]].sum()
datarural.reset_index(inplace=True)
datarural = datarural.merge(age, on='hh', how='left')
extensivelabourrural = datarural[['hh',"paid", "busines", "non-paid", "farm", "age"]]
extensivelabourrural['totalextensiverural'] = extensivelabourrural["paid"]+extensivelabourrural["busines"]+extensivelabourrural["non-paid"]+extensivelabourrural['farm']
extensivelabourrural.columns = ["HHID","paid", "busines", "non-paid", "farm", "age","totalextensiverural"]
extensivelabourrural = extensivelabourrural[['HHID','totalextensiverural', 'age']]
#extensivelabourrural = extensivelabourrural['totalextensiverural']


#MAKING INTENSIVE
age.columns = ['HHID', 'age']
data = pd.read_stata("gsec8_1.dta")
data = data.merge(data1, on="HHID", how="left") 
data = data[["HHID","h8q36a","h8q36b","h8q36c","h8q36d","h8q36e","h8q36f","h8q36g", "urban"]].dropna()
dataurban = data.loc[data["urban"].isin([1]),["HHID","h8q36a","h8q36b","h8q36c","h8q36d","h8q36e","h8q36f","h8q36g"]]
datarural = data.loc[data["urban"].isin([0]),["HHID","h8q36a","h8q36b","h8q36c","h8q36d","h8q36e","h8q36f","h8q36g"]]

dataurban = dataurban.groupby(by = "HHID")[["h8q36a","h8q36b","h8q36c","h8q36d","h8q36e","h8q36f","h8q36g"]].sum()
datarural = datarural.groupby(by = "HHID")[["h8q36a","h8q36b","h8q36c","h8q36d","h8q36e","h8q36f","h8q36g"]].sum()
dataurban.reset_index(inplace=True)
datarural.reset_index(inplace=True)
datarural = datarural.merge(age, on='HHID', how='left')
dataurban = dataurban.merge(age, on='HHID', how='left')

intensivelaboururban = dataurban[['HHID']]
intensivelabourrural = datarural[['HHID']]
intensivelaboururban['totalinturban'] = dataurban['h8q36a']+dataurban['h8q36b']+dataurban['h8q36c']+dataurban['h8q36d']+dataurban['h8q36e']+dataurban['h8q36f']+dataurban['h8q36g']
intensivelabourrural['totalintrural'] = datarural['h8q36a']+datarural['h8q36b']+datarural['h8q36c']+datarural['h8q36d']+datarural['h8q36e']+datarural['h8q36f']+datarural['h8q36g']


#intensivelaboururban = dataurban.sum(axis=1)
#intensivelabourrural = datarural.sum(axis=1)
rural = intensivelabourrural.merge(extensivelabourrural,on="HHID", how="outer")

urban = intensivelaboururban.merge(extensivelaboururban,on="HHID", how="outer")


#%% QUESTION 2.1.1:

Iurban = intensivelaboururban[["totalinturban"]]
Irural = intensivelabourrural[["totalintrural"]]
Erural = extensivelabourrural[["totalextensiverural"]]
Eurban = extensivelaboururban[["totalextensiveurban"]]

sum_extensivelaboururban = Eurban.describe()
sum_extensivelabourrural = Erural.describe()
sum_intensivelaboururban = Iurban.describe()
sum_intensivelabourrural = Irural.describe()
print(sum_extensivelaboururban.to_latex())
print(sum_extensivelabourrural.to_latex())
print(sum_intensivelaboururban.to_latex())
print(sum_intensivelabourrural.to_latex())

#%% Question 2.1.2:
iu=np.asarray(Iurban)
ir=np.asarray(Irural)
eu=np.asarray(Eurban)
Er=np.asarray(Erural)

#Hist
plt.figure
plt.subplots_adjust(top=0.9, bottom=0, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('Extensive and Intensive Histograms')
bins=50 #Adjust the number of bins
bins2=75
plt.subplot(1,2,1)
plt.hist(ir, bins, alpha=0.5, label='Rural_I')
plt.hist(iu, bins, alpha=0.5, label='Urban_I')
#pyplot.hist(wu, bins, alpha=0.5, label='Wealth')
plt.xlim([0,10000])
plt.legend(loc='upper right')

plt.subplot(1,2,2)
plt.hist(eu, bins, alpha=0.5, label='Urban_E')
plt.hist(Er, bins2, alpha=0.5, color='r', label='Rural_E')
plt.xlim([0,200])
#pyplot.hist(wu, bins, alpha=0.5, label='Wealth')
plt.legend(loc='upper right')
plt.show()

Iurban = Iurban.replace(0, 1)
lnIurban = np.log(Iurban)
varIurban=  np.var(lnIurban)
Eurban = Eurban.replace(0, 1)
lnEurban = np.log(Eurban)
varEurban=  np.var(lnEurban)
Irural = Irural.replace(0, 1)
lnIrural = np.log(Irural) 
varIrural =  np.var(lnIrural)
Erural = Erural.replace(0, 1)
lnErural = np.log(Erural) 
varErural =  np.var(lnErural)

#%% Question 2.1.3: CROSS-SECTION:
#I remove 0 consumption people:
#urban = urban.groupby(by='HHID')[["totalinturban", "totalextensiveurban"]].sum()
#urban = urban.dropna()
#rural = rural.dropna()

#1- Correlations Matrix (CM)
CIW_R=rural[["totalintrural","totalextensiverural"]]
CM_R= CIW_R.corr()
print(CM_R.to_latex())

CIW_U=urban[["totalinturban","totalextensiveurban"]]
CM_U= CIW_U.corr()
print(CM_U.to_latex())

rural['totalintrural'] = rural['totalintrural'].fillna(0)

#2.- Joint density graphs
with sns.axes_style('white'):
    sns.jointplot("totalintrural", "totalextensiverural", rural, kind='kde', xlim=(-600,2000),ylim=(0,200));

with sns.axes_style('white'):
    sns.jointplot("totalinturban", "totalextensiveurban", urban, kind='kde',xlim=(-600,2000),ylim=(0,150));

# 2.2. GENDER ANALYSIS by education
%reset -sf #Clear all
import pandas as pd
import numpy as np
import os
import statsmodels.formula.api as sm
os.chdir('/Users/Boyao/Desktop/UAB/Development/PS1Final')
#from data_functions_albert import remove_outliers
os.chdir('/Users/Boyao/Desktop/UAB/Development/PS1Final')
from statsmodels.iolib.summary2 import summary_col
pd.options.display.float_format = '{:,.2f}'.format
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
dollars = 2586.89 

#uganda_2013_Q2 dataset is already normalized by dollar
data = pd.read_stata("uganda_2013_Q2.dta")
data['intensive'] = data['intensive'].fillna(0)
data['extensive'] = data['extensive'].fillna(0)
#data['inctotal'] = data['hh_ttincome_2013'].fillna(0)
female = data.loc[data["sex"]=='Female',["HHID","education","consumption","wealth","income","intensive","extensive"]]
female.columns = ['hh','education','f consumption','f wealth', 'f income','f intensive','f extensive']

#'''Less than primary is 0, primary is 1, and more or equal than secundary is 2 .
#Don't know is understood as less than primary.'''
female = female.replace(['No formal education (*OLD*)', 'Less than primary (*OLD*)', 
                           'Some schooling but not Completed P.1','DK','Completed P.1','Completed P.2'
                           ,'Completed P.3', 'Completed P.4', 'Completed P.5', 'Completed P.6','Completed P.7'
                           ,'Completed J.1', 'Completed J.2', 'Completed J.3', '	Completed primary (*OLD*)'
                           ,'Completed S.1', 'Completed S.2', 'Completed S.3', 'Completed S.4'
                           ,'Completed S.5', 'Completed S.6', 'Completed Post primary Specialized training or Certificate'
                           ,'Completed Post secondary Specialized training or diploma', 'Completed Degree and above'
                           , 'Some secondary', 'Some primary', 'Never attended school', 'Completed O-level (*OLD*)'
                           ,'Completed A-level (*OLD*)', 'Completed University (*OLD*)', 'Don\'t know (*OLD*)', 'Completed primary (*OLD*)', '	Other (Specify) (*OLD*)'], 
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 2, 0, 1, 0])

#group it by education for female
fEduclessPri = female.loc[female["education"]==0,["HHID","f consumption","f wealth","f income","f intensive","f extensive"]]
fEducComPri = female.loc[female["education"]==1,["HHID","f consumption","f wealth","f income","f intensive","f extensive"]]
fEducComSec = female.loc[female["education"]==2,["HHID","f consumption","f wealth","f income","f intensive","f extensive"]]
#female=female.groupby(by = "education")[["f consumption","f wealth","f income","intensive","extensive"]].sum()


#For male
Male = data.loc[data["sex"]=='Male',["HHID","education","consumption","wealth","income","intensive","extensive"]]
Male.columns = ['hh','education','m consumption','m wealth', 'm income','m intensive','m extensive']

Male = Male.replace(['No formal education (*OLD*)', 'Less than primary (*OLD*)', 
                           'Some schooling but not Completed P.1','DK','Completed P.1','Completed P.2'
                           ,'Completed P.3', 'Completed P.4', 'Completed P.5', 'Completed P.6','Completed P.7'
                           ,'Completed J.1', 'Completed J.2', 'Completed J.3', '	Completed primary (*OLD*)'
                           ,'Completed S.1', 'Completed S.2', 'Completed S.3', 'Completed S.4'
                           ,'Completed S.5', 'Completed S.6', 'Completed Post primary Specialized training or Certificate'
                           ,'Completed Post secondary Specialized training or diploma', 'Completed Degree and above'
                           , 'Some secondary', 'Some primary', 'Never attended school', 'Completed O-level (*OLD*)'
                           ,'Completed A-level (*OLD*)', 'Completed University (*OLD*)', 'Don\'t know (*OLD*)', 'Completed primary (*OLD*)', '	Other (Specify) (*OLD*)'], 
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 2, 0, 1, 0])

#Male=Male.groupby(by = "education")[["m consumption","m wealth","m income","intensive","extensive"]].sum()

#group it by education

mEduclessPri = Male.loc[Male["education"]==0,["HHID","m consumption","m wealth","m income","m intensive","m extensive"]]
mEducComPri = Male.loc[Male["education"]==1,["HHID","m consumption","m wealth","m income","m intensive","m extensive"]]
mEducComSec = Male.loc[Male["education"]==2,["HHID","m consumption","m wealth","m income","m intensive","m extensive"]]


#Now let's redo the first question for women and man
#female
cfemale = female[["f consumption"]]
cfemale = cfemale.dropna()
wfemale = female[["f wealth"]]
ifemale = female[["f income"]]
intfemale = female[["f intensive"]]
extfemale = female[["f extensive"]]
sum_fem=female[["f consumption","f wealth", "f income","f intensive","f extensive"]]
sum_fem=sum_fem.describe()
print(sum_fem.to_latex())


#male
cmale = Male[["m consumption"]]
wmale = Male[["m wealth"]]
imale = Male[["m income"]]
intmale = Male[["m intensive"]]
extmale = Male[["m extensive"]]
sum_fem=Male[["m consumption","m wealth", "m income","m intensive","m extensive"]]
sum_fem=sum_fem.describe()
print(sum_fem.to_latex())

###By education Group for female and male
###Female by education

#EduclessPri Education less than primary school
cfemaleEduclessPri = fEduclessPri[["f consumption"]]
wfemaleEduclessPri = fEduclessPri[["f wealth"]]
ifemaleEduclessPri = fEduclessPri[["f income"]]
intfemaleEduclessPri = fEduclessPri[["f intensive"]]
extfemaleEduclessPri = fEduclessPri[["f extensive"]]
sum_femfEduclessPri=fEduclessPri[["f consumption","f wealth", "f income","f intensive","f extensive"]]
sum_femfEduclessPri=sum_femfEduclessPri.describe()
print(sum_femfEduclessPri.to_latex())

#primary school completed
cfemaleEducComPri = fEducComPri[["f consumption"]]
wfemaleEducComPri = fEducComPri[["f wealth"]]
ifemaleEducComPri = fEducComPri[["f income"]]
intfemaleEducComPri = fEducComPri[["f intensive"]]
extfemaleEducComPri = fEducComPri[["f extensive"]]
sum_femfEducComPri=fEducComPri[["f consumption","f wealth", "f income","f intensive","f extensive"]]
sum_femfEducComPri=sum_femfEducComPri.describe()
print(sum_femfEducComPri.to_latex())

# secondary school completed or higher
cfemaleEducComSec = fEducComSec[["f consumption"]]
wfemaleEducComSec = fEducComSec[["f wealth"]]
ifemaleEducComSec = fEducComSec[["f income"]]
intfemaleEducComSec = fEducComSec[["f intensive"]]
extfemaleEducComSec = fEducComSec[["f extensive"]]
sum_femfEducComSec=fEducComSec[["f consumption","f wealth", "f income","f intensive","f extensive"]]
sum_femfEducComSec=sum_femfEducComSec.describe()
print(sum_femfEducComSec.to_latex())


###Male by education

#EduclessPri Education less than primary school
cmaleEduclessPri = mEduclessPri[["m consumption"]]
wmaleEduclessPri = mEduclessPri[["m wealth"]]
imaleEduclessPri = mEduclessPri[["m income"]]
intmaleEduclessPri = mEduclessPri[["m intensive"]]
extmaleEduclessPri = mEduclessPri[["m extensive"]]
sum_mEduclessPri=mEduclessPri[["m consumption","m wealth", "m income","m intensive","m extensive"]]
sum_mEduclessPri=sum_mEduclessPri.describe()
print(sum_mEduclessPri.to_latex())

#primary school completed
cmaleEducComPri = mEducComPri[["m consumption"]]
wmaleEducComPri = mEducComPri[["m wealth"]]
imaleEducComPri = mEducComPri[["m income"]]
intmaleEducComPri = mEducComPri[["m intensive"]]
extmaleEducComPri = mEducComPri[["m extensive"]]
sum_mEducComPri=mEducComPri[["m consumption","m wealth", "m income","m intensive","m extensive"]]
sum_mEducComPri=sum_mEducComPri.describe()
print(sum_mEducComPri.to_latex())

# secondary school completed or higher
cmaleEducComSec = mEducComSec[["m consumption"]]
wmaleEducComSec = mEducComSec[["m wealth"]]
imaleEducComSec = mEducComSec[["m income"]]
intmaleEducComSec = mEducComSec[["m intensive"]]
extmaleEducComSec = mEducComSec[["m extensive"]]
sum_mEducComSec=mEducComSec[["m consumption","m wealth", "m income","m intensive","m extensive"]]
sum_mEducComSec=sum_mEducComSec.describe()
print(sum_mEducComSec.to_latex())

# 2.2.1. INEQUALITY
#Convert to array
ife=np.asarray(ifemale)
cfe=np.asarray(cfemale)
wfe=np.asarray(wfemale)
cm=np.asarray(cmale)
im=np.asarray(imale)
wm=np.asarray(wmale)

plt.figure
plt.subplots_adjust(top=0.9, bottom=0, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('CIW Histograms by gender')
bins=25 #Adjust the number of bins

plt.subplot(2,2,1)
plt.hist(cfe, bins, alpha=0.5, label='Fem_C')
plt.hist(ife, bins, alpha=0.5, label='Fem_I')
plt.xlim([-20000,70000])
plt.legend(loc='upper right')

plt.subplot(2,2,2)
plt.hist(cfe, bins, alpha=0.5, label='Fem_C')
plt.hist(wfe, bins, alpha=0.5, color='r', label='Fem_W')
plt.xlim([-20000,70000])
plt.legend(loc='down left')

plt.subplot(2,2,3)
plt.hist(cm, bins, alpha=0.5,label='Male_C')
plt.hist(im, bins, alpha=0.5, label='Male_I')
plt.xlim([-20000,70000])
plt.legend(loc='upper right')

plt.subplot(2,2,4)
plt.hist(cm, bins, alpha=0.5, label='Male_C')
plt.hist(wm, bins, alpha=0.5, color='r', label='Male_W')
plt.xlim([-20000,70000])
plt.legend(loc='down right')
plt.show()

###By education

intfemaleEduclessPri=np.asarray(intfemaleEduclessPri)
intfemaleEducComPri=np.asarray(intfemaleEducComPri)
intfemaleEducComSec=np.asarray(intfemaleEducComSec)

intmaleEduclessPri=np.asarray(intmaleEduclessPri)
intmaleEducComPri=np.asarray(intmaleEducComPri)
intmaleEducComSec=np.asarray(intmaleEducComSec)

plt.figure
plt.subplots_adjust(top=0.9, bottom=0, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('Intensive Histograms Female by education')
bins=25 #Adjust the number of bins

plt.subplot(2,2,1)
plt.hist(intfemaleEduclessPri, bins, alpha=0.5, label='FIn_LessPri')
plt.hist(intfemaleEducComPri, bins, alpha=0.5, label='FIn_ComPri')
plt.hist(intfemaleEducComSec, bins, alpha=0.5, label='FIn_ComSec')
plt.xlim([-100,3000])
plt.legend(loc='upper right')

plt.subplot(2,2,2)
plt.hist(intmaleEduclessPri, bins, alpha=0.5, label='MIn_LessPri')
plt.hist(intmaleEducComPri, bins, alpha=0.5, label='MIn_ComPri')
plt.hist(intmaleEducComSec, bins, alpha=0.5, label='MIn_ComSec')
plt.xlim([-100,4000])
plt.legend(loc='upper right')


##Extensive by education

extfemaleEduclessPri=np.asarray(extfemaleEduclessPri)
extfemaleEducComPri=np.asarray(extfemaleEducComPri)
extfemaleEducComSec=np.asarray(extfemaleEducComSec)

extmaleEduclessPri=np.asarray(extmaleEduclessPri)
extmaleEducComPri=np.asarray(extmaleEducComPri)
extmaleEducComSec=np.asarray(extmaleEducComSec)

plt.figure
plt.subplots_adjust(top=0.9, bottom=0, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('Intensive Histograms Female by education')
bins=25 #Adjust the number of bins

plt.subplot(2,2,1)
plt.hist(extfemaleEduclessPri, bins, alpha=0.5, label='FEx_LessPri')
plt.hist(extfemaleEducComPri, bins, alpha=0.5, label='FEx_ComPri')
plt.hist(extfemaleEducComSec, bins, alpha=0.5, label='FEx_ComSec')
#plt.xlim([-100,3000])
plt.legend(loc='upper left')

plt.subplot(2,2,2)
plt.hist(extmaleEduclessPri, bins, alpha=0.5, label='MEx_LessPri')
plt.hist(extmaleEducComPri, bins, alpha=0.5, label='MEx_ComPri')
plt.hist(extmaleEducComSec, bins, alpha=0.5, label='MEx_ComSec')
#plt.xlim([-100,4000])
plt.legend(loc='upper left')



#ifemaleEduclessPri=np.asarray(ifemaleEduclessPri)
#wfemaleEduclessPri=np.asarray(wfemaleEduclessPri)
#intfemaleEduclessPri=np.asarray(intfemaleEduclessPri)
#extfemaleEduclessPri=np.asarray(extfemaleEduclessPri)

#cmaleEduclessPri=np.asarray(cmaleEduclessPri)
#imaleEduclessPri=np.asarray(imaleEduclessPri)
#wmaleEduclessPri=np.asarray(wmaleEduclessPri)
#intmaleEduclessPri=np.asarray(intmaleEduclessPri)
#extmaleEduclessPri=np.asarray(extmaleEduclessPri)

#2.2.2. VARIANCES
lncf = np.log(cfemale)
varcf =  np.var(lncf)
ifemale = ifemale.replace(0, 1)
lnif = np.log(ifemale)
varif =  np.var(lnif)
wfe = wfemale.replace(0, 1)
lnwf = np.log(wfe)
varwf =  np.var(lnwf)

lncm = np.log(cm)
varcm = np.var(lncm)
im = imale.replace(0, 1)
lnim = np.log(im)
im = lnim.fillna(0)
varim = np.var(lnim)
wm = wmale.replace(0, 1)
lnwm = np.log(wm)
wm = lnim.fillna(0)
varwm = np.var(lnwm)


#2.2.3. CROSS-SECTION
#1.-Correlation matrix
CIW_F=female[["f consumption","f wealth", "f income"]]
CM_F= CIW_F.corr()
print(CM_F.to_latex())

CIW_M=male[["m consumption","m wealth", "m income"]]
CM_M= CIW_M.corr()
print(CM_M.to_latex())

#2.- Joint density graphs
with sns.axes_style('white'):
    sns.jointplot("f income", "f consumption", female, kind='kde');

with sns.axes_style('white'):
    sns.jointplot("f income", "f wealth", female, kind='kde');

with sns.axes_style('white'):
    sns.jointplot("m income", "m consumption", male, kind='kde');

with sns.axes_style('white'):
    sns.jointplot("m income", "m wealth", male, kind='kde');
    

#QUESTION 2.2.4: LIFECYCLE CIW:

#Female
Female_data=data.loc[data["sex"]=='Female',["hh_consumption_year_2013","Total","hh_ttincome_2013","age"]]
A = Female_data.groupby(by = "age")[["hh_consumption_year_2013","Total","hh_ttincome_2013"]].mean()
A['age'] = A.index

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Age')
ax1.set_ylabel('CI', color=color)
ax1.plot(A['age'],A[['hh_consumption_year_2013']] , color='g',label='consumption')
ax1.plot(A['age'],A[['hh_ttincome_2013']] , color=color,label='income')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Wealth', color=color)  # we already handled the x-label with ax1
ax2.plot(A['age'],A[['Total']] , color=color, label='wealth')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.legend(loc='best')
plt.title('Female CIW life-cycle profile')
plt.show()


#Male
Male_data=data.loc[data["sex"]=='Male',["hh_consumption_year_2013","Total","hh_ttincome_2013","age"]]
A = Male_data.groupby(by = "age")[["hh_consumption_year_2013","Total","hh_ttincome_2013"]].mean()
A['age'] = A.index

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Age')
ax1.set_ylabel('CI', color=color)
ax1.plot(A['age'],A[['hh_consumption_year_2013']] , color='g',label='consumption')
ax1.plot(A['age'],A[['hh_ttincome_2013']] , color=color,label='income')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Wealth', color=color)  # we already handled the x-label with ax1
ax2.plot(A['age'],A[['Total']] , color=color, label='wealth')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.legend(loc='best')
plt.title('Male CIW life-cycle profile')
plt.show()

#2.2.5 EXTREME BEHAVIOUR
#Female
#Rank by income percentile
Female_data['inctotal'] = Female_data["hh_ttincome_2013"].replace(0,float('NaN'))
Female_data['I_Percentile_rank']=Female_data.inctotal.rank(pct=True)

#Get the consumption/wealth share of the income top and bottom 10%. 
#Consumption
C_bottom=Female_data.loc[Female_data["I_Percentile_rank"]<0.1,["hh_consumption_year_2013"]]
C_bottom_10share=C_bottom.sum()/Female_data["hh_consumption_year_2013"].sum()
C_top=Female_data.loc[Female_data["I_Percentile_rank"]>0.9,["hh_consumption_year_2013"]]
C_top_10share_F=C_top.sum()/Female_data["hh_consumption_year_2013"].sum()
#The bottom 10% consumes only about 6% and the top 10% about 12%. 

#Wealth
W_bottom=Female_data.loc[Female_data["I_Percentile_rank"]<0.1,["Total"]]
W_bottom_10share=W_bottom.sum()/Female_data["Total"].sum()
W_top=Female_data.loc[Female_data["I_Percentile_rank"]>0.9,["Total"]]
W_top_10share_F=W_top.sum()/Female_data["Total"].sum()


#Male
#Rank by income percentile
Male_data['inctotal'] = Male_data["hh_ttincome_2013"].replace(0,float('NaN'))
Male_data['I_Percentile_rank']=Male_data.inctotal.rank(pct=True)

#Get the consumption/wealth share of the income top and bottom 10%. 
#Consumption
C_bottom=Male_data.loc[Male_data["I_Percentile_rank"]<0.1,["hh_consumption_year_2013"]]
C_bottom_10share=C_bottom.sum()/Male_data["hh_consumption_year_2013"].sum()
C_top=Male_data.loc[Male_data["I_Percentile_rank"]>0.9,["hh_consumption_year_2013"]]
C_top_10share_M=C_top.sum()/Male_data["hh_consumption_year_2013"].sum()
#The bottom 10% consumes only about 6% and the top 10% about 12%. 

#Wealth
W_bottom=Male_data.loc[Male_data["I_Percentile_rank"]<0.1,["Total"]]
W_bottom_10share=W_bottom.sum()/Male_data["Total"].sum()
W_top=Male_data.loc[Male_data["I_Percentile_rank"]>0.9,["Total"]]
W_top_10share_M=W_top.sum()/Male_data["Total"].sum()


#3. REGIONAL INEQUALITY
#3.1. CWL agains income
import pandas as pd
import numpy as np
import os
import statsmodels.formula.api as sm
os.chdir('/Users/Boyao/Desktop/UAB/Development/PS1Final')
from data_functions_albert import remove_outliers
os.chdir('/Users/Boyao/Desktop/UAB/Development/PS1Final')
from statsmodels.iolib.summary2 import summary_col
pd.options.display.float_format = '{:,.2f}'.format
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
dollars = 2586.89 

data = pd.read_stata("Uganda.dta")

#Region 1
central = data.loc[data["region"]==1,["HHID","hh_consumption_year_2013","Total","hh_ttincome_2013","hh_laboursupply_year_2013"]]


plt.figure()
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('CWL Central Region')
plt.subplot(131)
plt.scatter(central["hh_ttincome_2013"], central["hh_consumption_year_2013"])
plt.xlabel('Income')
plt.ylabel('Consumption')

plt.subplot(132)
plt.scatter(central["hh_ttincome_2013"],central['Total'])
plt.xlabel('Income')
plt.ylabel('Wealth')

plt.subplot(133)
plt.scatter(central["hh_ttincome_2013"],central["hh_laboursupply_year_2013"])
plt.xlabel('Income')
plt.ylabel('Hours')
plt.show()



#Region 2
Eastern = data.loc[data["region"]==2,["HHID","hh_consumption_year_2013","Total","hh_ttincome_2013","hh_laboursupply_year_2013"]]

plt.figure()
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('CWL Eastern Region')
plt.subplot(131)
plt.scatter(Eastern["hh_ttincome_2013"], Eastern["hh_consumption_year_2013"])
plt.xlabel('Income')
plt.ylabel('Consumption')

plt.subplot(132)
plt.scatter(Eastern["hh_ttincome_2013"],Eastern['Total'])
plt.xlabel('Income')
plt.ylabel('Wealth')

plt.subplot(133)
plt.scatter(Eastern["hh_ttincome_2013"],Eastern["hh_laboursupply_year_2013"])
plt.xlabel('Income')
plt.ylabel('Hours')
plt.show()



#Region 3
Northern = data.loc[data["region"]==3,["HHID","hh_consumption_year_2013","Total","hh_ttincome_2013","hh_laboursupply_year_2013"]]

plt.figure()
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('CWL Northern Region')
plt.subplot(131)
plt.scatter(Northern["hh_ttincome_2013"],Northern["hh_consumption_year_2013"])
plt.xlabel('Income')
plt.ylabel('Consumption')

plt.subplot(132)
plt.scatter(Northern["hh_ttincome_2013"],Northern['Total'])
plt.xlabel('Income')
plt.ylabel('Wealth')

plt.subplot(133)
plt.scatter(Northern["hh_ttincome_2013"],Northern["hh_laboursupply_year_2013"])
plt.xlabel('Income')
plt.ylabel('Hours')
plt.show()

#Region 4 
Western = data.loc[data["region"]==4,["HHID","hh_consumption_year_2013","Total","hh_ttincome_2013","hh_laboursupply_year_2013"]]

plt.figure()
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('CWL Western Region')
plt.subplot(131)
plt.scatter(Western["hh_ttincome_2013"],Western["hh_consumption_year_2013"])
plt.xlabel('Income')
plt.ylabel('Consumption')

plt.subplot(132)
plt.scatter(Western["hh_ttincome_2013"],Western['Total'])
plt.xlabel('Income')
plt.ylabel('Wealth')

plt.subplot(133)
plt.scatter(Western["hh_ttincome_2013"],Western["hh_laboursupply_year_2013"])
plt.xlabel('Income')
plt.ylabel('Hours')
plt.show()





#3.2.INEQUALITY
i1=np.asarray(central["hh_ttincome_2013"])
i2=np.asarray(Eastern["hh_ttincome_2013"])
i3=np.asarray(Northern["hh_ttincome_2013"])
i4=np.asarray(Western["hh_ttincome_2013"])
c1=np.asarray(central["hh_consumption_year_2013"])
c2=np.asarray(Eastern["hh_consumption_year_2013"])
c3=np.asarray(Northern["hh_consumption_year_2013"])
c4=np.asarray(Western["hh_consumption_year_2013"])
w1=np.asarray(central["Total"])
w2=np.asarray(Eastern["Total"])
w3=np.asarray(Northern["Total"])
w4=np.asarray(Western["Total"])
h1=np.asarray(central["hh_laboursupply_year_2013"])
h2=np.asarray(Eastern["hh_laboursupply_year_2013"])
h3=np.asarray(Northern["hh_laboursupply_year_2013"])
h4=np.asarray(Western["hh_laboursupply_year_2013"])



plt.figure
plt.subplots_adjust(top=0.9, bottom=0, left=0.3, right=1.5, wspace=0.5)
plt.suptitle('CIWL Histograms')
bins=25 #Adjust the number of bins

plt.subplot(2,2,1)
plt.hist(i1, bins, alpha=0.5, label='inc_c')
plt.hist(i2, bins, alpha=0.5, label='inc_e')
plt.hist(i3, bins, alpha=0.5, label='inc_n')
plt.hist(i4, bins, alpha=0.5, label='inc_w')
plt.legend(loc='upper right')

plt.subplot(2,2,2)
plt.hist(c1, bins, alpha=0.5, label='con_c')
plt.hist(c2, bins, alpha=0.5, label='con_e')
plt.hist(c3, bins, alpha=0.5, label='con_n')
plt.hist(c4, bins, alpha=0.5, label='con_w')
plt.legend(loc='upper right')

plt.subplot(2,2,3)
plt.hist(w1, bins, alpha=0.5, label='w_c')
plt.hist(w2, bins, alpha=0.5, label='w_e')
plt.hist(w3, bins, alpha=0.5, label='w_n')
plt.hist(w4, bins, alpha=0.5, label='w_w')
plt.legend(loc='upper right')

plt.subplot(2,2,4)
plt.hist(h1, bins, alpha=0.5, label='h_c')
plt.hist(h2, bins, alpha=0.5, label='h_e')
plt.hist(h3, bins, alpha=0.5, label='h_n')
plt.hist(h4, bins, alpha=0.5, label='h_w')
plt.legend(loc='upper right')
plt.show()


#3.3. JOINT DISTRIBUTION

CIWL_c=central[["hh_consumption_year_2013","Total","hh_ttincome_2013","hh_laboursupply_year_2013"]]
CM_c= CIWL_c.corr()
print(CM_c.to_latex())

CIW_e=Eastern[["hh_consumption_year_2013","Total","hh_ttincome_2013","hh_laboursupply_year_2013"]]
CM_U= CIW_e.corr()
print(CM_U.to_latex())

CIW_n=Northern[["hh_consumption_year_2013","Total","hh_ttincome_2013","hh_laboursupply_year_2013"]]
CM_U= CIW_n.corr()
print(CM_U.to_latex())

CIW_w=Western[["hh_consumption_year_2013","Total","hh_ttincome_2013","hh_laboursupply_year_2013"]]
CM_U= CIW_w.corr()
print(CM_U.to_latex())
