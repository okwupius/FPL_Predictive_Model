# Dashboards/utils.py

POSITION_MAP = {
    1: "GK",
    2: "DEF",
    3: "MID",
    4: "FWD"
}

def fixture_icon(value):

    if value <= 2:
        return "🟢"

    elif value == 3:
        return "🟡"

    return "🔴"


def health_status(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    return "Poor"


def gain_label(x):

    if x >= 5:
        return f"🟢 +{x:.2f}"

    elif x > 0:
        return f"🟡 +{x:.2f}"

    return f"🔴 {x:.2f}"