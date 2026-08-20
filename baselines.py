import numpy as np
import pandas as pd

EPS = 1e-8

def zscore_baseline(df, feature_columns, window=23):
    x = df[feature_columns].astype(float)
    scores = []
    for c in feature_columns:
        med = x[c].rolling(window, min_periods=3).median()
        mad = (x[c] - med).abs().rolling(window, min_periods=3).median()
        z = ((x[c] - med) / (1.4826 * mad + EPS)).abs()
        scores.append(z)
    raw = pd.concat(scores, axis=1).mean(axis=1).fillna(0.0)
    return raw.rank(pct=True).to_numpy()

def ewma_baseline(df, feature_columns, alpha=0.2):
    x = df[feature_columns].astype(float)
    scores = []
    for c in feature_columns:
        mu = x[c].ewm(alpha=alpha, adjust=False).mean()
        dev = (x[c] - mu).abs()
        scores.append(dev)
    raw = pd.concat(scores, axis=1).mean(axis=1).fillna(0.0)
    return raw.rank(pct=True).to_numpy()

def persistence_baseline(df, feature_columns, window=7):
    x = df[feature_columns].astype(float)
    delta = x.diff().abs().mean(axis=1)
    raw = delta.rolling(window, min_periods=1).mean().fillna(0.0)
    return raw.rank(pct=True).to_numpy()
