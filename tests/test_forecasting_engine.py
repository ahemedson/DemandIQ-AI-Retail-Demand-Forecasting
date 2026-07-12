from pathlib import Path

import pandas as pd

from models.forecasting_engine import ForecastingEngine


def main():

    # --------------------------------------------------
    # Load Dataset
    # --------------------------------------------------

    data_path = Path("data") / "train.csv"   # Change if your filename differs

    print("=" * 60)
    print("Loading dataset...")
    print("=" * 60)

    df = pd.read_csv(
        data_path,
        parse_dates=["Date"],
        dtype={"StateHoliday": str},
        low_memory=False
    )

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    # Standardize column names
    df.columns = df.columns.str.lower()

    print("\nDataset loaded successfully.\n")

    # --------------------------------------------------
    # Forecasting Engine
    # --------------------------------------------------

    engine = ForecastingEngine(df)

    print("=" * 60)
    print("Training models...")
    print("=" * 60)

    engine.train_models()

    print("Training completed.\n")

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    print("=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    print(engine.evaluation_results())

    print("\n")

    print("=" * 60)
    print("BEST MODEL")
    print("=" * 60)

    print(engine.best_model())


if __name__ == "__main__":
    main()