from main import Participant, Analyzer, create_session
from option_a_fitness.data_generator import generate_fitness_data


def analyze_scenario(scenario):
    """Generates and analyzes one fitness scenario."""

    # Generate reproducible test data from the instructor-supplied generator
    profile, observations_data = generate_fitness_data(
        participant_id="P001",
        scenario=scenario,
        seed=42,
        number_of_windows=12
    )

    # Convert the generated participant profile into our Participant object
    participant = Participant(
        profile["participant_id"],
        profile["baseline_heart_rate"],
        profile["baseline_temperature"],
        profile["baseline_skin_response"]
    )

    # Convert the observation dictionaries into Observation objects
    # and place them inside a Session
    session = create_session(participant, observations_data)

    # Analyze the complete session and return the result dictionary
    analyzer = Analyzer(session)
    return analyzer.analyze()


def test_resting():
    """Tests that resting data is classified correctly."""

    result = analyze_scenario("resting")

    # All observations should be usable in the normal resting scenario
    assert result["classification"] == "resting"
    assert result["usable_observations"] == 12

    print("Resting session test passed.")


def test_moderate_activity():
    """Tests that moderate activity data is classified correctly."""

    result = analyze_scenario("moderate_activity")

    # The generated scenario should be recognized as moderate activity
    assert result["classification"] == "moderate activity"
    assert result["usable_observations"] == 12

    print("Moderate activity test passed.")


def test_high_activity():
    """Tests that high activity data is classified correctly."""

    result = analyze_scenario("high_activity")

    # The generated scenario should be recognized as high activity
    assert result["classification"] == "high activity"
    assert result["usable_observations"] == 12

    print("High activity test passed.")


def test_recovery():
    """Tests that a recovery trend is detected correctly."""

    result = analyze_scenario("recovery")

    # Heart rate and activity should decline toward resting values
    assert result["classification"] == "recovering"
    assert result["usable_observations"] == 12

    print("Recovery test passed.")


def test_poor_quality():
    """Tests handling of missing, impossible, and poor-quality data."""

    result = analyze_scenario("poor_quality")

    # The supplied poor-quality scenario contains unusable sensor values
    assert result["classification"] == "insufficient data"
    assert result["usable_observations"] == 0

    print("Poor-quality data test passed.")


if __name__ == "__main__":
    # Run all five required scenario tests
    test_resting()
    test_moderate_activity()
    test_high_activity()
    test_recovery()
    test_poor_quality()

    print("\nAll tests passed.")