from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary
import pandas as pd

from aircraft import Aircraft
from airport import Airport
from route import Route

# constants
WEIGHT_PER_PASSENGER = 0  # kg

def solve_instance_from_csv(airplanes_csv_path: str, airports_csv_path: str, routes_csv_path: str) -> dict:
    # load data
    airplanes_df = pd.read_csv(airplanes_csv_path)
    airports_df = pd.read_csv(airports_csv_path)
    routes_df = pd.read_csv(routes_csv_path)

    # create objects
    airplanes = []
    for index, row in airplanes_df.iterrows():
        airplane = Aircraft(row["model"], row["code"], row["max_range"], row["fuel_efficiency"], row["max_payload"], row["count"])
        airplanes.append(airplane)

    airports = {}
    for index, row in airports_df.iterrows():
        airport = Airport(row["name"], row["code"], row["lat"], row["lon"], row["city"], row["country"])
        airports[row["code"]] = airport

    routes = []
    for index, row in routes_df.iterrows():
        origin = airports[row["origin"]]
        destination = airports[row["destination"]]
        route = Route(row["route_id"], origin, destination, row["passenger_load"], row["cargo_load"])
        routes.append(route)

    return solve_instance(airplanes, routes)

def solve_instance(airplanes: list[Aircraft], routes: list[Route]) -> dict:
    model = LpProblem("Flight_Assignment", LpMinimize)

    # decision vars
    x = {
        (i, j): LpVariable(name=f"x_{i}_{j}", cat=LpBinary)
        for i in range(len(airplanes))
        for j in range(len(routes))
    }

    # objective: maximize the total cost
    model += lpSum(
        x[(i, j)] *
        airplanes[i].fuel_efficiency * routes[j].distance
        for i in range(len(airplanes))
        for j in range(len(routes))
    )

    # constraint: each flight is covered exactly once
    for j in range(len(routes)):
        model += lpSum(x[i, j] for i in range(len(airplanes))) == 1, f"FlightCoveredOnce_{j}"

    # constraint: fleet count limits
    for i in range(len(airplanes)):
        model += lpSum(x[i, j] for j in range(len(routes))) <= airplanes[i].count, f"FleetLimit_{i}"

    # constraint payload limits
    for i in range(len(airplanes)):
        for j in range(len(routes)):
            total_load = routes[j].passenger_load * WEIGHT_PER_PASSENGER + routes[j].cargo_load
            model += (total_load * x[i, j] <= airplanes[i].max_payload), f"PayloadLimit_{i}_{j}"

    for i in range(len(airplanes)):
        for j in range(len(routes)):
            model += x[i, j] * routes[j].distance <= airplanes[i].max_range, f"RangeLimit_{i}_{j}"

    # solve
    status = model.solve()

    # check every route has an assigned plane
    for j in range(len(routes)):
        assigned_planes = [x[i, j].value() for i in range(len(airplanes))]
        if sum(assigned_planes) != 1:
            raise Exception("Could not assign all flights! "
                            "Please make sure your configuration is correct as there may not be enough airplanes to saturate all routes!")

    # check payload constraints are respected
    for i in range(len(airplanes)):
        for j in range(len(routes)):
            if x[i, j].value() == 1:
                payload = (routes[j].passenger_load * WEIGHT_PER_PASSENGER + routes[j].cargo_load)
                max_payload = airplanes[i].max_payload
                if payload > max_payload:
                    raise f"Error: Flight {routes[j].route_id} exceeds payload limit for Airplane {airplanes[i].model}."

    # print results
    print("Status: ", status)
    print("Objective value (Total Cost): ", model.objective.value())

    r = {}
    for i in range(len(airplanes)):
        for j in range(len(routes)):
            if x[i, j].value() == 1:
                print(f"Airplane {airplanes[i].model} assigned to flight {routes[j].route_id}")
                r[routes[j].route_id] = airplanes[i]

    return r


if __name__ == "__main__":
    result = solve_instance_from_csv("instance/airplanes.csv", "instance/airports.csv", "instance/routes.csv")
    print(result)