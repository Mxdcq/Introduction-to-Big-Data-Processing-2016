# Python Web Scraping Tutorial using BeautifulSoup
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Parsing a page with BeautifulSoup
page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
print(page.status_code)
print(page.content)

soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify()) # return HTML format
print(list(soup.children))
print([type(item) for item in list(soup.children)])

html = list(soup.children)[2]
print(list(html.children))

body = list(html.children)[3]
print(list(body.children))

p = list(body.children)[1]
print(p.get_text())
print('\n')


# Finding all instances of a tag at once
soup2 = BeautifulSoup(page.content, 'html.parser')
print(soup2.find_all('p'))  # return a list
print(soup2.find_all('p')[0].get_text())
print(soup2.find('p'))  # return the first instance of a tag
print('\n')

# Searching for tags by class and id
page2 = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup3 = BeautifulSoup(page2.content, 'html.parser')
print(soup3)
print(soup3.find_all('p', class_='outer-text'))
print(soup3.find_all(class_='outer-text'))
print(soup3.find_all(id='first'))
print('\n')

# Using CSS Selectors
print(soup3.select('div p'))

# Downloading weather data
page_weather = requests.get('http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.WDDCVeF96Aw')
soup_weather = BeautifulSoup(page_weather.content, 'html.parser')
seven_day = soup_weather.find(id='seven-day-forecast')
forecast_items = seven_day.find_all(class_='tombstone-container')
tonight = forecast_items[2]
print(tonight.prettify())

period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()
print(period)
print(short_desc)
print(temp)

img = tonight.find('img')
desc = img['title']
print(desc)

# Extracting all the information from the page
period_tags = seven_day.select('.tombstone-container .period-name')
periods = [pt.get_text() for pt in period_tags]
short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
print(len(periods), periods)
print(len(short_descs), short_descs)
print(len(temps), temps)
print(len(descs), descs)

# Combining our data into a Pandas Dataframe
weather = pd.DataFrame({
    'period': periods[1:],
    'short_desc': short_desc[1:],
    'temp': temps,
    'desc': descs[1:]
})
print(weather)

# use a regular expression and the Series.str.extract method to pull out the numeric temperature values
temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
print(temp_nums)
# the mean of all the high and low temperatures
print(weather["temp_num"].mean())
# select the rows that happen at night
is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
print(is_night)
print(weather[is_night])