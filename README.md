# Weather Prediction
This is a Python program that predicts weather data (temperature and rainfall) for a given date using historical weather data. The program uses the Meteostat library to fetch and interpolate weather data from weather stations.

## Installation

1. Clone the repository to your local machine:
```console
git clone https://github.com/your-username/weather-prediction.git
```

2. Install the required dependencies. You can use pip to install them:
```console
pip install -r requirements.txt
```

3. Run the meteopred.py script to start predicting weather data:
```console
python meteopred.py
```

## Usage

The `meteopred.py` script provides a `PredictWeather` class that can be used to predict temperature and rainfall for a specific date.

```python
from datetime import datetime
from meteostat import Point
from meteopred import PredictWeather

# Specify the geographical coordinates of the place
place = Point(lat=55.00835, lon=82.93573, alt=164)

# Create an instance of the PredictWeather class
predictor = PredictWeather(place)

# Predict temperature for a specific date
date = datetime(2023, 6, 20)
temperature_prediction = predictor.get_predict_temp(date)
print(temperature_prediction)

# Predict rainfall for a specific date
rainfall_prediction = predictor.get_predict_rain(date)
print(rainfall_prediction)
```

## Contributing
Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
This project utilizes the Meteostat library for fetching historical weather data.
