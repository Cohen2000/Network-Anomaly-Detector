# Network Anomaly Detector

A Python experiment in detecting unusual network activity from upload/download rates and user idle time. It covers data collection, controlled anomaly injection, model comparison and a live detector.

## What it demonstrates

- Feature collection with psutil and activity tracking with pynput.
- Comparison of logistic regression, random forest, histogram-based outlier scoring (HBOS) and K-means distance scoring.
- Evaluation with precision, recall, F1 and confusion matrices; a saved random-forest model for live inference.

## Start here

- [Analysis notebook](02_analysis.ipynb): experiments, plots and model comparison.
- [Monitor](01_monitor.py), [injector](02_injector.py) and [live detector](03_detector.py): the collection-to-inference workflow.
- [Example data](data/) and [saved model](models/).

## Running locally

Install the packages in `requirements.txt` in a Python virtual environment. Open the notebook for analysis, or run `python 03_detector.py` from the repository root to use the saved model. The live scripts need desktop input monitoring and access to network counters; permissions depend on the operating system. Use the injector only in an authorised test environment.

This is an experimental detector based on a small set of traffic/activity features, not a production intrusion-detection system.
