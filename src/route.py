from dataclasses import dataclass
from airport import Airport

@dataclass
class Route:
    def __init__(self, route_id: str, origin: Airport, destination: Airport, passenger_load: int, cargo_load: int):
        self.route_Id = route_id
        self.origin = origin
        self.destination = destination
        self.passenger_load = passenger_load
        self.cargo_load = cargo_load

        self.distance = self.origin.distance(self.destination)

    def __str__(self):
        return f"{self.route_Id}: {self.origin} → {self.destination}"

    def __repr__(self):
        return f"Route({self.route_Id}, {self.origin} → {self.destination}, {self.passenger_load} passengers, {self.cargo_load} kg, {self.distance:.2f} km)"

