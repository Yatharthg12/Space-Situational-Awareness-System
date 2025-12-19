from sgp4.api import Satrec, jday
from datetime import timedelta

def propagate_object(line1, line2, start_time, duration_minutes=2880, step_minutes=5):
    """
    Propagates a single space object using SGP4.
    Returns a list of position dicts with time and ECI coordinates (km).
    """
    satellite = Satrec.twoline2rv(line1, line2)
    positions = []

    current_time = start_time
    steps = duration_minutes // step_minutes

    for _ in range(steps):
        jd, fr = jday(
            current_time.year,
            current_time.month,
            current_time.day,
            current_time.hour,
            current_time.minute,
            current_time.second
        )

        error, position, velocity = satellite.sgp4(jd, fr)

        if error == 0:
            positions.append({
                "time": current_time,
                "x": position[0],
                "y": position[1],
                "z": position[2]
            })

        current_time += timedelta(minutes=step_minutes)

    return positions


def propagate_all_objects(matched_objects, start_time):
    """
    Propagates all matched objects.
    Returns a dict:
    {
        index: {
            'name': str,
            'type': str,
            'trajectory': [...]
        }
    }
    """
    trajectories = {}

    for idx, obj in enumerate(matched_objects):
        traj = propagate_object(
            obj["line1"],
            obj["line2"],
            start_time
        )

        trajectories[idx] = {
            "name": obj["name"],
            "type": obj["type"],
            "trajectory": traj
        }

    return trajectories
