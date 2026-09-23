from main import Participant, Analyzer, create_session

from sample_data import (
    participant_data,
    resting_data,
    moderate_data,
    high_activity_data,
    recovery_data,
    invalid_data
)


# Create the participant used in all test scenarios
participant = Participant(
    participant_data["name"],
    participant_data["resting_heart_rate"],
    participant_data["reference_temperature"],
    participant_data["reference_skin_response"]
)


# Test 1: Resting session
resting_session = create_session(participant, resting_data)
resting_result = Analyzer(resting_session).analyze()

assert resting_result["classification"] == "resting"
assert resting_result["usable_observations"] == 3

print("Resting session test passed.")


# Test 2: Moderate activity
moderate_session = create_session(participant, moderate_data)
moderate_result = Analyzer(moderate_session).analyze()

assert moderate_result["classification"] == "moderate activity"
assert moderate_result["usable_observations"] == 3

print("Moderate activity test passed.")


# Test 3: High activity
high_session = create_session(participant, high_activity_data)
high_result = Analyzer(high_session).analyze()

assert high_result["classification"] == "high activity"
assert high_result["usable_observations"] == 3

print("High activity test passed.")


# Test 4: Activity followed by recovery
recovery_session = create_session(participant, recovery_data)
recovery_result = Analyzer(recovery_session).analyze()

assert recovery_result["classification"] == "recovering"
assert recovery_result["usable_observations"] == 4

print("Recovery test passed.")


# Test 5: Poor-quality and invalid sensor data
invalid_session = create_session(participant, invalid_data)
invalid_result = Analyzer(invalid_session).analyze()

assert invalid_result["classification"] == "insufficient data"
assert invalid_result["usable_observations"] == 0

print("Invalid data test passed.")


print("\nAll tests passed.")