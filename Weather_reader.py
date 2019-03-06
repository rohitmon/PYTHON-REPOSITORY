#TODO: draw the different images for the current conditions - I have not started this yet.

#! python

# Lets import some required libraries that will be used to gather and display the information.
import urllib
# from urllib.request import urlopen
import json

# Import the libraries for the Waveshare 2.7" ePaper screen
import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

# Get and load the weather data from my house weather station.
weatherdata = urllib.urlopen("http://api.wunderground.com/api/<YOUR API KEY HERE>/conditions/q/pws:<YOUR LOCATION HERE>.json")
weathertemp = weatherdata.read()
weatherinfo = json.loads(weathertemp.decode())

# This gets the data regarding the sun and moon phases and rises/sets.
astrodata = urllib.urlopen("http://api.wunderground.com/api/<YOUR API KEY HERE>/astronomy/q/pws:<YOUR LOCATION HERE>.json")
astrotemp = astrodata.read()
astroinfo = json.loads(astrotemp.decode())

# Get information on any active alerts in the area.
alertdata = urllib.urlopen("http://api.wunderground.com/api/<YOUR API KEY HERE>/alerts/q/pws:<YOUR LOCATION HERE>.json")
alerttemp = alertdata.read()
alertinfo = json.loads(alerttemp.decode())

# Make the Trend data human format
if weatherinfo['current_observation']['pressure_trend'] == '+':
    WeatherTrend_st = 'upwards'
elif weatherinfo['current_observation']['pressure_trend'] == '-':
    WeatherTrend_st = 'downwards'
elif weatherinfo['current_observation']['pressure_trend'] == '0':
    WeatherTrend_st = 'constant'
elif weatherinfo['current_observation']['pressure_trend'] == '':
    WeatherTrend_st = 'N/C'

# Display the information to the ePaper screen.
try:
    # Set up the driver information.
    epd = epd2in7.EPD()
    epd.init()
    epd.Clear(0xFF)

    # Set up the ePaper for receiving information.
    Himage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    font10 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 10)
    
    # Format all the data in a readable format.
    print("Weather Info is about to display")
    draw.rectangle((0, 0, 263, 175), outline = 0)
    draw.text((3, 0), "Location: " + weatherinfo['current_observation']['observation_location']['full'], font = font10, fill = 0)
    draw.text((3, 14), weatherinfo['current_observation']['observation_time'], font = font10, fill = 0)
    draw.line((0, 25, 263, 25), fill = 0)
    draw.text((3, 26), "Conditions: " + weatherinfo['current_observation']['weather'] + " | Visibility: " + weatherinfo['current_observation']['visibility_mi'] + " miles.", font = font10, fill = 0)
    draw.text((3, 38), "Temperature: " + weatherinfo['current_observation']['temperature_string'] + " | Feels Like: " + weatherinfo['current_observation']['feelslike_string'], font = font10, fill = 0)
    draw.text((3, 50), "Heat Index: " + weatherinfo['current_observation']['heat_index_string'] + " | Wind Chill: " + weatherinfo['current_observation']['windchill_string'], font = font10, fill = 0)
    draw.text((3, 62), "Dew Point: " + weatherinfo['current_observation']['dewpoint_string'] + " | Humidity: " + weatherinfo['current_observation']['relative_humidity'], font = font10, fill = 0)
    draw.text((3, 74), "Rainfall: " + weatherinfo['current_observation']['precip_today_string'] + " | Wind: " + weatherinfo['current_observation']['wind_string'], font = font10, fill = 0)
    draw.text((3, 86), "Pressure: " + weatherinfo['current_observation']['pressure_in'] + ", trending: " + WeatherTrend_st, font = font10, fill = 0)
    draw.line((0, 97, 263, 97), fill = 0)
    draw.text((3, 98), "Sunrise: " + astroinfo['sun_phase']['sunrise']['hour'] + ":" + astroinfo['sun_phase']['sunrise']['minute'] + " | Sunset: " + astroinfo['sun_phase']['sunset']['hour'] + ":" + astroinfo['sun_phase']['sunset']['minute'], font = font10, fill = 0)
    draw.text((3, 110), "Moonrise: " + astroinfo['moon_phase']['moonrise']['hour'] + ":" + astroinfo['moon_phase']['moonrise']['minute'] + " | Moonset: " + astroinfo['moon_phase']['moonset']['hour'] + ":" + astroinfo['moon_phase']['moonset']['minute'], font = font10, fill = 0)
    draw.text((3, 122), "Moon Phase: " + astroinfo['moon_phase']['phaseofMoon'], font = font10, fill = 0)
    draw.text((3, 134), "Moon Illuminaion: " + astroinfo['moon_phase']['percentIlluminated'] + " %", font = font10, fill = 0)
    draw.line((0, 145, 263, 145), fill = 0)
    if 'type' in alertinfo:
        draw.text((3, 146), alertinfo['alerts']['description'], font = font10, fill = 0)
        draw.text((3, 158), alertinfo['alerts']['expires'], font = font10, fill = 0)
        draw.text((3, 170), alertinfo['alerts']['message'], font = font10, fill = 0)
    else:
        draw.text((3, 146), "No weather alerts or notices for this region at this time.", font = font10, fill = 0)
    
    # Grab the image for the current conditions and draw it onto the screen.
    currentimg = weatherinfo['current_observation']['icon_url']
    img_condition = re.split('\/', currentimg)[-1]
    condition_image = "/home/pi/epaper/python2/icons/" + img_condition[:-4] + ".bmp"
    bmp = Image.open(condition_image)
    Weatherimage.paste(bmp, (210, 47))
    epd.display(epd.getbuffer(Himage))
    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s' % traceback.format_exc())
    exit()