"""
Generates a set of airport, plane, and flight data to be analyzed
This set is a random subset of all the available data
"""
import dataclasses
import itertools
import random
import pandas as pd

from Airplane import Airplane
from Airport import Airport
from Route import Route

# random gen seed
SEED = 42456789

# size of each subset that will be randomly selected
NUM_AIRPORTS = 5
NUM_AIRCRAFT = 8  # for all aircraft, put 8
NUM_ROUTES = 10

# config
MIN_PASSENGER_LOAD = 50
MAX_PASSENGER_LOAD = 300
MIN_CARGO_LOAD = 1000
MAX_CARGO_LOAD = 10_000

def gen(debug=False, save_instance=True):
    random.seed(SEED)

    # airport data
    airports_df = pd.read_csv('../data/base/large_airports.csv')
    sampled_airports_df = airports_df.sample(n=NUM_AIRPORTS, random_state=SEED)
    airports = [Airport(
        name=row['name'],
        code=row['iata_code'],
        lat=row['latitude_deg'],
        lon=row['longitude_deg'],
        city=row['municipality'],
        country=row['iso_country']
    ) for index, row in sampled_airports_df.iterrows()]

    if debug:
        print(airports)

    # airplane data
    airplanes_df = pd.read_csv("../data/base/aircraft_data.csv")
    sampled_airplanes_df = airplanes_df.sample(n=NUM_AIRCRAFT, random_state=SEED)
    airplanes = [Airplane(
        model=row["Aircraft Model"],
        code=row["Code"],
        max_range=row["Max Range (km)"],
        fuel_efficiency=row["Fuel Efficiency (L/km)"],
        max_payload=row["Max Payload (kg)"]
    ) for index, row in sampled_airplanes_df.iterrows()]

    if debug:
        print(airplanes)

    # route data
    possible_routes = list(itertools.combinations(airports, 2))
    selected_routes = random.sample(possible_routes, NUM_ROUTES)

    routes = []
    for i, (origin, destination) in enumerate(selected_routes):
        passenger_load = random.randint(MIN_PASSENGER_LOAD, MAX_PASSENGER_LOAD)
        cargo_load = random.randint(MIN_CARGO_LOAD, MAX_CARGO_LOAD)
        routes.append(Route(
            route_id=f"FL{(i + 1):03}",
            origin=origin,
            destination=destination,
            passenger_load=passenger_load,
            cargo_load=cargo_load
        ))
    if debug:
        print(routes)

    # save the instance if needed
    if save_instance:
        airports_df = pd.DataFrame([a.__dict__ for a in airports])
        airplanes_df = pd.DataFrame([a.__dict__ for a in airplanes])
        routes_df = pd.DataFrame([r.__dict__ for r in routes])
        airports_df.to_csv("instance/airports.csv", header=True, index=False)
        airplanes_df.to_csv("instance/airplanes.csv", header=True, index=False)
        routes_df.to_csv("instance/routes.csv", header=True, index=False)

        print("Dataset generated!")

if __name__ == "__main__":
    gen(debug=True)