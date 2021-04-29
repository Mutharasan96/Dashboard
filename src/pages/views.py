from django.shortcuts import render
from django.http import HttpResponse

import csv
import pandas as pd
import os
import glob

def readfile():
    global rows,columns,data,read_file,missing_values

    # with open('media\MarketWatch.csv','r') as myfile:
    #     reader = csv.reader(myfile)
    #     for i in range(10):
    #         print(reader.__next__())
    pwd = os.getcwd()
    file_directory = pwd+'\media\\'
    csv_file = glob.glob(file_directory+'*.csv')[0]
    read_file= pd.read_csv(csv_file,sep=',',
    engine='python',
    usecols=lambda x: x in ['Security Name','Open','High'],
    skiprows = lambda x:x>10)
    
    data = pd.DataFrame(data=read_file)
    rows= len(data.axes[0])
    columns = len(data.axes[1])

    missingsigns = ['?','--']
    null_data = data[data.isnull().any(axis=1)]
    missing_values = len(null_data)    


# Create your views here.
def home_view(request,*args, **kwargs):
    readfile()
    message = f"I found {str(rows)} rows and {str(columns)} columns. Missing data are: {str(missing_values)}"
    

    # Split data into keys and value
    listKeys=[]
    listopenvalues=[]
    for x in data["Security Name"]:
        listKeys.append(x)

    for x in data["Open"]:
        listopenvalues.append(x)

    context = {
        "messages": message,
        "listKeys": listKeys,
        "listopenvalues":listopenvalues
    }
    
    return render(request,"pages/home.html",context)
