# Smart Fitness Session Analyzer

## Python Programming Assignment I - Option A

**Student:** Victoria Ludvigsen  
**Student number:** 421969

## Project description

This project implements Option A: Smart Fitness Session Analyzer.

The program analyzes simulated fitness sensor data. It validates observations, excludes unusable measurements, calculates summaries, compares session values with a participant's reference values, and classifies the session as:

- resting
- moderate activity
- high activity
- recovering
- insufficient data

The result is returned as a dictionary and displayed as a readable console report.

## Project structure

```text
ACIT4420_Assignment1/
├── README.md
├── main.py
├── sample_data.py
├── tests.py
└── requirements.txt
```

`main.py` contains the application logic, `sample_data.py` contains the sample scenarios, and `tests.py` tests the expected results.

## Class design

### Participant

Represents the participant and stores the name, resting heart rate, reference temperature, and reference skin response.

### Observation

Represents one sensor observation containing timestamp, heart rate, skin response, temperature, activity level, and signal quality. It also checks whether the observation is usable.

### Session

Represents one fitness session and contains a participant and a list of observations.

### Analyzer

Analyzes the usable observations, calculates summaries, compares values with reference measurements, detects recovery, classifies the session, and returns the result as a dictionary.

## Object-oriented design

### Composition

`Session` uses composition because it contains a `Participant` object and multiple `Observation` objects.

### Encapsulation

The participant's resting heart rate is stored in the protected-style attribute `_resting_heart_rate` and controlled through a property and setter.

### Inheritance

Inheritance and method overriding are not used. The classes represent separate responsibilities rather than specialized versions of the same type. Composition therefore gives a clearer design for this application.

### Static methods

`Observation` uses the static methods `is_valid_heart_rate()` and `is_valid_ratio()` because these checks do not depend on a specific observation object.

## Validation and assumptions

The assignment does not provide exact numerical limits, so the following values are project assumptions.

An observation is usable when:

- timestamp is zero or greater
- heart rate is between 30 and 220 bpm
- skin response is zero or greater
- temperature is between 20 and 45
- activity level is between 0 and 1
- signal quality is between 0 and 1 and at least 0.5

The sample data includes missing, impossible, and poor-quality values such as `None`, heart rates of `300` and `-10`, and signal quality of `0.20`.

## Classification rules

At least three usable observations are required for a normal classification.

- **Insufficient data:** fewer than three usable observations.
- **Resting:** average activity is below `0.25` and average heart rate is no more than `20 bpm` above resting heart rate.
- **High activity:** average activity is at least `0.70` or average heart rate is at least `60 bpm` above resting heart rate.
- **Moderate activity:** the session does not meet the other activity conditions.
- **Recovering:** heart rate and activity both decrease across the final three usable observations after clear activity. Recovery detection requires at least four usable observations.

The program also compares average heart rate, temperature, and skin response with the participant's reference values.

## Sample scenarios

The project includes five scenarios:

1. Resting session
2. Moderate activity
3. High activity
4. Activity followed by recovery
5. Missing, poor-quality, or invalid sensor data

## Running the program

The project uses only the Python standard library.

Clone the repository:

```bash
git clone https://github.com/victorialudvigsen/ACIT4420_Assignment1.git
```

Move into the project folder:

```bash
cd ACIT4420_Assignment1
```

Run:

```bash
python main.py
```

If the system uses `python3`:

```bash
python3 main.py
```

## Running the tests

```bash
python tests.py
```

Expected result:

```text
Resting session test passed.
Moderate activity test passed.
High activity test passed.
Recovery test passed.
Invalid data test passed.

All tests passed.
```

## Example output

```text
FITNESS SESSION REPORT
----------------------
Participant: Alex
Usable observations: 4/4
Classification: recovering
Explanation: Heart rate and activity declined near the end after a period of clear activity.

Heart rate:
  Average: 123.75 bpm
  Minimum: 95 bpm
  Maximum: 150 bpm

Activity level:
  Average: 0.60

Temperature:
  Average: 33.67

Skin response:
  Average: 2.93
```

## Known limitations

- The program uses simulated sensor data.
- Validation limits and classification thresholds are project assumptions.
- Recovery detection only examines the final three usable observations.
- The application does not use external APIs, databases, graphical interfaces, or machine-learning models.
