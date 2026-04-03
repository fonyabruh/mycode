from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def count_clicks(cell: str) -> int:
    """
    Считает количество действий click в ячейке action.
    Пример: "search, click, search" -> 1
    """
    if pd.isna(cell):
        return 0
    parts = [part.strip().lower() for part in str(cell).split(",")]
    return sum(part == "click" for part in parts)


def solve_actions(csv_path: str | Path = "actions.csv") -> dict:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Не найден файл {csv_path}. Положи actions.csv рядом со скриптом."
        )

    df = pd.read_csv(csv_path)
    required_columns = {"ip", "date", "action"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"В actions.csv не хватает колонок: {sorted(missing)}")

    # Парсим дату в формате %d.%m.%Y
    df["date_dt"] = pd.to_datetime(df["date"], format="%d.%m.%Y", errors="raise")

    # Задача 19: дата с максимальным числом активных пользователей
    daily_users = (
        df.groupby("date", as_index=False)["ip"]
        .nunique()
        .rename(columns={"ip": "unique_users"})
    )

    max_users = daily_users["unique_users"].max()
    best_dates = daily_users.loc[daily_users["unique_users"] == max_users, "date"]
    best_date = best_dates.iloc[0]

    # Задачи 20-21: март 2023
    march_mask = (df["date_dt"].dt.year == 2023) & (df["date_dt"].dt.month == 3)
    march_df = df.loc[march_mask].copy()

    march_unique_users = march_df["ip"].nunique()
    march_clicks = march_df["action"].apply(count_clicks).sum()

    # График по числу активных пользователей
    plot_df = daily_users.copy()
    plot_df["date_dt"] = pd.to_datetime(plot_df["date"], format="%d.%m.%Y", errors="raise")
    plot_df = plot_df.sort_values("date_dt")

    plt.figure(figsize=(12, 5))
    plt.plot(plot_df["date_dt"], plot_df["unique_users"], marker="o")
    plt.title("Число активных пользователей по датам")
    plt.xlabel("Дата")
    plt.ylabel("Уникальные пользователи")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("analysis_daily_users.png", dpi=150)
    plt.close()

    return {
        "task_19_best_date": best_date,
        "task_20_march_2023_unique_users": int(march_unique_users),
        "task_21_march_2023_clicks": int(march_clicks),
    }


if __name__ == "__main__":
    answers = solve_actions("actions.csv")
    print("Задача 19:", answers["task_19_best_date"])
    print("Задача 20:", answers["task_20_march_2023_unique_users"])
    print("Задача 21:", answers["task_21_march_2023_clicks"])
    print("График сохранён в analysis_daily_users.png")
