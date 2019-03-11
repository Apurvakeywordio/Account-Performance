import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile 
 
 
xls=pd.ExcelFile("Account.xlsx")
   
df1=pd.read_excel(xls, 'Sheet1')
df2=pd.read_excel(xls, 'Sheet2')
listOfNames=df1["Name"].tolist()
df2=df2.loc[:,["Name","ConversionRate"]]
previous_ConversionRate_list=df2['ConversionRate'].tolist()
df1=df1.loc[:,["Name","ConversionRate"]]
latest_ConversionRate_list=df1['ConversionRate'].tolist()
    
    

new_data=pd.DataFrame({
    'Name':listOfNames,
    'Latest ValuePerConversion':latest_ConversionRate_list,
    'Previous ValuePerConversion': previous_ConversionRate_list,

})
writer = ExcelWriter('rate.xlsx')
new_data.to_excel(writer,'ConversionRate_Performance',index=None)
writer.save()
    

