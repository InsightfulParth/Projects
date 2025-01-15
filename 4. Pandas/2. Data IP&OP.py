df.to_csv('C:\\Users\\admin\\Desktop\\D S files\\csv_example.csv',index=False)
s = pd.read_csv('C:\\Users\\admin\\Desktop\\D S files\\csv_example.csv')
print(s)
df = pd.read_csv('C:/Users/Admin/Desktop/Whatsapp/WhatsApp Chat with Rohit Patel.csv',usecols=['Sr. No.','Sent by','Description'],index_col=[0])

df.to_excel('C:\\Users\\admin\\Desktop\\D S files\\excel_example.xlsx',sheet_name='NewSheet')
a = pd.read_excel('C:\\Users\\admin\\Desktop\\D S files\\excel_example.xlsx',sheet_name='NewSheet')
print(a)

Data = pd.read_html('https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/')
print(type(Data))
print(Data)

#HTML
import pandas as pd
l = pd.read_html('https://www.aidtm.ac.in/en/Academics/BigData')
l[0]


Data = pd.read_html('https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/')
print(type(Data))
print(Data)

