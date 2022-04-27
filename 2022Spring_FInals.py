import sys
import random

class airplane_attributes:

    def __init__(self, weather_decider, wind_decider, weight_decider, ground_traffic_decider):
        """
        weather: In aviation, weather at airports is categorised based on the Runway Visibility Range (RVR), or in
                 simple terms, the distance of runway from the runway threshold - which is visible with the naked eye.
                 This is because, reduction in visibility is directly proportional to the deterioration in weather.
                 Hence, the main 3 categories we will include is:
                 cat_1: This is Category 1 where RVR is not less than 800 m
                 cat_2: This is Category 2 where RVR is not less than 300 m
                 cat_3: This is Category 3 where RVR is from 200 m to 0 m

        https://www.southernwings.co.nz/the-effects-of-wind-on-aircraft/
        wind: There are mainly four types of wind in aviation:
                 headwind: A headwind is wind blowing directly towards the front of the aircraft. A headwind increases
                           drag.
                 tailwind: A tailwind is wind blowing directly towards the rear of the aircraft. A tailwind assists the
                           aircraft’s propulsion systems.
                 crosswind: Winds blowing in any other direction than a headwind or tailwind.
                 wind_shear: A sudden change in headwind or tailwind causing rapid changes in lift to the aircraft also
                             known as ‘Wind Shear’ is one of the worst wind effects to experience.

        aircraft_weight_class: This is a significant randomized variable to consider due to the concept of
                               Wake Turbulence. Wake turbulence is a disturbance in the atmosphere that forms behind an
                               aircraft as it passes through the air. Heavier the aircraft, more is the wake turbulence.
                               The different weight classes are based on Maximum Take-Off Mass (MTOM):
                               light: MTOM < 7,000 kgs
                               medium: 7,000 kgs < MTOM < 136,000 kgs
                               heavy: MTOM >136,000 kgs
                               super: Specific category for Airbus A380-800 and Antonov An-225

        ground_traffic: This represents the aircraft traffic on taxiways. These planes would also be in a queue to get
                        ready for takeoff. Higher the ground traffic, higher would be the air traffic congestion.
                        The types of ground traffic assumed are low, average and high.

        air_traffic_congestion: This variable would be dependent on ground_traffic. Our assumption is that if
                                ground_traffic is high, air_traffic_congestion is also max. If ground_traffic is
                                average or low, air_traffic_congestion is regular


        """
        # weather either changes or remains same for every 100 planes
        self.weather = weather_decider.get_weather()

        # wind either changes or remains same for every 10 planes. Determined by weighted probability for each wind type
        # highest probability is given to headwind and tailwind
        self.wind = wind_decider.get_wind()

        # determined by weighted probability for each weight class. Highest probability is given for medium aircraft
        self.aircraft_weight_class = weight_decider.get_weight()

        # ground_traffic either changes or remains same for every 20 planes
        self.ground_traffic = ground_traffic_decider.get_ground_traffic()

        # air_traffic_congestion is directly dependent on ground_traffic
        if self.ground_traffic == 'high':
            self.air_traffic_congestion = 'max'
        if self.ground_traffic == 'average' or self.ground_traffic == 'low':
            self.air_traffic_congestion = 'regular'

class weather_decider:

    def __init__(self):
        self.temp_weather = random.choice(['cat_1', 'cat_2', 'cat_3'])
        self.weather_counter = 0

    def get_weather(self):
        if self.weather_counter % 100 == 0:
            self.temp_weather = random.choice(['cat_1', 'cat_2', 'cat_3'])

        self.weather_counter += 1
        return self.temp_weather

class wind_decider:

    def __init__(self):
        # https://pynative.com/python-weighted-random-choices-with-probability/
        self.temp_wind = random.choices(['headwind', 'tailwind', 'crosswind', 'wind_shear'], weights=(45, 45, 5, 5), k=1)
        self.wind_counter = 0

    def get_wind(self):
        if self.wind_counter % 10 == 0:
            self.temp_wind = random.choices(['headwind', 'tailwind', 'crosswind', 'wind_shear'], weights=(45, 45, 5, 5), k=1)

        self.wind_counter += 1
        return self.temp_wind[0]

class weight_decider:

    def __init__(self):
        self.temp_weight = []

    def get_weight(self):
        # https://pynative.com/python-weighted-random-choices-with-probability/
        self.temp_weight = random.choices(['light', 'medium', 'heavy', 'super'], weights=(5, 60, 30, 5), k=1)

        return self.temp_weight[0]

class ground_traffic_decider:

    def __init__(self):
        self.temp_ground_traffic = random.choice(['low', 'average', 'high'])
        self.ground_traffic_counter = 0

    def get_ground_traffic(self):
        if self.ground_traffic_counter % 20 == 0:
            self.temp_ground_traffic = random.choice(['low', 'average', 'high'])

        self.ground_traffic_counter += 1
        return self.temp_ground_traffic

def calculate_dist_affected_due_weather(weather_1, weather_2, separation):
    if weather_1 == weather_2:
        return separation
    elif weather_1 == 'cat_1':
        if weather_2 == 'cat_2':
            return separation + 0.5
        else:
            return separation + 1.5
    elif weather_1 == 'cat_2':
        if weather_2 == 'cat_1':
            return separation - 0.5
        else:
            return separation + 1
    else:
        if weather_2 == 'cat_1':
            return separation - 1.5
        else:
            return separation - 1

def calculate_dist_affected_due_wind(wind_1, wind_2, separation):
    if wind_1 == wind_2:
        return separation
    elif wind_1 == 'headwind':
        if wind_2 == 'tailwind':
            return separation - 0.2
        elif wind_2 == 'crosswind':
            return separation - 0.4
        else:
            return separation - 0.6
    elif wind_1 == 'tailwind':
        if wind_2 == 'headwind':
            return separation + 0.2
        elif wind_2 == 'crosswind':
            return separation - 0.2
        else:
            return separation - 0.4
    elif wind_1 == 'crosswind':
        if wind_2 == 'headwind':
            return separation + 0.4
        elif wind_2 == 'tailwind':
            return separation + 0.2
        else:
            return separation - 0.2
    else:
        if wind_2 == 'headwind':
            return separation + 0.6
        elif wind_2 == 'tailwind':
            return separation + 0.4
        else:
            return separation + 0.2

def calculate_dist_affected_due_aircraft_weight_class(aircraft_weight_class_1, aircraft_weight_class_2, separation):
    if aircraft_weight_class_1 == aircraft_weight_class_2:
        return separation
    elif aircraft_weight_class_1 == 'light':
        if aircraft_weight_class_2 == 'medium':
            return separation - 1.8
        elif aircraft_weight_class_2 == 'heavy':
            return separation - 1.9
        else:
            return separation - 2
    elif aircraft_weight_class_1 == 'medium':
        if aircraft_weight_class_2 == 'light':
            return separation + 0.4
        elif aircraft_weight_class_2 == 'heavy':
            return separation - 1.8
        else:
            return separation - 2
    elif aircraft_weight_class_1 == 'heavy':
        if aircraft_weight_class_2 == 'light':
            return separation + 1.5
        elif aircraft_weight_class_2 == 'medium':
            return separation + 0.4
        else:
            return separation - 1.8
    else:
        if aircraft_weight_class_2 == 'light':
            return separation + 3
        elif aircraft_weight_class_2 == 'medium':
            return separation + 2
        else:
            return separation + 1.5

def calculate_dist_affected_due_ground_traffic(ground_traffic_1, ground_traffic_2, separation):
    if ground_traffic_1 == ground_traffic_2:
        return separation
    elif ground_traffic_1 == 'low':
        if ground_traffic_2 == 'average':
            return separation + 0.2
        else:
            return separation + 0.4
    elif ground_traffic_1 == 'average':
        if ground_traffic_2 == 'low':
            return separation - 0.2
        else:
            return separation + 0.2
    else:
        if ground_traffic_2 == 'low':
            return separation - 0.4
        else:
            return separation - 0.2

def calculate_dist_affected_due_air_traffic_congestion(air_traffic_congestion_1, air_traffic_congestion_2, separation):
    if air_traffic_congestion_1 == air_traffic_congestion_2:
        return separation
    elif air_traffic_congestion_1 == 'regular':
        return separation + 0.3
    else:
        return separation - 0.3


if __name__ == '__main__':
    airplane_objects_dict = {}
    weather_decider = weather_decider()
    wind_decider = wind_decider()
    weight_decider = weight_decider()
    ground_traffic_decider = ground_traffic_decider()
    distance_list = []

    # 5 NM is the recommended separation minima according to ICAO
    separation_minima = 5

    # https://stackoverflow.com/questions/21598872/how-to-create-multiple-class-objects-with-a-loop-in-python
    for i in range(1, 10001):
        name = 'airplane_{}'.format(i)
        airplane_objects_dict[name] = airplane_attributes(weather_decider, wind_decider, weight_decider, ground_traffic_decider)
        if i > 1:
            airplane_name_1 = 'airplane_{}'.format(i - 1)
            airplane_name_2 = 'airplane_{}'.format(i)
            a = airplane_objects_dict[airplane_name_1].__dict__
            b = airplane_objects_dict[airplane_name_2].__dict__
            distance_affected_due_weather = calculate_dist_affected_due_weather(a['weather'], b['weather'], separation_minima)
            distance_affected_due_wind = calculate_dist_affected_due_wind(a['wind'], b['wind'], distance_affected_due_weather)
            distance_affected_due_aircraft_weight_class = calculate_dist_affected_due_aircraft_weight_class\
                (a['aircraft_weight_class'], b['aircraft_weight_class'], distance_affected_due_wind)
            distance_affected_due_ground_traffic = calculate_dist_affected_due_ground_traffic\
                (a['ground_traffic'], b['ground_traffic'], distance_affected_due_aircraft_weight_class)
            distance_affected_due_air_traffic_congestion = calculate_dist_affected_due_air_traffic_congestion\
                (a['air_traffic_congestion'], b['air_traffic_congestion'], distance_affected_due_ground_traffic)
            temp_optimized_separation_minima = distance_affected_due_air_traffic_congestion

            distance_list.append(temp_optimized_separation_minima)

    optimized_separation_minima = sum(distance_list)/len(distance_list)
    print(round(optimized_separation_minima, 3))