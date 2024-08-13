"""
Peter Kieu, email:pckieu@cougarnet.uh.edu , PSID: 1916075
"""
import csv

"""
read_file function will access only .csv files and extract the weather data
it grabs these files from my working directory I set inside the main().
"""
def read_file(file_names):
    # Initialize list to store weather data for each year
    weather_data = [] 
    for file_name in file_names:
        # Initialize variables to store weather metrics for each file
        total_days = 0
        total_temp = 0
        total_min_temp = float('inf')
        total_max_temp = float('-inf')
        total_rainfall = 0
        total_wind = 0
        total_humidity = 0
        total_pressure = 0
        hot_days = 0
        rainy_days = 0
        sunny_days = 0
        
        # Open the CSV file and read its contents
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Extract relevant data from the files row
                temp_9am = float(row['temp9am']) if row['temp9am'] != 'Blank' else None
                temp_3pm = float(row['temp3pm']) if row['temp3pm'] != 'Blank' else None
                rainfall = float(row['rainfall']) if row['rainfall'] != 'Blank' else None
                wind_speed_9am = float(row['wind_speed9am']) if row['wind_speed9am'] != 'Blank' else None
                wind_speed_3pm = float(row['wind_speed3pm']) if row['wind_speed3pm'] != 'Blank' else None
                humidity_9am = float(row['humidity9am']) if row['humidity9am'] != 'Blank' else None
                humidity_3pm = float(row['humidity3pm']) if row['humidity3pm'] != 'Blank' else None
                pressure_9am = float(row['pressure9am']) if row['pressure9am'] != 'Blank' else None
                pressure_3pm = float(row['pressure3pm']) if row['pressure3pm'] != 'Blank' else None
                cloud_9am = row['cloud9am']
                cloud_3pm = row['cloud3pm']
                
                # Check for missing values or Blank values
                if any(value is None for value in [temp_9am, temp_3pm, rainfall, wind_speed_9am, wind_speed_3pm,
                                                    humidity_9am, humidity_3pm, pressure_9am, pressure_3pm]):
                    continue  # Skip the row if any value is missing or 'Blank'
                
                # Calculate daily averages
                daily_temp = (temp_9am + temp_3pm) / 2
                daily_rainfall = rainfall
                daily_wind = (wind_speed_9am + wind_speed_3pm) / 2
                daily_humidity = (humidity_9am + humidity_3pm) / 2
                daily_pressure = (pressure_9am + pressure_3pm) / 2
                
                # Update total metrics
                total_days += 1
                total_temp += daily_temp
                total_rainfall += daily_rainfall
                total_wind += daily_wind
                total_humidity += daily_humidity
                total_pressure += daily_pressure
                
                # Update minimum and maximum temperatures
                if daily_temp > total_max_temp:
                    total_max_temp = daily_temp
                if daily_temp < total_min_temp:
                    total_min_temp = daily_temp
                
                # Check for hot days
                if daily_temp >= 85:
                    hot_days += 1
                
                # Check for rainy days
                if daily_rainfall > 0:
                    rainy_days += 1
                
                # Check for sunny days
                if cloud_9am in ['Fair', 'Partly Cloudy'] or cloud_3pm in ['Fair', 'Partly Cloudy']:
                    sunny_days += 1
        
        # Calculate average metrics for the current year
        avg_temp = total_temp / total_days
        avg_rainfall = total_rainfall / total_days
        avg_wind = total_wind / total_days
        avg_humidity = total_humidity / total_days
        avg_pressure = total_pressure / total_days
        p_hot = hot_days / total_days
        p_rain = rainy_days / total_days
        p_sunshine = sunny_days / total_days
        
        # Create dictionary containing weather metrics for the current year
        weather_metrics = {
            'a_temp': avg_temp,
            'a_min_temp': total_min_temp,
            'a_max_temp': total_max_temp,
            'a_rainfall': avg_rainfall,
            'a_wind': avg_wind,
            'a_humidity': avg_humidity,
            'a_pressure': avg_pressure,
            'p_hot': p_hot,
            'p_rain': p_rain,
            'p_sunshine': p_sunshine
        }
        
        weather_data.append(weather_metrics)
    
    return weather_data

# data variable is the output value of read_file function

"""
process_wind function grabs average of the total summation of wind speeds
in the respective year file.
"""
def process_wind(data):
    avg_wind_per_year = []
    for year_data in data:
        avg_wind_per_year.append(year_data['a_wind'])
    return avg_wind_per_year

"""
process_sun function grabs the average sunshine amount 
for each year.
"""
def process_sun(data):
    sunshine_ratios = [year_data['p_sunshine'] for year_data in data]
    return min(sunshine_ratios), max(sunshine_ratios)

"""
process_temperature function takes in the average, minimum, maximum, hot day ratio
from each years' weather file 
"""
def process_temperature(data):
    avg_temperatures = [year_data['a_temp'] for year_data in data]
    min_temperatures = [year_data['a_min_temp'] for year_data in data]
    max_temperatures = [year_data['a_max_temp'] for year_data in data]
    hot_day_ratios = [year_data['p_hot'] for year_data in data]
    return avg_temperatures, min_temperatures, max_temperatures, hot_day_ratios


"""
Does the samething as read_file function but it has two return values
cold and warm, this function acquires the date information and checks
if the current data is in a warm or cold month. The data gets stored into
the cold or warm list.
"""
def read_file_2(file_names):
    # Initialize list to store weather data for each year
    weather_data_warm = []
    weather_data_cold = []
    season = 'warm'
    total_days_w = 0
    total_temp_w = 0
    total_min_temp_w = float('inf')
    total_max_temp_w = float('-inf')
    total_rainfall_w = 0
    total_wind_w = 0
    total_humidity_w = 0
    total_pressure_w = 0
    hot_days_w = 0
    rainy_days_w = 0
    sunny_days_w = 0
    
    total_days_c = 0
    total_temp_c = 0
    total_min_temp_c = float('inf')
    total_max_temp_c = float('-inf')
    total_rainfall_c = 0
    total_wind_c = 0
    total_humidity_c = 0
    total_pressure_c = 0
    hot_days_c = 0
    rainy_days_c = 0
    sunny_days_c = 0
    
    for file_name in file_names:
        # Open the CSV file and read its contents
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Extract relevant data from the files row
                date = row['date']
                year, month, day = map(int, date.split('-'))
                temp_9am = float(row['temp9am']) if row['temp9am'] != 'Blank' else None
                temp_3pm = float(row['temp3pm']) if row['temp3pm'] != 'Blank' else None
                rainfall = float(row['rainfall']) if row['rainfall'] != 'Blank' else None
                wind_speed_9am = float(row['wind_speed9am']) if row['wind_speed9am'] != 'Blank' else None
                wind_speed_3pm = float(row['wind_speed3pm']) if row['wind_speed3pm'] != 'Blank' else None
                humidity_9am = float(row['humidity9am']) if row['humidity9am'] != 'Blank' else None
                humidity_3pm = float(row['humidity3pm']) if row['humidity3pm'] != 'Blank' else None
                pressure_9am = float(row['pressure9am']) if row['pressure9am'] != 'Blank' else None
                pressure_3pm = float(row['pressure3pm']) if row['pressure3pm'] != 'Blank' else None
                cloud_9am = row['cloud9am']
                cloud_3pm = row['cloud3pm']
                
                # Check for missing values or Blank values
                if any(value is None for value in [temp_9am, temp_3pm, rainfall, wind_speed_9am, wind_speed_3pm,
                                                    humidity_9am, humidity_3pm, pressure_9am, pressure_3pm]):
                    continue  # Skip the row if any value is missing or 'Blank'
                
                    
                # Determine the season based on the month's value
                if 3 <= month <= 10:
                    season = 'warm'
                elif 1 <= month <= 2:
                    season = 'cold'
                    
                # acquire the weather data between warm and cold seasons  
                if season == 'warm':
                    daily_temp = (temp_9am + temp_3pm) / 2
                    daily_rainfall = rainfall
                    daily_wind = (wind_speed_9am + wind_speed_3pm) / 2
                    daily_humidity = (humidity_9am + humidity_3pm) / 2
                    daily_pressure = (pressure_9am + pressure_3pm) / 2
                    
                    # Update total metrics
                    total_days_w += 1
                    total_temp_w += daily_temp
                    total_rainfall_w += daily_rainfall
                    total_wind_w += daily_wind
                    total_humidity_w += daily_humidity
                    total_pressure_w += daily_pressure
                    
                    # Update minimum and maximum temperatures
                    if daily_temp > total_max_temp_w:
                        total_max_temp_w = daily_temp
                    if daily_temp < total_min_temp_w:
                        total_min_temp_w = daily_temp
                    
                    # Check for hot days
                    if daily_temp >= 85:
                        hot_days_w += 1
                    
                    # Check for rainy days
                    if daily_rainfall > 0:
                        rainy_days_w += 1
                    
                    # Check for sunny days
                    if cloud_9am in ['Fair', 'Partly Cloudy'] or cloud_3pm in ['Fair', 'Partly Cloudy']:
                        sunny_days_w += 1
            
                    
                elif season == 'cold':
                    daily_temp = (temp_9am + temp_3pm) / 2
                    daily_rainfall = rainfall
                    daily_wind = (wind_speed_9am + wind_speed_3pm) / 2
                    daily_humidity = (humidity_9am + humidity_3pm) / 2
                    daily_pressure = (pressure_9am + pressure_3pm) / 2
                    
                    # Update total metrics
                    total_days_c += 1
                    total_temp_c += daily_temp
                    total_rainfall_c += daily_rainfall
                    total_wind_c += daily_wind
                    total_humidity_c += daily_humidity
                    total_pressure_c += daily_pressure
                    
                    # Update minimum and maximum temperatures
                    if daily_temp > total_max_temp_c:
                        total_max_temp_c = daily_temp
                    if daily_temp < total_min_temp_c:
                        total_min_temp_c = daily_temp
                    
                    # Check for hot days
                    if daily_temp >= 85:
                        hot_days_c += 1
                    
                    # Check for rainy days
                    if daily_rainfall > 0:
                        rainy_days_c += 1
                    
                    # Check for sunny days
                    if cloud_9am in ['Fair', 'Partly Cloudy'] or cloud_3pm in ['Fair', 'Partly Cloudy']:
                        sunny_days_c += 1
            
            
            
            
            
            
            
            
                if season == "warm":
                    # Calculate average metrics for the current year warm
                    avg_temp_w = total_temp_w / total_days_w
                    avg_rainfall_w = total_rainfall_w / total_days_w
                    avg_wind_w = total_wind_w / total_days_w
                    avg_humidity_w = total_humidity_w / total_days_w
                    avg_pressure_w = total_pressure_w / total_days_w
                    p_hot_w = hot_days_w / total_days_w
                    p_rain_w = rainy_days_w / total_days_w
                    p_sunshine_w = sunny_days_w / total_days_w
                    
                    # Create dictionary containing weather metrics for the current year warm
                    weather_metrics_w = { 'a_temp': avg_temp_w,
                        'a_min_temp': total_min_temp_w,
                        'a_max_temp': total_max_temp_w,
                        'a_rainfall': avg_rainfall_w,
                        'a_wind': avg_wind_w,
                        'a_humidity': avg_humidity_w,
                        'a_pressure': avg_pressure_w,
                        'p_hot': p_hot_w,
                        'p_rain': p_rain_w,
                        'p_sunshine': p_sunshine_w
                    }
                
                    weather_data_warm.append(weather_metrics_w)
            
                elif season == 'cold':
                    # Calculate average metrics for the current year cold
                    avg_temp_c = total_temp_c / total_days_c
                    avg_rainfall_c = total_rainfall_c / total_days_c
                    avg_wind_c = total_wind_c / total_days_c
                    avg_humidity_c = total_humidity_c / total_days_c
                    avg_pressure_c = total_pressure_c / total_days_c
                    p_hot_c = hot_days_c / total_days_c
                    p_rain_c = rainy_days_c / total_days_c
                    p_sunshine_c = sunny_days_w / total_days_c
                    
                    # Create dictionary containing weather metrics for the current year cold
                    weather_metrics_c = { 'a_temp_c': avg_temp_c,
                        'a_min_temp_c': total_min_temp_c,
                        'a_max_temp_c': total_max_temp_c,
                        'a_rainfall_c': avg_rainfall_c,
                        'a_wind_c': avg_wind_c,
                        'a_humidity_c': avg_humidity_c,
                        'a_pressure_c': avg_pressure_c,
                        'p_hot_c': p_hot_c,
                        'p_rain_c': p_rain_c,
                        'p_sunshine_c': p_sunshine_c
                    }
                    
                    weather_data_cold.append(weather_metrics_c)
            
            
            
    # return the weather data for both warm and cold seasons
    return weather_data_warm, weather_data_cold
    
    
"""
does the same thing as process_wind but considers 
the cold and warm month data. should return the average wind speeds for both
cold and warm months from the corresponding year.
"""
def process_wind_2(weather_data_warm, weather_data_cold):
    avg_wind_per_year_w = []
    avg_wind_per_year_c = []
    for year_data in weather_data_warm:
        avg_wind_per_year_w.append(year_data['a_wind'])
    for year_data in weather_data_cold:
        avg_wind_per_year_c.append(year_data['a_wind_c'])
        
    avg_wind_per_year_w = sum(avg_wind_per_year_w) / len(avg_wind_per_year_w)
    avg_wind_per_year_c = sum(avg_wind_per_year_c) / len(avg_wind_per_year_c)
    
    return avg_wind_per_year_w, avg_wind_per_year_c
"""
function the same as process_sun but considers minimum and maximum for both cold and warm
months.
"""
def process_sun_2(weather_data_warm, weather_data_cold):
    sunshine_ratios_w = [year_data['p_sunshine'] for year_data in weather_data_warm]
    sunshine_ratios_c = [year_data['p_sunshine_c'] for year_data in weather_data_cold]
    min_sunshine_ratios_w = min(sunshine_ratios_w)
    max_sunshine_ratios_w = max(sunshine_ratios_w)
    min_sunshine_ratios_c = min(sunshine_ratios_c)
    max_sunshine_ratios_c = max(sunshine_ratios_c)
    
    return min_sunshine_ratios_w, max_sunshine_ratios_w, min_sunshine_ratios_c, max_sunshine_ratios_c
    
"""
performances the same function as process_temperature but considers the cold
and warm months from the year.
"""   
def process_temperature_2(weather_data_warm, weather_data_cold):
    avg_temperatures_w = [year_data['a_temp'] for year_data in weather_data_warm]
    min_temperatures_w = [year_data['a_min_temp'] for year_data in weather_data_warm]
    max_temperatures_w = [year_data['a_max_temp'] for year_data in weather_data_warm]
    hot_day_ratios_w = [year_data['p_hot'] for year_data in weather_data_warm]
    avg_temperatures_c = [year_data['a_temp_c'] for year_data in weather_data_cold]
    min_temperatures_c = [year_data['a_min_temp_c'] for year_data in weather_data_cold]
    max_temperatures_c = [year_data['a_max_temp_c'] for year_data in weather_data_cold]
    hot_day_ratios_c = [year_data['p_hot_c'] for year_data in weather_data_cold]
    
    avg_temperatures_w = sum(avg_temperatures_w)/ len(avg_temperatures_w)
    min_temperatures_w = sum(min_temperatures_w) / len(min_temperatures_w)
    max_temperatures_w = sum(max_temperatures_w) / len(max_temperatures_w)
    hot_day_ratios_w = sum(hot_day_ratios_w) / len(hot_day_ratios_w)
    
    avg_temperatures_c = sum(avg_temperatures_c)/ len(avg_temperatures_c)
    min_temperatures_c = sum(min_temperatures_c) / len(min_temperatures_c)
    max_temperatures_c = sum(max_temperatures_c) / len(max_temperatures_c)
    hot_day_ratios_c = sum(hot_day_ratios_c) / len(hot_day_ratios_c)
    
    return avg_temperatures_w, min_temperatures_w, max_temperatures_w, hot_day_ratios_w, avg_temperatures_c, min_temperatures_c, max_temperatures_c, hot_day_ratios_c

"""
main function will go through all the existing yearly .csv files and output the weather
data for the whole year, and the year when divided into cold/warm months
"""
# Main function
def main():
    directory = r'C:\Users\bangk\OneDrive\Documents\OOP hw'  # my directory with .csv files
    for year in range(2006, 2022):
         if year in [2007, 2008, 2009, 2016, 2017, 2020]:
             pass
         else:
             file_names = [f"{directory}/htx_{year}_weather.csv"]
             #acquire weather data
             weather_data = read_file(file_names)
             weather_data_warm, weather_data_cold = read_file_2(file_names)
             #function processing weather information
             avg_wind_per_year = process_wind(weather_data)
             min_sunshine_ratio, max_sunshine_ratio = process_sun(weather_data)
             avg_temperatures, min_temperatures, max_temperatures, hot_day_ratios = process_temperature(weather_data)
             # functions considering warm and cold seasons
             avg_wind_per_year_w, avg_wind_per_year_c = process_wind_2(weather_data_warm, weather_data_cold)
             min_sunshine_ratios_w, max_sunshine_ratios_w, min_sunshine_ratios_c, max_sunshine_ratios_c = process_sun_2(weather_data_warm, weather_data_cold)
             avg_temperatures_w, min_temperatures_w, max_temperatures_w, hot_day_ratios_w, avg_temperatures_c, min_temperatures_c, max_temperatures_c, hot_day_ratios_c = process_temperature_2(weather_data_warm, weather_data_cold)

             print("\n")
             print(year)
             print("Average Wind Speed Per Year:", avg_wind_per_year)
             print("Minimum Sunshine Ratio:", min_sunshine_ratio)
             print("Maximum Sunshine Ratio:", max_sunshine_ratio) 
             print("Average Temperatures Per Year:", avg_temperatures)   
             print("Minimum Temperatures Per Year:", min_temperatures)     
             print("Maximum Temperatures Per Year:", max_temperatures)
             print("Hot Day Ratios Per Year:", hot_day_ratios)
             print("\nSeasons")
             
             print("Average Wind Speed Per Year warm:", avg_wind_per_year_w, "cold: ", avg_wind_per_year_c)
             print("Minimum Sunshine Ratio warm:", min_sunshine_ratios_w, "cold: ", min_sunshine_ratios_c)
             print("Maximum Sunshine Ratio warm:", max_sunshine_ratios_w, "cold: ", max_sunshine_ratios_c)
             print("Average Temperatures Per Year warm:", avg_temperatures_w, "cold: ", avg_temperatures_c)
             print("Minimum Temperatures Per Year warm:", min_temperatures_w, "cold: ", min_temperatures_c)
             print("Maximum Temperatures Per Year warm:", max_temperatures_w, "cold: ", max_temperatures_c)
             print("Hot Day Ratios Per Year warm:", hot_day_ratios_w, "cold: ", hot_day_ratios_c)
if __name__ == "__main__":
    main()