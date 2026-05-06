def calculate_surge_multiplier(demand_score, supply_count):
    supply_count = max(supply_count, 1)

    estimated_demand = demand_score * 10
    ratio = estimated_demand / supply_count

    if ratio <= 1:
        surge = 1.0
    elif ratio <= 1.5:
        surge = 1.2
    elif ratio <= 2:
        surge = 1.5
    elif ratio <= 3:
        surge = 2.0
    else:
        surge = min(3.0, 1 + (ratio - 1) * 0.5)

    return round(surge, 2)