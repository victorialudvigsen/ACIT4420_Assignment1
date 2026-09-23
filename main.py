from sample_data import (
    participant_data,
    resting_data,
    moderate_data,
    high_activity_data,
    recovery_data,
    invalid_data
)

class Participant:
    """Represents a participant and their normal reference measurements."""

    def __init__(self, name, resting_heart_rate, reference_temperature,
                 reference_skin_response):
        self.name = name

        # Protected attribute controlled through a property
        self.resting_heart_rate = resting_heart_rate

        self.reference_temperature = reference_temperature
        self.reference_skin_response = reference_skin_response

    @property
    def resting_heart_rate(self):
        return self._resting_heart_rate

    @resting_heart_rate.setter
    def resting_heart_rate(self, value):
        if value > 0:
            self._resting_heart_rate = value
        else:
            raise ValueError("Resting heart rate must be greater than 0.")


class Observation:
    """Represents one observation window from the fitness sensor."""

    def __init__(self, timestamp, heart_rate, skin_response,
                 temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality

    @staticmethod
    def is_valid_heart_rate(value):
        # Project assumption: heart rate must be between 30 and 220 bpm
        return value is not None and 30 <= value <= 220

    @staticmethod
    def is_valid_ratio(value):
        # Activity level and signal quality are represented from 0 to 1
        return value is not None and 0 <= value <= 1

    def is_usable(self):
        """Checks whether the observation contains usable sensor data."""

        if self.timestamp is None or self.timestamp < 0:
            return False

        if not self.is_valid_heart_rate(self.heart_rate):
            return False

        if self.skin_response is None or self.skin_response < 0:
            return False

        if self.temperature is None or not 20 <= self.temperature <= 45:
            return False

        if not self.is_valid_ratio(self.activity_level):
            return False

        if not self.is_valid_ratio(self.signal_quality):
            return False

        # Very poor signal quality is not considered usable
        if self.signal_quality < 0.5:
            return False

        return True


class Session:
    """Represents one fitness session for a participant."""

    def __init__(self, participant):
        self.participant = participant
        self.observations = []

    def add_observation(self, observation):
        self.observations.append(observation)

    def get_usable_observations(self):
        usable_observations = []

        for observation in self.observations:
            if observation.is_usable():
                usable_observations.append(observation)

        return usable_observations


class Analyzer:
    """Analyzes usable observations from a fitness session."""

    def __init__(self, session):
        self.session = session

    def get_heart_rates(self):
        heart_rates = []

        for observation in self.session.get_usable_observations():
            heart_rates.append(observation.heart_rate)

        return heart_rates

    def get_activity_levels(self):
        activity_levels = []

        for observation in self.session.get_usable_observations():
            activity_levels.append(observation.activity_level)

        return activity_levels

    def get_temperatures(self):
        temperatures = []

        for observation in self.session.get_usable_observations():
            temperatures.append(observation.temperature)

        return temperatures

    def get_skin_responses(self):
        skin_responses = []

        for observation in self.session.get_usable_observations():
            skin_responses.append(observation.skin_response)

        return skin_responses

    def get_heart_rate_summary(self):
        heart_rates = self.get_heart_rates()
        return create_summary(heart_rates)

    def get_activity_summary(self):
        activity_levels = self.get_activity_levels()
        return create_summary(activity_levels)

    def get_temperature_summary(self):
        temperatures = self.get_temperatures()
        return create_summary(temperatures)

    def get_skin_response_summary(self):
        skin_responses = self.get_skin_responses()
        return create_summary(skin_responses)

    def compare_with_reference(self):
        """Compares session averages with the participant's reference values."""

        usable_observations = self.session.get_usable_observations()

        if len(usable_observations) == 0:
            return {
                "heart_rate_difference": None,
                "temperature_difference": None,
                "skin_response_difference": None
            }

        participant = self.session.participant

        heart_rate_average = self.get_heart_rate_summary()["average"]
        temperature_average = self.get_temperature_summary()["average"]
        skin_response_average = self.get_skin_response_summary()["average"]

        return {
            "heart_rate_difference":
                heart_rate_average - participant.resting_heart_rate,

            "temperature_difference":
                temperature_average - participant.reference_temperature,

            "skin_response_difference":
                skin_response_average - participant.reference_skin_response
        }

    def is_recovering(self):
        usable_observations = self.session.get_usable_observations()

        # At least four observations are needed to identify a recovery trend
        if len(usable_observations) < 4:
            return False

        third_last = usable_observations[len(usable_observations) - 3]
        second_last = usable_observations[len(usable_observations) - 2]
        last = usable_observations[len(usable_observations) - 1]

        heart_rate_declining = (
            third_last.heart_rate > second_last.heart_rate
            and second_last.heart_rate > last.heart_rate
        )

        activity_declining = (
            third_last.activity_level > second_last.activity_level
            and second_last.activity_level > last.activity_level
        )

        # Recovery should follow a period of clear activity
        was_active = third_last.activity_level >= 0.70

        return heart_rate_declining and activity_declining and was_active

    def classify_session(self):
        usable_observations = self.session.get_usable_observations()

        # Too little valid data gives an unreliable classification
        if len(usable_observations) < 3:
            return "insufficient data"

        if self.is_recovering():
            return "recovering"

        heart_rate_summary = self.get_heart_rate_summary()
        activity_summary = self.get_activity_summary()

        average_heart_rate = heart_rate_summary["average"]
        average_activity = activity_summary["average"]

        resting_heart_rate = self.session.participant.resting_heart_rate

        # Classification rules used in this project
        if average_activity < 0.25 and average_heart_rate <= resting_heart_rate + 20:
            return "resting"

        elif average_activity >= 0.70 or average_heart_rate >= resting_heart_rate + 60:
            return "high activity"

        else:
            return "moderate activity"

    def get_classification_explanation(self):
        classification = self.classify_session()

        if classification == "insufficient data":
            return "There are fewer than three usable observations."

        elif classification == "recovering":
            return "Heart rate and activity declined near the end after a period of clear activity."

        elif classification == "resting":
            return "Average heart rate and activity level are close to resting values."

        elif classification == "high activity":
            return "Heart rate or activity level is clearly elevated."

        else:
            return "Heart rate and activity level indicate moderate activity."

    def analyze(self):
        """Returns the complete analysis as a structured dictionary."""

        usable_observations = self.session.get_usable_observations()

        return {
            "participant": self.session.participant.name,
            "total_observations": len(self.session.observations),
            "usable_observations": len(usable_observations),
            "classification": self.classify_session(),
            "explanation": self.get_classification_explanation(),
            "heart_rate": self.get_heart_rate_summary(),
            "activity_level": self.get_activity_summary(),
            "temperature": self.get_temperature_summary(),
            "skin_response": self.get_skin_response_summary(),
            "reference_comparison": self.compare_with_reference()
        }


def calculate_average(values):
    """Calculates the average of a list of numerical values."""

    if len(values) == 0:
        return None

    total = 0

    for value in values:
        total += value

    return total / len(values)


def calculate_minimum(values):
    """Finds the minimum value in a list."""

    if len(values) == 0:
        return None

    minimum = values[0]

    for value in values:
        if value < minimum:
            minimum = value

    return minimum


def calculate_maximum(values):
    """Finds the maximum value in a list."""

    if len(values) == 0:
        return None

    maximum = values[0]

    for value in values:
        if value > maximum:
            maximum = value

    return maximum


def create_summary(values):
    """Creates a summary of numerical values."""

    return {
        "average": calculate_average(values),
        "minimum": calculate_minimum(values),
        "maximum": calculate_maximum(values)
    }

def print_report(result):
    """Prints a readable fitness session report."""

    print("\nFITNESS SESSION REPORT")
    print("----------------------")

    print(f"Participant: {result['participant']}")
    print(f"Usable observations: {result['usable_observations']}/{result['total_observations']}")
    print(f"Classification: {result['classification']}")
    print(f"Explanation: {result['explanation']}")

    # Only show measurement summaries when usable data exists
    if result["usable_observations"] > 0:
        print("\nHeart rate:")
        print(f"  Average: {result['heart_rate']['average']:.2f} bpm")
        print(f"  Minimum: {result['heart_rate']['minimum']} bpm")
        print(f"  Maximum: {result['heart_rate']['maximum']} bpm")

        print("\nActivity level:")
        print(f"  Average: {result['activity_level']['average']:.2f}")

        print("\nTemperature:")
        print(f"  Average: {result['temperature']['average']:.2f}")

        print("\nSkin response:")
        print(f"  Average: {result['skin_response']['average']:.2f}")

        comparison = result["reference_comparison"]

        print("\nDifference from reference values:")
        print(f"  Heart rate: {comparison['heart_rate_difference']:.2f} bpm")
        print(f"  Temperature: {comparison['temperature_difference']:.2f}")
        print(f"  Skin response: {comparison['skin_response_difference']:.2f}")

    else:
        print("\nNo usable sensor measurements were available.")


def create_session(participant, observations_data):
    """Creates a session from a list of observation dictionaries."""

    session = Session(participant)

    for data in observations_data:
        observation = Observation(
            data["timestamp"],
            data["heart_rate"],
            data["skin_response"],
            data["temperature"],
            data["activity_level"],
            data["signal_quality"]
        )

        session.add_observation(observation)

    return session


def run_scenarios():
    """Runs and reports the five required sample scenarios."""

    # Create the participant from the sample data
    participant = Participant(
        participant_data["name"],
        participant_data["resting_heart_rate"],
        participant_data["reference_temperature"],
        participant_data["reference_skin_response"]
    )

    # The five required scenarios
    scenarios = [
        ("Resting session", resting_data),
        ("Moderate activity", moderate_data),
        ("High activity", high_activity_data),
        ("Activity followed by recovery", recovery_data),
        ("Poor-quality or invalid data", invalid_data)
    ]

    # Analyze and report each scenario
    for scenario_name, scenario_data in scenarios:
        print("\n")
        print("=" * 50)
        print(scenario_name.upper())
        print("=" * 50)

        session = create_session(participant, scenario_data)
        analyzer = Analyzer(session)
        result = analyzer.analyze()

        print_report(result)


if __name__ == "__main__":
    run_scenarios()