import sys
import random
import pandas as pd

class airplane_attributes:

    def __init__(self, weather_decider, wind_decider, weight_decider, ground_traffic_decider, hypotheis_type):
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
        if hypotheis_type == "hyp_1":
            # weather either changes or remains same for every 100 planes
            self.weather = weather_decider.get_weather()
        else:
            self.weather = "cat_3"
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
        """
            Method to randomize weather category for the MC simulation after every 100 flights
        """
        if self.weather_counter % 100 == 0:
            self.temp_weather = random.choice(['cat_1', 'cat_2', 'cat_3'])

        self.weather_counter += 1
        return self.temp_weather

class wind_decider:

    def __init__(self):
        # https://pynative.com/python-weighted-random-choices-with-probability/
        self.temp_wind = random.choices(['headwind', 'tailwind', 'crosswind', 'wind_shear'], weights=(80, 10, 5, 5), k=1)
        self.wind_counter = 0

    def get_wind(self):
        """
            Method to randomize wind category for the MC simulation after every 10 flights. The randomized choices have
            been assigned weights.
        """
        if self.wind_counter % 10 == 0:
            self.temp_wind = random.choices(['headwind', 'tailwind', 'crosswind', 'wind_shear'], weights=(80, 10, 5, 5), k=1)

        self.wind_counter += 1
        return self.temp_wind[0]

class weight_decider:

    def __init__(self):
        self.temp_weight = []

    def get_weight(self):
        """
            Method to randomize weight category values for the MC simulation. The randomized choices have
            been assigned weights.
        """
        # https://pynative.com/python-weighted-random-choices-with-probability/
        self.temp_weight = random.choices(['light', 'medium', 'heavy', 'super'], weights=(5, 60, 30, 5), k=1)

        return self.temp_weight[0]

class ground_traffic_decider:

    def __init__(self):
        self.temp_ground_traffic = random.choice(['low', 'average', 'high'])
        self.ground_traffic_counter = 0

    def get_ground_traffic(self):
        """
        Method to randomize ground traffic type values for the MC simulation after every 20 flights.
        """
        if self.ground_traffic_counter % 20 == 0:
            self.temp_ground_traffic = random.choice(['low', 'average', 'high'])

        self.ground_traffic_counter += 1
        return self.temp_ground_traffic

def calculate_dist_affected_due_weather(weather_1: str, weather_2: str, separation: float) -> float:
    """
        Calculates change in separation minima (in NM) for current and next flight in queue depending
        on weather type:
            1. same category - no change
            2. category 1 to category 2: +0.5
            3. category 1 to category 3: +1.5
            4. category 2 to category 1: -0.5
            5. category 2 to category 3: +1
            6. category 3 to category 1: -1.5
            7. category 3 to category 2: -1
        :param weather_1: weather type during current flight in queue
        :param weather_2: weather type during next flight in queue
        :param separation: default separation minima defined (5 NM)
        :return: change in separation minima in NM
        >>> calculate_dist_affected_due_weather('cat_1', 'cat_2', 5)
        5.5
    """
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

def calculate_dist_hyp_2(weather_1: str, weather_2: str, separation: float) -> float:
    """
        Calculates change in separation minima (in NM) for current and next flight in queue for hypothesis 2
        where weather is of category 3 (worst) for all flights
        :param weather_1: weather type during current flight in queue
        :param weather_2: weather type during next flight in queue
        :param separation: default separation minima defined (5 NM)
        :return: change in separation minima in NM
        >>> calculate_dist_hyp_2('cat_3', 'cat_3', 5)
        6
    """
    if weather_1 == weather_2:
        return separation + 1


def calculate_dist_affected_due_wind(wind_1: str, wind_2: str, separation: float) -> float:
    """
        Calculates change in separation minima (in NM) for current and next flight in queue depending
        on wind type:
            1. same category - no change
            2. headwind to tailwind: -0.2
            3. headwind to crosswind: -0.4
            4. headwind to wind shear: -0.6
            5. tailwind to headwind: +0.2
            6. tailwind to crosswind: -0.2
            7. tailwind to wind shear: -0.4
            8. crosswind to headwind: +0.4
            9. crosswind to tailwind: +0.2
            10. crosswind to wind shear: -0.2
            11. wind shear to headwind: +0.6
            12. wind shear to tailwind: +0.4
            13. wind shear to crosswind: +0.2
        :param wind_1: wind condition during current flight in queue
        :param wind_2: wind condition during next flight in queue
        :param separation: separation distance affected due to weather
        :return: change in separation minima in NM
        >>> calculate_dist_affected_due_wind('headwind', 'crosswind', 5.5)
        5.1
    """
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

def calculate_dist_affected_due_aircraft_weight_class(aircraft_weight_class_1: str, aircraft_weight_class_2: str, separation: float) -> float:
    """
        Calculates change in separation minima (in NM) for current and next flight in queue depending
        on weight class:
            1. same category - no change
            2. light before medium: -1.8
            3. light before heavy: -1.9
            4. light before super: -2
            5. medium before light: +0.4
            6. medium before heavy: -1.8
            7. medium before super: -2
            8. heavy before light: +1.5
            9. heavy before medium: +0.4
            10. heavy before super: -1.8
            11. super before light: +3
            12. super before medium: +2
            13. super before heavy: +1.5
        :param aircraft_weight_class_1: weight class of current flight in queue
        :param aircraft_weight_class_2: weight class of next flight in queue
        :param separation: separation distance affected due to wind
        :return: change in separation minima in NM
        >>> calculate_dist_affected_due_aircraft_weight_class('heavy', 'super', 5.1)
        3.3
    """
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

def calculate_dist_affected_due_ground_traffic(ground_traffic_1: str, ground_traffic_2: str, separation: float) -> float:
    """
        Calculates change in separation minima (in NM) for current and next flight in queue depending
        on ground traffic:
            1. same category - no change
            2. low to average: +0.2
            3. low to high: +0.4
            4. average to low: -0.2
            5. average to high: +0.2
            6. high to low: -0.4
            7. high to average: -0.2
        :param ground_traffic_1: ground traffic during current flight in queue
        :param ground_traffic_2: ground traffic during next flight in queue
        :param separation: separation distance affected due to weight class
        :return: change in separation minima in NM
        >>> calculate_dist_affected_due_ground_traffic('average', 'high', 3.3)
        3.5
    """
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

def calculate_dist_affected_due_air_traffic_congestion(air_traffic_congestion_1: str, air_traffic_congestion_2: str, separation: float) -> float:
    """
        Calculates change in separation minima (in NM) for current and next flight in queue depending
        on air traffic congestion:
            1. same category - no change
            2. regular to max: +0.3
            3. max to regular: -0.3
        :param air_traffic_congestion_1: air traffic congestion during current flight in queue
        :param air_traffic_congestion_2: air traffic congestion during next flight in queue
        :param separation: separation distance affected due to ground traffic
        :return: final change in separation minima in NM
        >>> calculate_dist_affected_due_air_traffic_congestion('max', 'regular', 3.5)
        3.2
    """
    if air_traffic_congestion_1 == air_traffic_congestion_2:
        return separation
    elif air_traffic_congestion_1 == 'regular':
        return separation + 0.3
    else:
        return separation - 0.3


if __name__ == '__main__':
    import doctest
    #import 2022Spring_Finals

    print(doctest.testmod())

    airplane_objects_dict = {}
    weather_decider = weather_decider()
    wind_decider = wind_decider()
    weight_decider = weight_decider()
    ground_traffic_decider = ground_traffic_decider()
    distance_list_hyp1 = []
    distance_list_hyp2 = []

    # 5 NM is the recommended separation minima according to ICAO
    separation_minima = 5

    #creating dataframe to export simulation data
    hyp1_header = ['weather1', 'weather2', 'wind1', 'wind2', 'aircraft_weight_class1', 'aircraft_weight_class2', 'ground_traffic1', 'ground_traffic2', 'air_traffic_congestion1', 'air_traffic_congestion2', 'calculated_minima']
    df1 = pd.DataFrame(columns=hyp1_header)
    df2 = pd.DataFrame(columns=hyp1_header)


    # https://stackoverflow.com/questions/21598872/how-to-create-multiple-class-objects-with-a-loop-in-python
    for i in range(1, 1001):
        name = 'airplane_{}'.format(i)
        airplane_objects_dict[name] = airplane_attributes(weather_decider, wind_decider, weight_decider, ground_traffic_decider, "hyp_1")
        if i > 1:
            airplane_name_1 = 'airplane_{}'.format(i - 1)
            airplane_name_2 = 'airplane_{}'.format(i)
            a1 = airplane_objects_dict[airplane_name_1].__dict__
            b1 = airplane_objects_dict[airplane_name_2].__dict__
            distance_affected_due_weather = calculate_dist_affected_due_weather(a1['weather'], b1['weather'], separation_minima)
            distance_affected_due_wind = calculate_dist_affected_due_wind(a1['wind'], b1['wind'], distance_affected_due_weather)
            distance_affected_due_aircraft_weight_class = calculate_dist_affected_due_aircraft_weight_class\
                (a1['aircraft_weight_class'], b1['aircraft_weight_class'], distance_affected_due_wind)
            distance_affected_due_ground_traffic = calculate_dist_affected_due_ground_traffic\
                (a1['ground_traffic'], b1['ground_traffic'], distance_affected_due_aircraft_weight_class)
            distance_affected_due_air_traffic_congestion = calculate_dist_affected_due_air_traffic_congestion\
                (a1['air_traffic_congestion'], b1['air_traffic_congestion'], distance_affected_due_ground_traffic)
            temp_optimized_separation_minima = distance_affected_due_air_traffic_congestion

            to_append = [a1['weather'], b1['weather'], a1['wind'], b1['wind'], a1['aircraft_weight_class'], b1['aircraft_weight_class'],\
                           a1['ground_traffic'], b1['ground_traffic'], a1['air_traffic_congestion'], b1['air_traffic_congestion'], distance_affected_due_ground_traffic]
            a_series = pd.Series(to_append, index=df1.columns)
            df1 = df1.append(a_series, ignore_index=True)
            distance_list_hyp1.append(temp_optimized_separation_minima)

    # exporting to csv
    df1.to_csv('hyp1_small.csv')
    optimized_separation_minima_hyp1 = sum(distance_list_hyp1)/len(distance_list_hyp1)
    output_hyp1 = round(optimized_separation_minima_hyp1, 3)
    print("The final calculated separation minima for hypothesis 1 is {}".format(output_hyp1))


    # Testing Hypothesis-2:
    for i in range(1, 1001):
     name = 'airplane_{}'.format(i)
     airplane_objects_dict[name] = airplane_attributes(weather_decider, wind_decider, weight_decider, ground_traffic_decider, "hyp_2")
     if i > 1:
         airplane_name_1 = 'airplane_{}'.format(i - 1)
         airplane_name_2 = 'airplane_{}'.format(i)
         a2 = airplane_objects_dict[airplane_name_1].__dict__
         b2 = airplane_objects_dict[airplane_name_2].__dict__
         distance_affected_due_weather = calculate_dist_hyp_2(a2['weather'], b2['weather'], separation_minima)
         distance_affected_due_wind = calculate_dist_affected_due_wind(a2['wind'], b2['wind'], distance_affected_due_weather)
         distance_affected_due_aircraft_weight_class = calculate_dist_affected_due_aircraft_weight_class\
             (a2['aircraft_weight_class'], b2['aircraft_weight_class'], distance_affected_due_wind)
         distance_affected_due_ground_traffic = calculate_dist_affected_due_ground_traffic\
             (a2['ground_traffic'], b2['ground_traffic'], distance_affected_due_aircraft_weight_class)
         distance_affected_due_air_traffic_congestion = calculate_dist_affected_due_air_traffic_congestion\
             (a2['air_traffic_congestion'], b2['air_traffic_congestion'], distance_affected_due_ground_traffic)
         temp_optimized_separation_minima = distance_affected_due_air_traffic_congestion

         to_append = [a2['weather'], b2['weather'], a2['wind'], b2['wind'], a2['aircraft_weight_class'], b2['aircraft_weight_class'], \
                      a2['ground_traffic'], b2['ground_traffic'], a2['air_traffic_congestion'], b2['air_traffic_congestion'], distance_affected_due_ground_traffic]
         a_series = pd.Series(to_append, index=df1.columns)
         df2 = df2.append(a_series, ignore_index=True)

         distance_list_hyp2.append(temp_optimized_separation_minima)

    # exporting to csv
    df2.to_csv('hyp2_small.csv')
    optimized_separation_minima_hyp2 = sum(distance_list_hyp2)/len(distance_list_hyp2)
    output_hyp2 = round(optimized_separation_minima_hyp2, 3)
    print("\nThe final calculated separation minima for hypothesis 2 is {}".format(output_hyp2))