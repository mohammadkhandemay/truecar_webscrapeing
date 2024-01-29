# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:35:35 2023

@author: mohammad
"""
import mysql.connector
from bs4 import BeautifulSoup
import requests
price=list()
mileage=list()

cnx=mysql.connector.connect(user='root',password='12345',host='127.0.0.1',database='learn')
cursor=cnx.cursor()
cursor.execute('DROP TABLE IF EXISTS cars;')
cursor.execute('CREATE TABLE cars(price varchar(20), mileage varchar(20));')

base_url='https://www.truecar.com/used-cars-for-sale/listings/'
make=input('Please enter the manufacturer name:')
model=input('Please enter the model name:')
url=base_url + make + '/' + model + '/'

page=requests.get(url)
soup=BeautifulSoup(page.text,'html.parser')
part=soup.find_all('div',attrs={'card-content order-3 vehicle-card-body'})
        

for i in part:
    #get price
    item=i.find('div',attrs={'vehicle-card-bottom vehicle-card-bottom-top-spacing'})
    item2=item.find('div',attrs={'vehicle-card-bottom-pricing flex w-full justify-between'})
    item3=item2.find('div',attrs={'vehicle-card-bottom-pricing-secondary pl-3 lg:pl-2 vehicle-card-bottom-max-50'})
    item4=item3.find('div',attrs={'heading-3 normal-case my-1 font-bold'})
    p=item3.text
    p=p.split('$')
    price.append(p[-1])
    
    
    #get mileage
    use=i.find('div',attrs={'mt-2-5 w-full border-t pt-2-5'})
    use2=use.find('div',attrs={'truncate text-xs'})
    mileage.append(use2.text[:-6])
#put info in table
for j in range(20):
    cursor.execute("INSERT INTO cars VALUES (%s,%s)",(price[j],mileage[j]))

cnx.commit()
cnx.close()                  