# Smart Fitness Session Analyzer

## Python Programming Assignment I - Option A

**Student:** Victoria Ludvigsen  
**Student number:** 421969

## Project description

This project implements Option A: Smart Fitness Session Analyzer.

The program uses the instructor-supplied fitness data generator to create simulated participant profiles and sensor observations. The generated dictionaries are converted into custom Python objects, validated, analyzed, and classified as:

- resting
- moderate activity
- high activity
- recovering
- insufficient data

The analysis is returned as a structured dictionary and displayed as a readable console report.

## Project structure

```text
ACIT4420_Assignment1/
├── option_a_fitness/
│   ├── DATA_DESCRIPTION.md
│   ├── data_generator.py
│   └── example_usage.py
├── .gitignore
├── README.md
├── main.py
├── requirements.txt
└── tests.py
```

`main.py` contains the application logic.  
`tests.py` tests the five documented scenarios.  
`option_a_fitness` contains the instructor-supplied starter files. `data_generator.py` has not been modified.

## Class design

### Participant

Stores the participant ID and personal reference values for heart rate, temperature, and skin response.

### Observation

Represents one sensor observation containing timestamp, heart rate, skin response, temperature, activity level, and signal quality. It also validates whether the observation is usable.

### Session

Contains a `Participant` object and a list of `Observation` objects.

### Analyzer

Analyzes usable observations, calculates summaries, compares measurements with reference values, detects recovery, classifies the session, and returns the result as a dictionary.

## Object-oriented design

### Composition

`Session` uses composition because it contains a `Participant` object and multiple `Observation` objects.

### Encapsulation

The participant's resting heart rate is stored in the protected-style attribute `_resting_heart_rate` and controlled through a property and setter.

### Inheritance

Inheritance and method overriding are not used because the classes represent separate responsibilities rather than specialized versions of the same type. Composition gives a clearer design for this application.

### Static methods

`Observation` uses `is_valid_heart_rate()` and `is_valid_ratio()` as static methods because these checks do not depend on a specific object.

## Data and validation

The program imports the instructor-supplied generator:

```python
from option_a_fitness.data_generator import generate_fitness_data
```

It uses the five documented scenarios:

- `resting`
- `moderate_activity`
- `high_activity`
- `recovery`
- `poor_quality`

A fixed seed of `42` is used so the example data and tests are reproducible.

An observation is usable when:

- timestamp is zero or greater
- heart rate is between 35 and 205 bpm
- skin response is zero or greater
- temperature is between 25 and 42 degrees Celsius
- activity level is between 0 and 1
- signal quality is between 0 and 1 and at least 0.5

The ranges follow the supplied data description. The minimum signal quality of `0.5` is a project assumption.

The poor-quality scenario contains missing, impossible, or low-quality values that are rejected by the validation logic.

## Analysis and classification

For usable observations, the program calculates average, minimum, and maximum values for heart rate, activity level, temperature, and skin response.

Average heart rate, temperature, and skin response are also compared with the participant's reference values.

Classification rules:

- **Insufficient data:** fewer than three usable observations.
- **Resting:** average activity is below `0.25` and average heart rate is no more than `20 bpm` above resting heart rate.
- **High activity:** average activity is at least `0.70` or average heart rate is at least `60 bpm` above resting heart rate.
- **Moderate activity:** the session does not meet the other activity conditions.
- **Recovering:** the first three and final three usable observations are compared. Heart rate and activity must show a clear decline toward resting values.

Recovery detection requires at least six usable observations. The exact classification thresholds are project assumptions.

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
Poor-quality data test passed.

All tests passed.
```

## Example output

```text
FITNESS SESSION REPORT
----------------------
Participant: P001
Usable observations: 12/12
Classification: recovering
Explanation: Heart rate and activity declined from higher activity toward resting values.

Heart rate:
  Average: 112.83 bpm
  Minimum: 86 bpm
  Maximum: 141 bpm
```

## Known limitations

- The program uses simulated sensor data from the supplied generator.
- Validation and classification depend on defined numerical thresholds.
- Recovery detection compares the beginning and end of the session rather than the complete trend.
- The example scenarios use a fixed seed for reproducibility.
- The application does not use external APIs, databases, graphical interfaces, or machine-learning models.
