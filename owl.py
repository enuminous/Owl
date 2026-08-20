from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler

from signals import build_owl_signals
from baselines import zscore_baseline, ewma_baseline, persistence_baseline
from metrics import future_failure_labels, threshold_at_fpr, warning_metrics

@dataclass
class OWLExperiment:
    time_column: str
    failure_column: str
    feature_columns: list
    warning_horizon: int = 20
    horizons: tuple = (3, 7, 23)
    max_false_alarm_rate: float = 0.05
    train_fraction: float = 0.60
    random_state: int = 23

    def run(self, df):
        df = df.sort_values(self.time_column).reset_index(drop=True).copy()
        future_y = future_failure_labels(df[self.failure_column].to_numpy(), self.warning_horizon)
        cut = max(10, int(len(df) * self.train_fraction))

        sig = build_owl_signals(df, self.feature_columns, self.horizons)
        owl_score = sig["owl_warning_score"].to_numpy()

        z = zscore_baseline(df, self.feature_columns, max(self.horizons))
        ewma = ewma_baseline(df, self.feature_columns)
        persist = persistence_baseline(df, self.feature_columns)

        # Learned temporal baseline using only raw observations + first differences.
        X = df[self.feature_columns].astype(float).copy()
        for c in self.feature_columns:
            X[f"{c}__dx"] = X[c].diff().fillna(0.0)
        scaler = RobustScaler()
        model = LogisticRegression(max_iter=3000, random_state=self.random_state)
        X_train = scaler.fit_transform(X.iloc[:cut])
        X_test = scaler.transform(X.iloc[cut:])
        y_train = future_y[:cut]
        if len(np.unique(y_train)) < 2:
            logit_score = np.full(len(df), y_train.mean() if len(y_train) else 0.0)
        else:
            model.fit(X_train, y_train)
            train_p = model.predict_proba(X_train)[:,1]
            test_p = model.predict_proba(X_test)[:,1]
            logit_score = np.concatenate([train_p, test_p])

        scores = {
            "owl": owl_score,
            "zscore": z,
            "ewma": ewma,
            "persistence": persist,
            "logistic_temporal": logit_score,
        }

        results = {}
        for name, score in scores.items():
            threshold = threshold_at_fpr(
                future_y[:cut],
                score[:cut],
                self.max_false_alarm_rate
            )
            results[name] = warning_metrics(
                df[self.failure_column].to_numpy()[cut:],
                future_y[cut:],
                score[cut:],
                threshold
            )

        return {
            "n_total": len(df),
            "train_n": cut,
            "test_n": len(df)-cut,
            "warning_horizon": self.warning_horizon,
            "max_false_alarm_rate": self.max_false_alarm_rate,
            "results": results,
            "primary_comparison": (
                "Compare sensitivity and median lead time at approximately matched "
                "false-alarm thresholds selected on the training segment."
            )
        }
