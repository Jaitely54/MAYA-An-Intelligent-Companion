import requests
from datetime import datetime, timedelta
from keys import openweathermap_api_key, ipinfo_api_token

def get_city_from_ipinfo(api_token):
    try:
        response = requests.get(f'https://ipinfo.io?token={api_token}')
        data = response.json()
        return data['city']
    except Exception as e:
        print(f"Error obtaining city from IP: {e}")
        return None

def get_weather(api_key, city, forecast=False, days=1):
    """
    Retrieves the weather information for a given city.

    Args:
        api_key (str): The API key for accessing the OpenWeatherMap API.
        city (str): The name of the city for which to retrieve the weather information.
        forecast (bool): Whether to fetch forecast data. Default is False (current weather).
        days (int): Number of days ahead for the forecast. Default is 1 (tomorrow).

    Returns:
        str: A formatted string containing the weather description, temperature, and humidity for the given city.
        str: An error message if the API request is unsuccessful.
    """
    base_url = "http://api.openweathermap.org/data/2.5/"
    endpoint = "forecast" if forecast else "weather"
    url = base_url + endpoint
    
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code == 200:
            if forecast:
                # Fetch forecast data for the specified day
                # Note: OpenWeatherMap returns data in 3-hour intervals
                forecast_list = data["list"]
                target_date = datetime.now() + timedelta(days=days)
                target_date_str = target_date.strftime('%Y-%m-%d')
                for entry in forecast_list:
                    if entry["dt_txt"].startswith(target_date_str):
                        weather_description = entry["weather"][0]["description"]
                        temperature = entry["main"]["temp"]
                        humidity = entry["main"]["humidity"]
                        weather_info = (f"Weather forecast for {city} on {target_date_str}: {weather_description}\n"
                                        f"Temperature: {temperature}°C\n"
                                        f"Humidity: {humidity}%")
                        return weather_info
                return f"No forecast data available for {city} on {target_date_str}."
            else:
                # Current weather data
                weather_description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                humidity = data["main"]["humidity"]

                weather_info = (f"Current weather in {city}: {weather_description}\n"
                                f"Temperature: {temperature}°C\n"
                                f"Humidity: {humidity}%")
                return weather_info
        else:
            return f"Error fetching weather: {data['message']}"
    except Exception as e:
        return f"An error occurred: {e}"

def parse_query(query):
    """
    Parses the query to determine if a weather forecast is requested, for how many days, and which city.

    Args:
        query (str): The user query.

    Returns:
        bool: Whether a forecast is requested.
        int: Number of days for the forecast.
        str: City name or 'current' for the current city.
    """
    query = query.lower()
    forecast = False
    days = 0
    city = None

    if "my current city" in query or "here" in query:
        city = "current"
    else:   
        # Extract city name if mentioned
        city_keywords = ["in", "of", "at"]
        for keyword in city_keywords:
            if keyword in query:
                city_part = query.split(keyword)[-1].strip()
                city = city_part.split(" ")[0]  # Assuming the city is the first part after the keyword
                break

    if "tomorrow" in query:
        forecast = True
        days = 1
    elif "in" in query and "days" in query:
        parts = query.split()
        try:
            days = int(parts[parts.index("in") + 1])
            forecast = True
        except (IndexError, ValueError):
            days = 0

    return forecast, days, city

if __name__ =='__main__':
    # Example queries
    queries = [
        "what will be the weather updates of meerut tomorrow",
        "what will be the weather updates of here",
    ]

    for query in queries:
        if "hi" in query or "hello" in query:
            print("hi")
        elif "weather" in query:
            forecast, days, city = parse_query(query)
            if city == "current":
                city = get_city_from_ipinfo(ipinfo_api_token)
            if city:
                weather_info = get_weather(openweathermap_api_key, city, forecast, days)
                print(weather_info)
            else:
                print("Could not detect city based on IP address or provided query.")
