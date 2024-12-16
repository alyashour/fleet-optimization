from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpBinary
import pandas as pd

def solve_instance():
    # load data
    airplanes_df = pd.read_csv("instance/airplanes.csv")
    routes_df = pd.read_csv("instance/routes.csv")

    # constants
    WEIGHT_PER_PASSENGER = 100  # kg

    model = LpProblem("Flight_Assignment", LpMinimize)

    # decision vars
    x = {
        (i, j): LpVariable(name=f"x_{i}_{j}", cat=LpBinary)
        for i in range(len(airplanes_df))
        for j in range(len(routes_df))
    }

    # objective: maximize the total cost
    model += lpSum(
        x[(i, j)] *
        airplanes_df.loc[i, "fuel_efficiency"] * routes_df.loc[j, "distance"]
        for i in range(len(airplanes_df))
        for j in range(len(routes_df))
    )

    # constraint: each flight is covered exactly once
    for j in range(len(routes_df)):
        model += lpSum(x[i, j] for i in range(len(airplanes_df))) == 1

    # constraint: fleet count limits
    for i in range(len(airplanes_df)):
        model += lpSum(x[i, j] for j in range(len(routes_df))) <= airplanes_df.loc[i, "count"], f"FleetLimit_{i}"

    # constraint payload limits
    for i in range(len(airplanes_df)):
        for j in range(len(routes_df)):
            total_load = routes_df.loc[j, "passenger_load"] * WEIGHT_PER_PASSENGER + routes_df.loc[j, "cargo_load"]
            model += (total_load * x[i, j] <= airplanes_df.loc[i, "max_payload"])

    for i in range(len(airplanes_df)):
        for j in range(len(routes_df)):
            model += x[i, j] * routes_df.loc[j, "distance"] <= airplanes_df.loc[i, "max_range"]

    # solve
    status = model.solve()

    # # check every route has an assigned plane
    # for j in range(len(routes_df)):
    #     assigned_planes = [x[i, j].value() for i in range(len(airplanes_df))]
    #     if sum(assigned_planes) != 1:
    #         raise f"Error: Flight {routes_df.loc[j, 'flight_id']} is not properly assigned!"

    # check payload constraints are respected
    for i in range(len(airplanes_df)):
        for j in range(len(routes_df)):
            if x[i, j].value() == 1:
                payload = (routes_df.loc[j, "passenger_load"] * WEIGHT_PER_PASSENGER + routes_df.loc[j, "cargo_load"])
                max_payload = airplanes_df.loc[i, "max_payload"]
                if payload > max_payload:
                    raise f"Error: Flight {routes_df.loc[j, 'flight_id']} exceeds payload limit for Airplane {airplanes_df.loc[i, 'name']}."

    # print results
    print("Status: ", status)
    print("Objective value (Total Cost): ", model.objective.value())

    result = {}
    for i in range(len(airplanes_df)):
        for j in range(len(routes_df)):
            if x[i, j].value() == 1:
                print(f"Airplane {airplanes_df.loc[i, 'code']} assigned to flight {routes_df.loc[j, 'route_Id']}")
                result[routes_df.loc[j, 'route_Id']] = airplanes_df.loc[i, 'code']

    return result


if __name__ == "__main__":
    result = solve_instance()
    print(result)