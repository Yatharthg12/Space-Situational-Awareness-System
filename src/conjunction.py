import math
import csv
import os


def euclidean_distance(p1, p2):
    return math.sqrt(
        (p1["x"] - p2["x"]) ** 2 +
        (p1["y"] - p2["y"]) ** 2 +
        (p1["z"] - p2["z"]) ** 2
    )


def find_closest_approach(traj1, traj2):
    min_distance = float("inf")
    tca = None

    for p1, p2 in zip(traj1, traj2):
        d = euclidean_distance(p1, p2)
        if d < min_distance:
            min_distance = d
            tca = p1["time"]

    return min_distance, tca


def detect_conjunctions(
    trajectories,
    high_risk_km=2,
    medium_risk_km=10,
    output_csv="outputs/conjunction_events.csv"
):
    events = []
    keys = list(trajectories.keys())

    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            obj1 = trajectories[keys[i]]
            obj2 = trajectories[keys[j]]

            min_dist, tca = find_closest_approach(
                obj1["trajectory"],
                obj2["trajectory"]
            )

            if min_dist < medium_risk_km:
                risk = "HIGH" if min_dist < high_risk_km else "MEDIUM"

                events.append({
                    "object_1": obj1["name"],
                    "object_2": obj2["name"],
                    "distance_km": round(min_dist, 3),
                    "tca": tca,
                    "risk": risk
                })

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Write CSV (even if empty)
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["object_1", "object_2", "distance_km", "tca", "risk"]
        )
        writer.writeheader()
        for event in events:
            writer.writerow(event)

    return events
