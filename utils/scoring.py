# utils/scoring.py

SCORES = {
    "Yes": 3,
    "Not Sure": 2,
    "No": 0
}

def calculate_total_score(answers):
    total = 0
    for ans in answers:
        total += SCORES.get(ans, 0)
    return total

def calculate_risk_level(score):
    percent = (score / 60) * 100

    if percent < 30:
        return "Low"
    elif percent < 60:
        return "Medium"
    else:
        return "High"