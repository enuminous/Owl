import numpy as np
from sklearn.metrics import (
    brier_score_loss,
    log_loss,
    roc_auc_score,
    average_precision_score,
)

def future_failure_labels(failure, warning_horizon):
    failure = np.asarray(failure, dtype=int)
    y = np.zeros_like(failure)
    n = len(failure)
    for i in range(n):
        end = min(n, i + warning_horizon + 1)
        y[i] = int(failure[i+1:end].max() if i + 1 < end else 0)
    return y

def threshold_at_fpr(y_true, score, max_fpr=0.05):
    y_true = np.asarray(y_true, dtype=int)
    score = np.asarray(score, dtype=float)
    negatives = score[y_true == 0]
    if len(negatives) == 0:
        return float(np.quantile(score, 0.95))
    q = max(0.0, min(1.0, 1.0 - max_fpr))
    return float(np.quantile(negatives, q))

def lead_times(failure, alerts):
    failure = np.asarray(failure, dtype=int)
    alerts = np.asarray(alerts, dtype=int)
    failure_idx = np.where(failure == 1)[0]
    if len(failure_idx) == 0:
        return []
    leads = []
    for fi in failure_idx:
        prior = np.where(alerts[:fi] == 1)[0]
        if len(prior):
            leads.append(int(fi - prior[-1]))
    return leads

def warning_metrics(failure, future_y, score, threshold):
    score = np.clip(np.asarray(score, dtype=float), 1e-9, 1 - 1e-9)
    future_y = np.asarray(future_y, dtype=int)
    alerts = (score >= threshold).astype(int)

    negatives = future_y == 0
    positives = future_y == 1

    fpr = float(alerts[negatives].mean()) if negatives.any() else None
    sensitivity = float(alerts[positives].mean()) if positives.any() else None

    out = {
        "threshold": float(threshold),
        "false_alarm_rate": fpr,
        "sensitivity": sensitivity,
        "brier": float(brier_score_loss(future_y, score)),
        "log_loss": float(log_loss(future_y, np.c_[1-score, score], labels=[0, 1])),
    }

    if len(np.unique(future_y)) > 1:
        out["roc_auc"] = float(roc_auc_score(future_y, score))
        out["average_precision"] = float(average_precision_score(future_y, score))
    else:
        out["roc_auc"] = None
        out["average_precision"] = None

    leads = lead_times(failure, alerts)
    out["median_lead_time"] = float(np.median(leads)) if leads else None
    out["n_failures_with_prior_alert"] = len(leads)
    return out
