# IS597 2022 Spring Final Project : Monte Carlo Simulation to Derive Optimal Separation Minima during Commercial Aircraft Landing Sequence
### Team Members : 

Mathew Puthanpurackal (mathewjose47)

Ruchi Rao (raoruchi)
## Background

If we ever observe aircraft arriving at an airport, we would notice that the airplanes actually land in a queue
one after the other. In order to do so, each airplane in the queue has to maintain a certain distance from the current landing 
airplane to ensure a safe landing sequence. According to the guidelines given by the International Civil Aviation Organization(ICAO), 
the minimum separation distance between two aircraft in a landing sequence should be 5NM (Nautical Miles). Our project aims to
run a Monte Carlo simulation with the variables affecting a landing sequence to derive the optimal minimum separation, in the hopes
to reduce the distance.

If the optimum separation minima can be reduced further, it could be beneficial to the airline industry, thereby making the landing sequence
faster and more efficient.

![](https://upload.wikimedia.org/wikipedia/commons/e/e0/A340-300_landing_sequence_%284342008531%29.jpg)

## Randomized Variables

- **Weather:**  
In aviation, weather at airports is categorised based on the Runway Visibility Range (RVR), or in  simple terms, the distance of runway from the runway threshold - 
which is visible with the naked eye. This is because, reduction in visibility is directly proportional to the deterioration in weather. Hence, the main 3 categories we will include is:  
  - **cat_1:** This is Category 1 where RVR is not less than 800 m 
  - **cat_2:** This is Category 2 where RVR is not less than 300 m 
  - **cat_3:** This is Category 3 where RVR is from 200 m to 0 m
  

- **Wind:**  
There are mainly four types of wind in aviation:  
  - **headwind:** A headwind is wind blowing directly towards the front of the aircraft. A headwind increases drag. 
  - **tailwind:** A tailwind is wind blowing directly towards the rear of the aircraft. A tailwind assists the aircraft’s propulsion systems. 
  - **crosswind:** Winds blowing in any other direction than a headwind or tailwind. 
  - **wind_shear:** A sudden change in headwind or tailwind causing rapid changes in lift to the aircraft also known as ‘Wind Shear’ is one of the worst wind effects to experience.  
 

- **Weight Class:**  
This is a significant randomized variable to consider due to the concept of Wake Turbulence. Wake turbulence is a disturbance in the atmosphere that forms behind an
aircraft as it passes through the air. Heavier the aircraft, more is the wake turbulence. The different weight classes are based on Maximum Take-Off Mass (MTOM):  
  - **light:** MTOM < 7,000 kgs 
  - **medium:** 7,000 kgs < MTOM < 136,000 kgs 
  - **heavy:** MTOM >136,000 kgs 
  - **super:** Specific category for Airbus A380-800 and Antonov An-225


- **Ground Traffic:**  
This represents the aircraft traffic on taxiways. These planes would also be in a queue to get
ready for takeoff. Higher the ground traffic, higher would be the air traffic congestion.
The types of ground traffic assumed are **low**, **average** and **high**.


- **Air Traffic Congestion:**  
This variable would be dependent on ground_traffic. Our assumption is that if
ground_traffic is high, air_traffic_congestion is also **max**. If ground_traffic is
average or low, air_traffic_congestion is **regular**.

### Randomizing Variables:

We randomized our selected variables in three ways:

- **Weighted Probabilities**
  - Weight  
  ```self.temp_weight = random.choices(['light', 'medium', 'heavy', 'super'], weights=(5, 60, 30, 5), k=1)```
  - Wind  
  ```self.temp_wind = random.choices(['headwind', 'tailwind', 'crosswind', 'wind_shear'], weights=(80, 10, 5, 5), k=1)```
- **Controlled Randomization**
  - Weather - changes every 100 aircraft
  - Wind - changes every 10 aircraft 
  - Ground Traffic - changes every 20 aircraft
- **Derived Mid-Simulation**
  - Air Traffic Congestion - depends on Ground Traffic


## Hypothesis

### Hypothesis 1: The optimal separation between two aircraft in a landing sequence is less than 5 NM

### Hypothesis 2: During prolonged worst weather conditions, the optimal separation is affected not more than 2 NM

## Conclusion

## References

- https://ops.group/blog/wp-content/uploads/2017/03/ICAO-Doc4444-Pans-Atm-16thEdition-2016-OPSGROUP.pdf
- https://skybrary.aero/articles/mitigation-wake-turbulence-hazard
- https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap7_section_1.html
- https://www.southernwings.co.nz/the-effects-of-wind-on-aircraft/

## User Guide



