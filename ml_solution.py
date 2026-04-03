from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score


W0 = 1.0
W1 = 7.0
W2 = 7.0
DEFAULT_P = 0.5


def sigmoid(z: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-z))


def predict_proba(x1, x2, w0=W0, w1=W1, w2=W2):
    z = w0 + w1 * x1 + w2 * x2
    return sigmoid(z)


def predict_label(proba, threshold=DEFAULT_P):
    return np.where(np.asarray(proba) >= threshold, 1, -1)


def solve_manual_part():
    x1 = -0.2
    x2 = 0.3
    proba = float(predict_proba(x1, x2))
    label = int(predict_label(proba, DEFAULT_P))
    return {
        "z": W0 + W1 * x1 + W2 * x2,
        "sigma": proba,
        "sigma_rounded_2": round(proba, 2),
        "predicted_label": label,
    }


def solve_validation(csv_path: str | Path = "validation_set.csv") -> dict:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Не найден файл {csv_path}. Положи validation_set.csv рядом со скриптом."
        )

    df = pd.read_csv(csv_path)
    required_columns = {"x1", "x2", "y"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"В validation_set.csv не хватает колонок: {sorted(missing)}")

    df["proba"] = predict_proba(df["x1"], df["x2"])
    df["pred_default"] = predict_label(df["proba"], DEFAULT_P)

    accuracy_default = accuracy_score(df["y"], df["pred_default"])

    thresholds = np.linspace(0, 1, 1001)
    accuracies = []

    for threshold in thresholds:
        pred = predict_label(df["proba"], threshold)
        acc = accuracy_score(df["y"], pred)
        accuracies.append(acc)

    accuracies = np.array(accuracies)
    best_idx = int(np.argmax(accuracies))
    best_threshold = float(thresholds[best_idx])
    best_accuracy = float(accuracies[best_idx])

    # График accuracy от порога
    plt.figure(figsize=(10, 5))
    plt.plot(thresholds, accuracies)
    plt.axvline(DEFAULT_P, linestyle="--", label="p = 0.5")
    plt.axvline(best_threshold, linestyle="--", label=f"best p = {best_threshold:.2f}")
    plt.title("Зависимость accuracy от порога p")
    plt.xlabel("Порог p")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig("ml_accuracy_vs_threshold.png", dpi=150)
    plt.close()

    return {
        "accuracy_at_p_05": round(float(accuracy_default), 2),
        "best_threshold_p": round(best_threshold, 2),
        "best_accuracy": round(best_accuracy, 4),
    }


if __name__ == "__main__":
    manual = solve_manual_part()
    print("Задача 22: sigma =", manual["sigma_rounded_2"])
    print("Задача 23: y_hat =", manual["predicted_label"])

    try:
        validation = solve_validation("validation_set.csv")
        print("Задача 24: accuracy при p=0.5 =", validation["accuracy_at_p_05"])
        print("Задача 25: лучший p =", validation["best_threshold_p"])
        print("Лучшая accuracy =", validation["best_accuracy"])
        print("График сохранён в ml_accuracy_vs_threshold.png")
    except FileNotFoundError as e:
        print(e)
