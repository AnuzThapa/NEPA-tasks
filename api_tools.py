from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a given city using OpenWeatherMap API.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A string describing the current weather conditions
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return "Error: OPENWEATHER_API_KEY is not set in the environment variables."

        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            weather_desc = data["weather"][0]["description"].capitalize()
            temp_c = data["main"]["temp"]
            temp_f = temp_c * 9/5 + 32
            return f"The weather in {city} is currently {weather_desc} with a temperature of {temp_c:.1f}°C ({temp_f:.1f}°F)."
        else:
            return f"Error fetching weather: API returned status code {response.status_code}"

    except Exception as e:
        return f"Error fetching weather for {city}: {str(e)}"



@tool
def get_crypto_price(crypto_symbol: str) -> str:
    """
    Get the current price of a cryptocurrency using CoinMarketCap.
    """
    try:
        api_key = os.getenv("CMC_API_KEY")
        if not api_key:
            return "Error: CoinMarketCap API key not set in environment variables."


        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        params = {"symbol": crypto_symbol.upper(), "convert": "USD"}
        headers = {"X-CMC_PRO_API_KEY": api_key}

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if "data" in data and crypto_symbol.upper() in data["data"]:
                quote = data["data"][crypto_symbol.upper()]["quote"]["USD"]
                price = quote["price"]
                change_24h = quote.get("percent_change_24h", 0)
                change_sign = "+" if change_24h >= 0 else ""
                return f"The current price of {crypto_symbol.upper()} is ${price:,.2f} USD (24h change: {change_sign}{change_24h:.2f}%)"
            else:
                return f"Could not find price information for {crypto_symbol}. Check the symbol."
        else:
            return f"Error fetching crypto price: API returned status code {response.status_code}"

    except Exception as e:
        return f"Error fetching crypto price for {crypto_symbol}: {str(e)}"


