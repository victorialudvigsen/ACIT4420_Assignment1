from option_a_fitness.data_generator import generate_fitness_data


class Participant:
    """Represents a participant and their normal reference measurements."""

    def __init__(self, participant_id, resting_heart_rate,
                 reference_temperature, reference_skin_response):
        self.participant_id = participant_id

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
        # Expected range from the supplied data description
        return value is not None and 35 <= value <= 205

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

        # Expected temperature range from the supplied data description
        if self.temperature is None or not 25 <= self.temperature <= 42:
            return False

        if not self.is_valid_ratio(self.activity_level):
            return False

        if not self.is_valid_ratio(self.signal_quality):
            return False

        # Project assumption: signal quality below 0.5 is too poor to use
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
        """Checks for a clear decline from activity toward resting values."""

        usable_observations = self.session.get_usable_observations()

        # The supplied generator always creates at least six observations
        if len(usable_observations) < 6:
            return False

        first_heart_rates = []
        last_heart_rates = []
        first_activity_levels = []
        last_activity_levels = []

        # Use the first three observations as the beginning of the session
        for index in range(3):
            observation = usable_observations[index]
            first_heart_rates.append(observation.heart_rate)
            first_activity_levels.append(observation.activity_level)

        # Use the last three observations as the end of the session
        for index in range(
            len(usable_observations) - 3,
            len(usable_observations)
        ):
            observation = usable_observations[index]
            last_heart_rates.append(observation.heart_rate)
            last_activity_levels.append(observation.activity_level)

        first_heart_rate_average = calculate_average(first_heart_rates)
        last_heart_rate_average = calculate_average(last_heart_rates)

        first_activity_average = calculate_average(first_activity_levels)
        last_activity_average = calculate_average(last_activity_levels)

        resting_heart_rate = self.session.participant.resting_heart_rate

        # Recovery should show a clear decline from the start to the end
        heart_rate_declined = (
            first_heart_rate_average >= last_heart_rate_average + 15
        )

        activity_declined = (
            first_activity_average >= last_activity_average + 0.20
        )

        # The session should begin with noticeable activity
        started_active = first_activity_average >= 0.55

        # Heart rate should move back toward the participant's baseline
        ended_near_resting = (
            last_heart_rate_average <= resting_heart_rate + 30
        )

        return (
            heart_rate_declined
            and activity_declined
            and started_active
            and ended_near_resting
        )

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

        # Classification thresholds are project assumptions
        if (
            average_activity < 0.25
            and average_heart_rate <= resting_heart_rate + 20
        ):
            return "resting"

        elif (
            average_activity >= 0.70
            or average_heart_rate >= resting_heart_rate + 60
        ):
            return "high activity"

        else:
            return "moderate activity"

    def get_classification_explanation(self):
        classification = self.classify_session()

        if classification == "insufficient data":
            return "There are fewer than three usable observations."

        elif classification == "recovering":
            return (
                "Heart rate and activity declined from higher activity "
                "toward resting values."
            )

        elif classification == "resting":
            return (
                "Average heart rate and activity level are close "
                "to resting values."
            )

        elif classification == "high activity":
            return "Heart rate or activity level is clearly elevated."

        else:
            return (
                "Heart rate and activity level indicate moderate activity."
            )

    def analyze(self):
        """Returns the complete analysis as a structured dictionary."""

        usable_observations = self.session.get_usable_observations()

        return {
            "participant": self.session.participant.participant_id,
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
    print(
        f"Usable observations: "
        f"{result['usable_observations']}/{result['total_observations']}"
    )
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
        print(f"  Minimum: {result['activity_level']['minimum']:.2f}")
        print(f"  Maximum: {result['activity_level']['maximum']:.2f}")

        print("\nTemperature:")
        print(f"  Average: {result['temperature']['average']:.2f}")
        print(f"  Minimum: {result['temperature']['minimum']:.2f}")
        print(f"  Maximum: {result['temperature']['maximum']:.2f}")

        print("\nSkin response:")
        print(f"  Average: {result['skin_response']['average']:.2f}")
        print(f"  Minimum: {result['skin_response']['minimum']:.2f}")
        print(f"  Maximum: {result['skin_response']['maximum']:.2f}")

        comparison = result["reference_comparison"]

        print("\nDifference from reference values:")
        print(
            f"  Heart rate: "
            f"{comparison['heart_rate_difference']:.2f} bpm"
        )
        print(
            f"  Temperature: "
            f"{comparison['temperature_difference']:.2f}"
        )
        print(
            f"  Skin response: "
            f"{comparison['skin_response_difference']:.2f}"
        )

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

    scenarios = [
        ("Resting session", "resting"),
        ("Moderate activity", "moderate_activity"),
        ("High activity", "high_activity"),
        ("Activity followed by recovery", "recovery"),
        ("Poor-quality or invalid data", "poor_quality")
    ]

    for scenario_name, scenario_type in scenarios:
        # Use the instructor-supplied generator for all scenario data
        profile, observations_data = generate_fitness_data(
            participant_id="P001",
            scenario=scenario_type,
            seed=42,
            number_of_windows=12
        )

        # Convert the generated participant dictionary into our own object
        participant = Participant(
            profile["participant_id"],
            profile["baseline_heart_rate"],
            profile["baseline_temperature"],
            profile["baseline_skin_response"]
        )

        print("\n")
        print("=" * 50)
        print(scenario_name.upper())
        print("=" * 50)

        # Convert the generated observations into our own objects and analyze them
        session = create_session(participant, observations_data)
        analyzer = Analyzer(session)
        result = analyzer.analyze()

        print_report(result)


if __name__ == "__main__":
    run_scenarios()