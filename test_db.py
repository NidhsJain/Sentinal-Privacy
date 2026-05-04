from utils.db import insert_privacy_result
import uuid

test_data = {
    "session_id": str(uuid.uuid4()),
    "answers": {"test_q": "Yes"},
    "category_scores": {"Network Privacy": 3},
    "total_score": 10.0,
    "risk_percentage": 25.0,
    "risk_level": "Low"
}

print("Running manual test insertion...")
insert_privacy_result(test_data)
print("Test completed.")
