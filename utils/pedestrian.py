import calendar

import pandas as pd


def load_and_clean_pedestrian_data(counts_csv_path, sensor_csv_path=None):
    """Clean data from Melbourne city council pedestrian sensor system."""
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


def sort_months(months):
    """Sort a sequence of months by their calendar order"""
    month_ref = list(calendar.month_name)[1:]
    return sorted(months, key=lambda month: month_ref.index(month))


def get_column_values(df, col_name):
    """Get sorted unique values from DataFrame for year, month, or sensor name"""
    column = df[col_name]
    if col_name in ("Year", "Sensor_Name"):
        return sorted(column.unique())
    elif col_name == "Month":
        return sort_months(column)
    else:
        raise Exception(f"unsupported column {col_name}")


        
        
