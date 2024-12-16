from dataclasses import dataclass


@dataclass
class Airplane:
    def __init__(self, model, code, max_range, fuel_efficiency, max_payload):
        self.model = model
        self.code = code
        self.max_range = max_range
        self.fuel_efficiency = fuel_efficiency
        self.max_payload = max_payload

    def __str__(self):
        return self.model

    def __repr__(self):
        return f"Airplane({self.model}, {self.code}, {self.max_range}, {self.fuel_efficiency}, {self.max_payload})"
