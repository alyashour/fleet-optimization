from dataclasses import dataclass
from functools import lru_cache
from haversine import haversine, Unit  # for distances between points on globe (lat/lon)


@lru_cache(maxsize=64)
def _find_distance(lat1, lon1, lat2, lon2):
    return haversine((lat1, lon1), (lat2, lon2))

@dataclass
class Airport:
    def __init__(self, name: str, code: str, lat: float, lon: float, city: str, country: str):
        self.name = name
        self.code = code
        self.lat = lat
        self.lon = lon
        self.city = city
        self.country = country

    def distance(self, other: "Airport"):
        return _find_distance(self.lat, self.lon, other.lat, other.lon)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def __repr__(self):
        return f"Airport({self.name}, {self.code}, {self.lat}, {self.lon}, {self.city}, {self.country})"

    def __eq__(self, other):
        return self.code == other.code

def test(tolerance=0.005):
    a1 = Airport("JFK", "John F. Kennedy International Airport", 40.6413, -73.7781)
    a2 = Airport("LAX", "Los Angeles International Airport", 33.9416, -118.4085)
    print(a1)
    print(a2)
    dist = a1.distance(a2)
    expected = 3974.20

    print(f"Distance between {a1} and {a2} is {dist} km")
    print(f"Expected: {expected}")  # according to https://www.distance.to/JFK/LAX#:~:text=Distance%20from%20JFK%20to%20LAX&text=The%20shortest%20distance%20(air%20line,2%2C469.45%20mi%20(3%2C974.20%20km).&text=The%20shortest%20route%20between%20JFK,50h%2022min.

    print(f"Test {"passed" if abs(dist - expected) < tolerance * expected else "failed"}",
              "| tolerance:", f"{tolerance * 100}%",
          "difference:", round(abs(dist - expected), 3),
          f"({abs(dist-expected)/expected*100:.2f}%)"
    )

if __name__ == "__main__":
    test()