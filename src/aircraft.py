from dataclasses import dataclass


@dataclass
class Aircraft:
    def __init__(self, model: str, code: str, max_range: int, fuel_efficiency: float, max_payload: int, count=1):
        self.model = model
        self.code = code
        self.max_range = max_range
        self.fuel_efficiency = fuel_efficiency
        self.max_payload = max_payload
        self.count = count

    def __purchase__(self, n: int=1):
        self.count += n

    def __str__(self):
        return self.model

    def __repr__(self):
        return f"Airplane({self.model}, {self.code}, {self.max_range}, {self.fuel_efficiency}, {self.max_payload})"
