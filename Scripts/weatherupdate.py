import requests
from datetime import datetime, timedelta
from llama_cpp import Llama  # Import the Llama 2 model wrapper
from keys import openweathermap_api_key, ipinfo_api_token
from dynamics import llama_7b

# Initialize the Llama 2 model

model_used = llama_7b
llama_model = Llama(
    model_path=model_used,  # Load the model
    verbose=False
)

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
    Retrieves the weather information for a given city and generates a recommendation using the LLM model.

    Args:
        api_key (str): The API key for accessing the OpenWeatherMap API.
        city (str): The name of the city for which to retrieve the weather information.
        forecast (bool): Whether to fetch forecast data. Default is False (current weather).
        days (int): Number of days ahead for the forecast. Default is 1 (tomorrow).

    Returns:
        str: A formatted string containing the weather description, temperature, and a recommendation.
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
                forecast_list = data["list"]
                target_date = datetime.now() + timedelta(days=days)
                target_date_str = target_date.strftime('%Y-%m-%d')
                for entry in forecast_list:
                    if entry["dt_txt"].startswith(target_date_str):
                        weather_description = entry["weather"][0]["description"]
                        temperature = entry["main"]["temp"]
                        # Generate a recommendation using the Llama 2 model
                        recommendation = generate_llm_recommendation(city, temperature, target_date_str, weather_description)
                        weather_info = (f"Weather forecast for {city} on {target_date_str}:\n"
                                        f"Temperature: {temperature}°C\n"
                                        f"Condition: {weather_description.capitalize()}\n"
                                        f"Recommendation: {recommendation}")
                        return weather_info
                return f"No forecast data available for {city} on {target_date_str}."
            else:
                # Current weather data
                weather_description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                current_date = datetime.now().strftime('%Y-%m-%d')
                # Generate a recommendation using the Llama 2 model
                recommendation = generate_llm_recommendation(city, temperature, current_date, weather_description)

                weather_info = (f"Current weather in {city}:\n"
                                f"Temperature: {temperature}°C\n"
                                f"Condition: {weather_description.capitalize()}\n"
                                f"Recommendation: {recommendation}")
                return weather_info
        else:
            return f"Error fetching weather: {data['message']}"
    except Exception as e:
        return f"An error occurred: {e}"

def generate_llm_recommendation(city, temperature, date, weather_description):
    """
    Generates a weather recommendation using the Llama 2 model based on city, temperature, date, and weather condition.

    Args:
        city (str): The city for which the recommendation is generated.
        temperature (float): The temperature in Celsius.
        date (str): The date for which the recommendation is needed.
        weather_description (str): The weather condition description.

    Returns:
        str: The recommendation generated by the Llama 2 model.
    """
    # Craft a prompt to send to the Llama 2 model
    prompt = (f"Weather information:\n"
              f"City: {city}\n"
              f"Date: {date}\n"
              f"Temperature: {temperature}°C\n"
              f"Condition: {weather_description.capitalize()}.\n"
              "Based on this information, provide a short recommendation.")

    # Send the prompt to the Llama 2 model
    response = llama_model(prompt, max_tokens=50)

    # Handle response properly, ensuring output text is retrieved
    generated_text = response['choices'][0]['text'].strip()

    # Ensure no duplication of "Recommendation" label
    if generated_text.lower().startswith("recommendation:"):
        generated_text = generated_text[len("Recommendation:"):].strip()

    # Return the generated recommendation
    return generated_text if generated_text else "No recommendation generated."


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

if __name__ == '__main__':
    # Example queries
    queries = [
        "what will be the weather updates of here tomorrow"
    ]

    for query in queries:
        if "weather" in query:
            forecast, days, city = parse_query(query)
            if city == "current":
                city = get_city_from_ipinfo(ipinfo_api_token)
            if city:
                weather_info = get_weather(openweathermap_api_key, city, forecast, days)
                print(weather_info)
            else:
                print("Could not detect city based on IP address or provided query.")
