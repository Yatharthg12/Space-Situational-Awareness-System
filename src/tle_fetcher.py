import csv

def parse_tle_file(filepath):
    objects = []

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    i = 0
    while i <= len(lines) - 3:
        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]

        if line1.startswith("1 ") and line2.startswith("2 "):
            objects.append({
                "name": name,
                "line1": line1,
                "line2": line2
            })
            i += 3
        else:
            i += 1

    return objects


def load_all_tles():
    tle_sources = {
        "active": "data/tle_active.txt",
        "debris": "data/tle_debris.txt",
        "stations": "data/tle_stations.txt"
    }

    return {k: parse_tle_file(v) for k, v in tle_sources.items()}


def load_selected_objects(csv_path="data/selected_objects.csv"):
    selected = []

    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            selected.append({
                "name": row["name"].strip(),
                "type": row["type"].strip(),
                "source": row["source"].strip()
            })

    return selected


def match_selected_to_tles(
    selected_objects,
    all_tles,
    debris_limit_per_name=25
):
    """
    Matches selected objects to TLEs with controlled debris sampling.
    """

    matched = []
    debris_counter = {}

    for sel in selected_objects:
        name_key = sel["name"]
        source = sel["source"]

        candidates = all_tles.get(source, [])

        for obj in candidates:
            if name_key in obj["name"]:

                # Apply debris limit
                if sel["type"] == "satellite_debris":
                    count = debris_counter.get(name_key, 0)
                    if count >= debris_limit_per_name:
                        continue
                    debris_counter[name_key] = count + 1

                matched.append({
                    "name": obj["name"],
                    "type": sel["type"],
                    "source": source,
                    "line1": obj["line1"],
                    "line2": obj["line2"]
                })

    return matched
