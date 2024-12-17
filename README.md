# Flight Scheduling System
Mixed-integer linear programming model to schedule flights and distribute aircraft to minimize cost.

## Usage
Run `instance_gen.py` to generate an instance.  
You can edit the specific values to your liking in the CSV files under src/instance.
Run `lp.py` to find a solution.

You can alternatively call the `lp.solve_instance` function directly by passing in your instance data (aircraft, airports, and routes).
## Math
Decision variables are $x_{i,j}$ where $i$ is the aircraft index and $j$ is the route index and $\forall x_{i,j} \in \left\\{ 0,1 \right\\} $

Let $a_i$ be aircraft with index $i \in \mathbb{Z}^+$ and let $r_j$ be route with index $j \in \mathbb{Z}^+$.  
I approximate the variable cost, $c$, of running a route as $$c_{i,j}=x_{i,j} \cdot \text{efficiency} \left( a_i \right) \cdot \text{distance}\left(r_j\right)$$

The objective function is $MIN_{i,j} (c)$

The model considers the following constraints:
- each route must be covered exactly once
- the solution cannot use more aircraft than described in the fleet
- aircraft can carry strictly less than their maximum payload (cargo + passenger)
- aircraft cannot service a route who's distance is larger than the aircraft's range

### Notes
All airports and aircraft in the model are real-to-life.
Distances are calculated and cached at runtime based on airport locations using the haversine formula.
Routes are strictly unique and route A → B $\ne$ B → A.

## Datasets
- ["Our Airports" Open Dataset](https://github.com/davidmegginson/ourairports-data/blob/main/airports.csv)
- Various manufacturer resources for aircraft specs

## What's next?
- [ ] route visualizer
- [ ] nonlinear fuel function

Aly Ashour

  
