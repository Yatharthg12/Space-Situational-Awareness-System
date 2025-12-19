def classify_risk(distance_km):
    if distance_km < 2:
        return "HIGH"
    elif distance_km < 10:
        return "MEDIUM"
    else:
        return "LOW"
