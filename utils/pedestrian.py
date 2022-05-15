import pandas as pd


def load_and_clean_pedestrian_data(path):
    df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(
        {
            "day": df["Mdate"],
            "year": df["Year"],
            "hour": df["Time"],
            "month": pd.to_datetime(df["Month"], format='%B').dt.month
        }
    )
    return df


def load_and_clean_pedestrian_data(counts_csv_path, sensor_csv_path=None):
    df = pd.read_csv(counts_csv_path).set_index("ID")
    # Date_Time field previously had incorrect time so needed to reconstruct it.
    # TODO: switch to loading as datetime by providing a parsing template
    df["Date_Time"] = pd.to_datetime(
        {
            "day": df["Mdate"],
            "year": df["Year"],
            "hour": df["Time"],
            "month": pd.to_datetime(df["Month"], format="%B").dt.month,
        }
    )
    df["datetime_flat_year"] = pd.to_datetime(
        {
            "day": df["Mdate"],
            "year": 2000,
            "hour": df["Time"],
            "month": pd.to_datetime(df["Month"], format="%B").dt.month,
        }
    )
    if sensor_csv_path is not None:
        geo_df = pd.read_csv(
            sensor_csv_path, usecols=["sensor_id", "latitude", "longitude"]
        )
        df = df.merge(geo_df, left_on="Sensor_ID", right_on="sensor_id")
    df = df.sort_values("Date_Time")
    return df
