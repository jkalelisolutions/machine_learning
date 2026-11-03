# A Tea Estate field Supervisor Assistant

The assistant is used to fetch data from a weather API and answer questions like "Is today a good day for harvesting?". The assistant then answers based on the data pulled from the Weather API.

## To Setup

1. pip install anthropic python-dotenv requaest.
2. Create a new file .env with: ANTHROPIC_API=your_api_here, WEATHER_API=your_api_here
3. Get your api key from https://platform.claude.com and https://open-meteo.com
4. Change city name in get_weather(): url

### To Run

python day14_exercise.py
