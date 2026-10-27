# OWL

<!-- ENUMINOUS-UNIFIED-NAV:START -->
## Repository navigation

**eNuminous network:** [All public repositories](https://github.com/enuminous/EFMW/blob/main/REPOSITORY_NAVIGATION.md) · [EFMW](https://github.com/enuminous/EFMW) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [Frozen Lean](https://github.com/enuminous/Monolithic-102-Zoo-Lean4) · [Zoo](https://github.com/enuminous/Tortoise) · [Papers](https://github.com/enuminous/papers) · [Quantum geometry](https://github.com/enuminous/Base888-Quantum-Geometry)

**This project:** [Repository home](https://github.com/enuminous/Owl) · [Subject index](https://github.com/enuminous/EFMW/blob/main/REPOSITORY_NAVIGATION.md#zoo-index-and-agents)

<details open>
<summary><strong>On this page</strong></summary>

- [Intended uses](#intended-uses)
- [Core question](#core-question)
- [Flat-stack repository](#flat-stack-repository)
- [OWL signal stack](#owl-signal-stack)
- [Installation](#installation)
- [Run example](#run-example)
- [Run tests](#run-tests)
- [Minimal usage](#minimal-usage)
- [Primary evaluation](#primary-evaluation)
- [Baselines](#baselines)
- [Freeze rule](#freeze-rule)
- [Negative results](#negative-results)
- [Status](#status)


</details>

**Related repositories:** [Tortoise](https://github.com/enuminous/Tortoise) · [Monolithic-Zoo-Lean4](https://github.com/enuminous/Monolithic-Zoo-Lean4) · [Monolithic-102-Zoo-Lean4](https://github.com/enuminous/Monolithic-102-Zoo-Lean4) · [Octopus](https://github.com/enuminous/Octopus) · [Gecko](https://github.com/enuminous/Gecko) · [Zoo-Monster](https://github.com/enuminous/Zoo-Monster)

> **Evidence boundary:** A link between projects is navigation, not an assertion of proven equivalence, experimental validation, or shared authorship. See each repository’s own status and review notes.
<!-- ENUMINOUS-UNIFIED-NAV:END -->


**Observational Warning Layer**

OWL is a minimal EFMW-derived early-warning framework for sequential systems.

Its purpose is narrow:

> Detect whether a system is moving toward a predefined failure state before a conventional alarm would fire.

OWL does not attempt to diagnose everything about a system. It produces a warning score from observable state, temporal change, cross-variable contradiction, persistence, and multiscale deterioration.

## Intended uses

- machinery and predictive maintenance
- control systems
- robotics
- AI-agent reliability
- logistics
- network operations
- industrial telemetry
- organizational operations
- other sequential systems with objectively resolvable failures

## Core question

At a matched false-alarm rate:

> Does OWL provide more warning lead time than conventional monitoring?

## Flat-stack repository

Every file lives at repository root.

```text
README.md
LICENSE
CITATION.cff
pyproject.toml
requirements.txt
owl.py
signals.py
baselines.py
metrics.py
freeze.py
alert_schema.json
example_config.yaml
example_data.csv
example_run.py
test_owl.py
MANIFEST.sha256
```

## OWL signal stack

```text
observation
→ robust normalization
→ first/second change
→ pairwise relational deviation
→ contradiction
→ persistence
→ multiscale aggregation
→ warning score
→ calibrated alert probability
```

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run example

```bash
python example_run.py
```

## Run tests

```bash
pytest -q
```

## Minimal usage

```python
import pandas as pd
from owl import OWLExperiment

df = pd.read_csv("example_data.csv")

exp = OWLExperiment(
    time_column="time",
    failure_column="failure",
    feature_columns=["sensor_a", "sensor_b", "sensor_c"],
    warning_horizon=20,
    horizons=(3, 7, 23),
    random_state=23,
)

result = exp.run(df)
print(result)
```

## Primary evaluation

OWL is scored on:

- sensitivity to future failure
- false-alarm rate
- median warning lead time
- Brier score
- log loss
- AUROC / average precision

The central comparison is not "did OWL ever fire early?"

It is:

> At the same false-alarm rate, did OWL warn earlier and more reliably than the baselines?

## Baselines

Included:

- simple z-score alarm
- EWMA-style deviation score
- persistence baseline
- logistic temporal baseline

## Freeze rule

Before prospective testing, freeze:

- features
- horizons
- failure definition
- warning window
- score weights
- alert threshold selection rule
- baselines
- false-alarm budget
- metrics
- exclusions
- source code and config

Then hash the package with:

```bash
python freeze.py
```

Do not revise the frozen machine after observing outcomes. Create OWL-M2 instead.

## Negative results

If conventional monitoring provides equal or better warning at matched false-alarm rates, OWL has not demonstrated incremental utility.

That is a valid result.

## Status

Research software. Experimental. Not validated for medical, safety-critical, financial, or autonomous deployment.
