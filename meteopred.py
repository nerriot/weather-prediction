from datetime import datetime

import numpy as np
from meteostat import Point, Daily


class PredictWeather:
    def __init__(self, place: Point) -> None:
        """
        Initializes an instance of PredictWeather class.

        Args:
            place (Point): The geographical coordinates of the place.
        """

        self.place = place
        assert isinstance(place, Point), "place should be an instance of Point"

        self.data = self._create_array()

    def _create_array(self) -> np.array:
        """
        Creates a numpy array containing weather data.
        Returns:
            np.array: A numpy array containing weather data.
        """

        start_date = datetime(1950, 1, 1)
        end_date = datetime(2022, 12, 31)

        # Since weather stations can fail, there are gaps in the data that are filled in by the "interpolate()" method.
        # The data is obtained by the "_date" attribute, because the "fetch()" and "interpolate()" methods do not combine well
        data = Daily(self.place, start=start_date, end=end_date).interpolate(100)._data.values[:, :4]

        # Also, for ease of use, data for every February 29 is deleted
        data = np.delete(data, np.arange(669, len(data), 1461), axis=0)

        return data.reshape((-1, 365, 4))

    def _get_predict_axis(self, date: datetime, axis: int) -> list:
        """
            Retrieves the average and standard deviation of a specific weather parameter for a given date.

            Args:
                date (datetime): The date for which weather data is requested.
                axis (int): The axis corresponding to the weather parameter.

            Returns:
                list: A list containing the average and standard deviation of the weather parameter.
        """

        # Since only data is used to predict the weather for any date, the year does not affect the prediction.
        # This is done so that there will be no confusion from February 29
        assert date.month != 2 or date.day != 29, "at the moment it is not possible to predict the weather for February 29"
        date = datetime(2023, date.month, date.day)

        weather_in_previous_years = self.data[:, date.timetuple().tm_yday - 1, axis]
        average = np.mean(weather_in_previous_years)
        std = np.std(weather_in_previous_years)

        return [average, std]

    def get_predict_temp(self, date: datetime) -> dict:
        """
            Predicts temperature for a given date and returns the average and standard deviation.

            Args:
                date (datetime): The date for which temperature prediction is requested.

            Returns:
                dict: A dictionary containing the average and standard deviation of the predicted temperature.
        """

        min_average_temperature, min_temp_std = self._get_predict_axis(date, 1)
        avg_average_temperature, avg_temp_std = self._get_predict_axis(date, 0)
        max_average_temperature, max_temp_std = self._get_predict_axis(date, 2)

        return {
            'min': min_average_temperature,
            'min_std': min_temp_std,
            'avg': avg_average_temperature,
            'avg_std': avg_temp_std,
            'max': max_average_temperature,
            'max_std': max_temp_std
        }

    def get_predict_rain(self, date: datetime) -> dict:
        """
            Predicts rainfall for a given date and returns the average and standard deviation.

            Args:
                date (datetime): The date for which rainfall prediction is requested.

            Returns:
                dict: A dictionary containing the average and standard deviation of the predicted rainfall.
        """

        average_mm, std_mm = self._get_predict_axis(date, 3)

        return {
            'avg': average_mm,
            'avg_std': std_mm
        }


if __name__ == '__main__':
    nsk = Point(55.00835, 82.93573, 164)

    pred = PredictWeather(nsk)
    print(pred.get_predict_temp(datetime(2023, 6, 18)))
    print(pred.get_predict_rain(datetime(2023, 6, 18)))
