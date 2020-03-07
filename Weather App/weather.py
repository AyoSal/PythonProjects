# Python program to find current 
# weather details of any city 
# using openweathermap api and share with user via twilio api

# import required modules 
import requests, json, pytemperature, datetime

from datetime import date, datetime, timedelta, timezone
date1 = date.today()
# Enter your API key here 
api_key = "8b154a3d84fdf70745bdcf69f2ce39bf"

# base_url variable to store url 
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name 
city_name = input("Enter city name : ") 

# complete_url variable to store 
# complete url address 
complete_url = base_url + "appid=" + api_key + "&q=" + city_name 

# get method of requests module 
# return response object 
response = requests.get(complete_url) 

# json method of response object 
# convert json format data into 
# python format data 
x = response.json() 

# Now x contains list of nested dictionaries 
# Check the value of "cod" key is equal to 
# "404", means city is found otherwise, 
# city is not found 
if x["cod"] != "404": 

	# store the value of "main" 
	# key in variable y 
	y = x["main"] 

	# store the value corresponding 
	# to the "temp" key of y 
	current_temperature = y["temp"] 

pyt = pytemperature.k2c(current_temperature)
pyx =str(round(pyt, 2))
print(pyx)    
	# store the value corresponding 
	# to the "pressure" key of y 
#	current_pressure = y["pressure"] 

	# store the value corresponding 
	# to the "humidity" key of y 
#	current_humidiy = y["humidity"] 

	# store the value of "weather" 
	# key in variable z 
z = x["weather"] 

	# store the value corresponding 
	# to the "description" key at 
	# the 0th index of z 
weather_description = z[0]["description"]


	# print following values 
print(" Temperature (in celsius unit) = " +
					str(pyx) +

		"\n description = " +
					str(weather_description)) 

#else: 
#	print(" City Not Found ") 


from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("ACXXXXX", "cXXXXX")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="+14377741007",
                       from_="+1205740-2281",
                       body="Good Morning Ayo! Your weather update for today " + str(date1) + " in" + str(city_name) + " is " + str(pyx) + " degrees, Pls note there'll be " + str(weather_description) + " Ayos code is Slick!!")
