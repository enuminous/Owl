import numpy as np
import pandas as pd

EPS = 1e-8

def robust_z(series, window=23):
    med = series.rolling(window, min_periods=3).median()
    mad = (series - med).abs().rolling(window, min_periods=3).median()
    return (series - med) / (1.4826 * mad + EPS)

def build_owl_signals(df, feature_columns, horizons=(3, 7, 23)):
    x = df[feature_columns].astype(float).copy()
    out = pd.DataFrame(index=df.index)

    zcols = []
    dxcols = []
    ddxcols = []

    for c in feature_columns:
        zc = f"{c}__z"
        dc = f"{c}__dx"
        ddc = f"{c}__ddx"
        out[zc] = robust_z(x[c], max(horizons))
        out[dc] = x[c].diff()
        out[ddc] = x[c].diff().diff()
        zcols.append(zc)
        dxcols.append(dc)
        ddxcols.append(ddc)

    rel_dev_cols = []
    for i, a in enumerate(feature_columns):
        for b in feature_columns[i+1:]:
            rel = x[a] - x[b]
            rel_z = robust_z(rel, max(horizons)).abs()
            name = f"rel__{a}__{b}__contradiction"
            out[name] = rel_z
            rel_dev_cols.append(name)

    # Global contradiction.
    if rel_dev_cols:
        out["contradiction"] = out[rel_dev_cols].mean(axis=1)
    else:
        out["contradiction"] = 0.0

    # Local instability.
    local_parts = []
    for c in zcols + dxcols + ddxcols:
        local_parts.append(out[c].abs())
    out["local_instability"] = pd.concat(local_parts, axis=1).mean(axis=1)

    # Persistence and multiscale deterioration.
    for h in horizons:
        out[f"contradiction_mean_{h}"] = out["contradiction"].rolling(h, min_periods=1).mean()
        out[f"instability_mean_{h}"] = out["local_instability"].rolling(h, min_periods=1).mean()
        out[f"contradiction_slope_{h}"] = (
            out["contradiction"].diff().rolling(h, min_periods=1).mean()
        )
        out[f"instability_slope_{h}"] = (
            out["local_instability"].diff().rolling(h, min_periods=1).mean()
        )

    # Equal-weight warning score. Kept interpretable on purpose.
    components = [
        out["contradiction"].clip(lower=0),
        out["local_instability"].clip(lower=0),
    ]
    for h in horizons:
        components.extend([
            out[f"contradiction_mean_{h}"].clip(lower=0),
            out[f"instability_mean_{h}"].clip(lower=0),
            out[f"contradiction_slope_{h}"].clip(lower=0),
            out[f"instability_slope_{h}"].clip(lower=0),
        ])

    stack = pd.concat(components, axis=1).replace([np.inf, -np.inf], np.nan).fillna(0.0)

    # Rank-normalize each component for robust aggregation.
    ranked = stack.rank(pct=True)
    out["owl_warning_score"] = ranked.mean(axis=1)

    return out.replace([np.inf, -np.inf], np.nan).fillna(0.0)
