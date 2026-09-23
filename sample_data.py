# Reference data for the participant used in the sample scenarios
participant_data = {
    "name": "Alex",
    "resting_heart_rate": 65,
    "reference_temperature": 33.0,
    "reference_skin_response": 2.0
}


# Scenario 1: Resting session
resting_data = [
    {
        "timestamp": 1,
        "heart_rate": 70,
        "skin_response": 2.0,
        "temperature": 33.0,
        "activity_level": 0.10,
        "signal_quality": 0.95
    },
    {
        "timestamp": 2,
        "heart_rate": 72,
        "skin_response": 2.1,
        "temperature": 33.1,
        "activity_level": 0.12,
        "signal_quality": 0.94
    },
    {
        "timestamp": 3,
        "heart_rate": 68,
        "skin_response": 1.9,
        "temperature": 32.9,
        "activity_level": 0.08,
        "signal_quality": 0.96
    }
]


# Scenario 2: Moderate activity
moderate_data = [
    {
        "timestamp": 1,
        "heart_rate": 95,
        "skin_response": 2.4,
        "temperature": 33.2,
        "activity_level": 0.40,
        "signal_quality": 0.95
    },
    {
        "timestamp": 2,
        "heart_rate": 105,
        "skin_response": 2.6,
        "temperature": 33.4,
        "activity_level": 0.50,
        "signal_quality": 0.94
    },
    {
        "timestamp": 3,
        "heart_rate": 110,
        "skin_response": 2.7,
        "temperature": 33.5,
        "activity_level": 0.55,
        "signal_quality": 0.96
    }
]


# Scenario 3: High activity
high_activity_data = [
    {
        "timestamp": 1,
        "heart_rate": 130,
        "skin_response": 3.0,
        "temperature": 33.8,
        "activity_level": 0.75,
        "signal_quality": 0.95
    },
    {
        "timestamp": 2,
        "heart_rate": 145,
        "skin_response": 3.3,
        "temperature": 34.0,
        "activity_level": 0.85,
        "signal_quality": 0.94
    },
    {
        "timestamp": 3,
        "heart_rate": 150,
        "skin_response": 3.5,
        "temperature": 34.2,
        "activity_level": 0.90,
        "signal_quality": 0.96
    }
]


# Scenario 4: Activity followed by recovery
recovery_data = [
    {
        "timestamp": 1,
        "heart_rate": 120,
        "skin_response": 2.8,
        "temperature": 33.5,
        "activity_level": 0.65,
        "signal_quality": 0.95
    },
    {
        "timestamp": 2,
        "heart_rate": 150,
        "skin_response": 3.5,
        "temperature": 34.0,
        "activity_level": 0.90,
        "signal_quality": 0.96
    },
    {
        "timestamp": 3,
        "heart_rate": 130,
        "skin_response": 3.0,
        "temperature": 33.8,
        "activity_level": 0.60,
        "signal_quality": 0.95
    },
    {
        "timestamp": 4,
        "heart_rate": 95,
        "skin_response": 2.4,
        "temperature": 33.4,
        "activity_level": 0.25,
        "signal_quality": 0.94
    }
]


# Scenario 5: Poor-quality and invalid sensor data
invalid_data = [
    {
        "timestamp": 1,
        "heart_rate": 300,
        "skin_response": 2.1,
        "temperature": 33.1,
        "activity_level": 0.65,
        "signal_quality": 0.90
    },
    {
        "timestamp": 2,
        "heart_rate": 100,
        "skin_response": 2.3,
        "temperature": 33.0,
        "activity_level": 0.50,
        "signal_quality": 0.20
    },
    {
        "timestamp": 3,
        "heart_rate": -10,
        "skin_response": 2.0,
        "temperature": 33.2,
        "activity_level": 0.40,
        "signal_quality": 0.95
    },
    {
        "timestamp": 4,
        "heart_rate": None,
        "skin_response": 2.2,
        "temperature": 33.0,
        "activity_level": 0.45,
        "signal_quality": 0.95
    }
]