
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Function to calculate missing values by column
def missing_values_table(df):
    # Total missing values
    mis_val = df.isnull().sum()

    # Percentage of missing values
    mis_val_percent = 100 * df.isnull().sum() / len(df)

    # dtype of missing values
    mis_val_dtype = df.dtypes

    # Make a table with the results
    mis_val_table = pd.concat([mis_val, mis_val_percent, mis_val_dtype], axis=1)

    # Rename the columns
    mis_val_table_ren_columns = mis_val_table.rename(
    columns = {0 : 'Missing Values', 1 : '% of Total Values', 2: 'Dtype'})

    # Sort the table by percentage of missing descending
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
    '% of Total Values', ascending=False).round(1)

    # Print some summary information
    print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
        "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")

    # Return the dataframe with missing information
    return mis_val_table_ren_columns

def split_date(df, column):
    df['Date'] = pd.to_datetime(df[column])
    df['Year'] = df.Date.dt.year
    df['Month'] = df.Date.dt.month
    df['Day'] = df.Date.dt.day
    df['WeekOfYear'] = df.Date.dt.isocalendar().week
    df["Day of Week"] = df.Date.dt.dayofweek
    df["Is Weekend"] = df.Date.dt.dayofweek > 4
    df['dayofweek'] = df.Date.dt.day_name()
    # df['Is Weekend'].replace({False: 0, True: 1}, inplace=True)

def label_encoder(df:pd.DataFrame,columns:list=None):
    if columns == None:
        # columns = df.select_dtypes(exclude = ['number','datetime'])
        columns = df.select_dtypes(exclude = ['number'])
    le = LabelEncoder()

    for col in columns:
        df[col] = le.fit_transform(df[col])

    return df