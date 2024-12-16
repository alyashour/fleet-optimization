import random


class Fleet(list):
    def __init__(self):
        super().__init__()

    @property
    def size(self):
        size = 0
        for aircraft in super().__iter__():
            size += aircraft.count
        return size

    def add_aircraft(self, aircraft):
        super().append(aircraft)

    def grow_to_size(self, target_size):
        while self.size < target_size:
            delta = target_size - self.size
            purchase_amt = int(delta//2 if delta > 2 else delta)
            random.choice(self).__purchase__(purchase_amt)
        assert self.size == target_size