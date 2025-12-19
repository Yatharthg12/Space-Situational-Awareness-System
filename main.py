from datetime import datetime

from src.tle_fetcher import (
    load_all_tles,
    load_selected_objects,
    match_selected_to_tles
)

from src.propagator import propagate_all_objects
from src.conjunction import detect_conjunctions
from src.visualize import plot_orbits

# Load and match TLEs
all_tles = load_all_tles()
selected = load_selected_objects()
matched_objects = match_selected_to_tles(selected, all_tles)

print(f"Total matched objects: {len(matched_objects)}")

# Propagate
start_time = datetime.utcnow()
trajectories = propagate_all_objects(matched_objects, start_time)

print("Propagation complete.")

# Detect conjunctions (normal thresholds)
events = detect_conjunctions(trajectories)

print(f"Total conjunction events detected: {len(events)}")
print("Results saved to outputs/conjunction_events.csv")

# Visualization
plot_orbits(trajectories)
print("Orbit visualization saved to outputs/orbits.html")
