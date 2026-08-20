import json
import pandas as pd
from owl import OWLExperiment

df = pd.read_csv("example_data.csv")

exp = OWLExperiment(
    time_column="time",
    failure_column="failure",
    feature_columns=["sensor_a", "sensor_b", "sensor_c"],
    warning_horizon=20,
    horizons=(3, 7, 23),
    max_false_alarm_rate=0.05,
    random_state=23,
)

result = exp.run(df)
print(json.dumps(result, indent=2))
