import pandas as pd

def detect_anomalies(data: pd.Series, z_thresh: float = 3.0):
    """
    Simple anomaly detection using Z-score.
    Args:
        data (pd.Series): Series of water usage values
        z_thresh (float): threshold for anomaly detection
    Returns:
        pd.Series: points detected as anomalies
    """
    mean = data.mean()
    std = data.std()
    z_scores = (data - mean) / std
    return data[abs(z_scores) > z_thresh]

if __name__ == "__main__":
    # Example usage with dummy data
    readings = pd.Series([100, 105, 98, 500, 102, 97, 103])
    anomalies = detect_anomalies(readings, z_thresh=2.0)

    print("Anomalies detected:\n", anomalies)
