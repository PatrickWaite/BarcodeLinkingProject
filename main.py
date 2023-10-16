#imports for project 
from sqlalchemy import create_engine, text
import pandas as pd
from tkinter import filedialog as fd
from dbConnect import get_connectionString
from queries import get_barcodeData
import os
from datetime import datetime


def connAndCall(query):
    try:
# GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
        engine = create_engine(url=get_connectionString()) #pull connection string from dbConnect.py so that connection isn't hard coded in main file
        print(f"Connection created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error:", ex)
        
        #create connection and execute query from quries.py
    with engine.connect() as conn:
        #Note call the text() from sqlachemy to turn the text string result from get_inventoryQuery() into an executable SQL
        #df_queryResults = pd.DataFrame(conn.execute(text(get_CreateQuery())))
        df = pd.DataFrame(conn.execute(text(query)))
        return df
        #return q
        #print(df)

def pullBarcode():
    BarcodeString = fd.askopenfilename()
    barcodeList = pd.read_excel(BarcodeString)
    return barcodeList

def output(dataframe):
    #check to see if output path exists
    outputDir = './BarcodeOutput' #define output folder, should it not exist it will be created 
    isExist = os.path.exists(outputDir)
    print(isExist)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(outputDir)
        print("The new directory is created!")
#save dataframe outputs to output directory with a date
    date = datetime.now()
    dt = date.strftime("%d%m%Y")
    #print(FT['personal__last_name'].value_counts())
    dataframe.to_csv(f'{outputDir}/ZAP_Proccessed_barcode_output{dt}.csv')
    dataframe.to_excel(f'{outputDir}/ZAP_Processed_barcode_output{dt}.xlsx')
    print({outputDir})


def main():
    #bring in the provided list of barcode
    df = pullBarcode()
    print(df.keys())

    #makes the barcode list into a parseable list for pandas 
    barcode = df['BARCODE'].astype(str).tolist()
    black = df.rename(columns={'BARCODE':'barcode'}) ##this may be needed 
    strList = str(barcode).replace('[','').replace(']','')

    #make the calls to the database
    d = pd.DataFrame(connAndCall(get_barcodeData(strList)))


    #we need to remember to standardize the datatype of barcode on the upload file so that the merge/cat can happen correctly else program cant compare str with non-str values. 
    black['barcode'] = black['barcode'].astype('str')

    mergecat1 = black.merge(d, how="outer",left_on='barcode',right_on='barcode')

    output(mergecat1)

    print('Process Finished')

if __name__ == '__main__':
    main()