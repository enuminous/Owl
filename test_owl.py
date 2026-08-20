import pandas as pd
from signals import build_owl_signals
from owl import OWLExperiment

def test_signal_builder():
    df = pd.read_csv("example_data.csv")
    sig = build_owl_signals(
        df,
        ["sensor_a", "sensor_b", "sensor_c"],
        horizons=(3,7,23),
    )
    assert len(sig) == len(df)
    assert "owl_warning_score" in sig.columns
    assert sig["owl_warning_score"].between(0,1).all()

def test_experiment_runs():
    df = pd.read_csv("example_data.csv")
    exp = OWLExperiment(
        time_column="time",
        failure_column="failure",
        feature_columns=["sensor_a", "sensor_b", "sensor_c"],
        warning_horizon=20,
    )
    out = exp.run(df)
    assert "results" in out
    assert "owl" in out["results"]
    assert "zscore" in out["results"]
