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


if __name__ == '__main__':
    airplane_objects_dict = {}
    weather_decider = weather_decider()
    wind_decider = wind_decider()
    weight_decider = weight_decider()
    ground_traffic_decider = ground_traffic_decider()

    # https://stackoverflow.com/questions/21598872/how-to-create-multiple-class-objects-with-a-loop-in-python
    for i in range(1, 10000):
        name = 'airplane_{}'.format(i)
        airplane_objects_dict[name] = airplane_attributes(weather_decider, wind_decider, weight_decider, ground_traffic_decider)

    # a = airplane_objects_dict['airplane_1'].__dict__
    # print(a['weather'])
    # for k, v in airplane_objects_dict.items():
    #     print(v.wind)
    for i in range(1, 10000):
        name_1 = 'airplane_{}'.format(i)
        name_2 = 'airplane_{}'.format(i+1)
        a = airplane_objects_dict[name_1].__dict__
        b = airplane_objects_dict[name_2].__dict__
        print(a)



