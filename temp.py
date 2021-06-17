
"""
CREATING FRAUDS
"""
import pandas as pd
import csv as csv 
import numpy as np
import random 
from datetime import datetime, date


"""Reading the file """

badguy=pd.read_excel("/Users/AngelicaGoglio/Documents/GitHub/dataset_LGZ0031833648.xlsx")   #Reading the excel file
badguy['date'] = pd.to_datetime(badguy['date']) #Converting argument to date and time
badguy = badguy.rename(columns={"active_imp": "power"})  #Changing name of the active power column into power 

original_df=badguy.copy()   #Creting a copy of tghe data

original_df = badguy.reset_index (drop=True) #Resetting the index starting from 0
original_df = original_df.rename(columns={'date':'date','SM':'smart meter'}) #Changing the name of column I will keep 

working_df = original_df.drop(['active_exp', 'r1','r2','r3', 'r4'], axis=1) #dropping the columns I don't need
working_df['date'] =  pd.to_datetime(working_df['date'], format = "%Y-%m-%d T%H:%M:%S") #Changing the format of the data
working_df ['day'] = working_df ['date'].apply(lambda x: x.strftime('%Y-%m-%d')) #Separating date from time
working_df ['time'] = working_df ['date'].apply(lambda x: x.strftime('%H:%M')) #Separating date from time
working_df = working_df.drop(['date'], axis=1) #Dropping the intial column date where I had both date and time



"""SELECT THE FRAUDULENT DAYS"""   #I need to select the days of the fraud so that I can remove and work only on a sub-dataset, which will be the fraudulent period

date_0 = '2020-06-07'      #SELECT STARTING DATE   #Beginning date for the fraud
date_f = '2020-06-10'      #SELECT ENDING DATE     #Final day of the fraud

fraud_df = working_df.loc[(working_df['day'] >= date_0) & (working_df['day'] <= date_f)]  #Extracting the sub-dataset
 
"""Modifying the days"""

#Now I will create the functions for the frauds. Each fraud will have a different function, based on the table in the paper "A Tunable Fraud Detection System for
#Advanced Metering Infrastructure Using Short-Lived Patterns". The total number of types of frauds is 6, each one will be define as FDI+ #fraud_type

g = random.uniform(0, 1) #This random number is outsdide FDI6 because it has to stay the same for each alteration
threshold = 0.2 #Threshold for FDI2  #Please select a threshold in kWh

#POSSIBLE TYPES OF FRAUDS

#List of all the definition of the frauds. As each function should iterate through the rows, the power is given also with the index #MARC IF YOU DON'T UNDERSTAND PLEASE TELL ME
#All the function return the fraudulent power

def FDI1():  #The modified power is half  of the original
    power_modify = 0.5*fraud_df['power'][index] 
    return (power_modify)

def FDI2(): #The modified power is subsitute with the threshold in case the original was higher than the threshold  
    if fraud_df['power'][index] >= threshold: 
        power_modify = threshold
    else:
        power_modify = fraud_df['power'][index]
    return (power_modify)

def FDI3():   #The modified power is given by substracting a constant from the original one
    constant = 0.1     #select constant in kWh
    power_modify = fraud_df['power'][index] - constant 
    return (power_modify)

def FDI4 (): #The modified power is set to zero
    power_modify = 0
    return (power_modify)

def FDI5 (): #The original power is given by modified by a different percentage
    p = random.uniform(0, 1)
    power_modify = (1-p)*fraud_df['power'][index]
    return (power_modify)
 
def FDI6 (): #multiplying the average consumption of previous month by a random percentage defined for each report
      power_modify = g*mean  #As i didn't "previous" months, I used the mean power
      return (power_modify )
  

  

df = pd.DataFrame(columns=['index','day','FD1','FD2','FD3','FD4','FD5','FD6']) #Creating a new data frame with all the frauds, later, depending on the chosen fraud, only one column will be kept



for  index,row in fraud_df.iterrows():  #iteration row by row. For each row the index, the date and the power will be read. THen the power will be used in the frauds. To call it the index has to be used
    
    index = index  #This is needed for the index column
    
    day = fraud_df['day'][index]    #This is needed to put the date in the dataframe

    mean = fraud_df['power'].mean()  #This is used for FDI6
    
    FD11 = FDI1()  #Calling the fraud 
    
    FD22 = FDI2()   #Calling the fraud 
   
    FD33 =FDI3()  #Calling the fraud 
    
    FD44 = FDI4() #Calling the fraud 
    
    FD55 = FDI5() #Calling the fraud 
    
    FD66 = FDI6() #Calling the fraud 
    
    df = df.append({'index':index,'day':day,'FD1':FD11,'FD2':FD22,'FD3':FD33,'FD4':FD44,'FD5':FD55,'FD6':FD66},
                      ignore_index=True)
df.set_index('index', drop= True, inplace=True)


    
def Final_fraud (type_of_fraud):   #This is the function that will keep only the column of the selected fraud
    if type_of_fraud == 'FD1':        
        final_df = df.drop(['FD2','FD3','FD4','FD5','FD6'], axis=1)
    if type_of_fraud == 'FD2':
        final_df = df.drop(['FD1','FD3','FD4','FD5','FD6'], axis=1)
    if type_of_fraud == 'FD3':
        final_df = df.drop(['FD1','FD2','FD4','FD5','FD6'], axis=1)
    if type_of_fraud == 'FD4':
        final_df = df.drop(['FD1','FD2','FD3','FD5','FD6'], axis=1)
    if type_of_fraud == 'FD5':
        final_df = df.drop(['FD1','FD2','FD3','FD4','FD6'], axis=1)
    if type_of_fraud == 'FD6':
        final_df = df.drop(['FD1','FD2','FD3','FD4','FD5'], axis=1)
    return(final_df)


"""KEEP ONLY THE FRAUD YOU WANT"""

type_of_fraud = 'FD'+str(6)   #Selecting the fraud by placing he number you want 

final_fraudulent_df = Final_fraud(type_of_fraud)  #Calling the function

final_final_fraudulent_df= final_fraudulent_df.drop(['day'], axis = 1)  #Dropping the day as there is already the column day in the original (working_df) dataframe



"Creating the final dataframe"

complete_df =pd.concat( [working_df,final_final_fraudulent_df], axis = 1)  #Final dataframe merging the original one (working_df) and the fraudulent one

complete_df[type_of_fraud] = complete_df[type_of_fraud].fillna(complete_df['power']) #Marc you know
        
# export_df.to_excel ('fraudulent_LGZ0031833648.xlsx', index = True)














 
      
    

