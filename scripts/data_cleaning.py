from tkinter import Y
import pandas as pd
import pandas as pd
import re
import sys
import numpy as np
from datetime import datetime,timedelta,date
from geopy.geocoders import Nominatim
from geopy import distance
from sklearn.preprocessing import LabelEncoder
import holidays

class DataCleaning:
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="gokada",timeout=None)
        self.nigeria_holiday= holidays.Nigeria()
        print('DataCleaning module')
        print('Dataset Clearning Module')
    #Function to drop columns with zero values

    def drop_rows(self, df,col1,col2):
        df_new= df.drop(df[(df[col1] == 0) & (df[col2] == 0)].index)
        return df_new

    # Calculating skewness of each column 
    def calculating_skewness(self,df):
        df.skew(axis='index', skipna=True)

   #Function to drop columns missing descriptive data that is unpredictable
    def drop_missing(self,df,col):
        df_dropped= df.dropna(subset=[col])
        return df_dropped.shape

    # Functions to backward fill and forward fill columns  
    def fix_missing_ffill(self,df, col):
        df[col] = df[col].fillna(method='ffill',axis = 1)
        return df[col]


    def fix_missing_bfill(self,df, col):
        df[col] = df[col].fillna(method='bfill')
        return df[col]
    # Functions to fill missing columns with mean, median, mode
    #using median
    def fix_missing_median(self,df):
        df_Med=df['Column'].fillna(df['column'].median(), inplace=True)
        return df_Med
  
    # Using mean
    def fix_missing_mean(self,df):
        df_mean=df['column'].fillna(int(df['column'].mean()), inplace=True)
        return df_mean
  
    # Using mode
    def fix_missing_mode(self,df):
        df_mode=df['column'].fillna(int(df['Salary'].mode()), inplace=True)
        return df_mode
    # By Interpolation
    def fix_missing_interpolation_fffil(self,df):
        df_clean = df.interpolate(method='ffill')
        return df_clean

    def fix_missing_interpolation(self,df):  
        df_cleann = df.interpolate(method='bfill')
        return df_cleann
    
    def spliter(self,text:str,ind:int=-4):
        try:
            text=text.split(',')[ind]
            return text 
        except Exception:
            if ind > 1:
                print("Error occured")
                sys.exit(1)
            else:
                ind+=1
                return self.spliter(text,ind)

    def reverse_location(self,df:pd.DataFrame,lat_col_name:str="Trip_Origin_lat",
                           lng_col_name:str="Trip_Origin_lng",loc_col_name:str="location"):
        locator = self.geolocator
        df[loc_col_name] = df.apply(
            lambda x:str(locator.reverse(str(x[lat_col_name])+","+str(x[lng_col_name]))),
               axis=1)
        df[loc_col_name] = df[loc_col_name].apply(lambda x:self.spliter(x))
        return df
    def check_holiday(self,order_time:datetime):
        return order_time.date() in self.nigeria_holiday

    def add_holiday_feature(self,df:pd.DataFrame,date_col:str="Trip Start Time"):
        df["holiday"]=df[date_col].apply(lambda x:self.check_holiday(x))
        return df
    def find_distance(self,df:pd.DataFrame,distance_col_name:str="distance",trip_origin_col_names:list=["trip_origin"],trip_destination_col_names:list=["trip_destination"]):
        if len(trip_destination_col_names) > 1 and len(trip_origin_col_names) > 1:
            df[distance_col_name]=df.apply(lambda x:distance.distance((x[trip_origin_col_names[0]],x[trip_origin_col_names[1]]), (x[trip_destination_col_names[0]],x[trip_destination_col_names[1]])).km,axis=1)
        else:
            df[distance_col_name]=df.apply(lambda x:distance.distance((x[trip_origin_col_names[0]]), (x[trip_destination_col_names[0]])).km,axis=1)
        return 