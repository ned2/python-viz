import pandas as pd


def clean_and_load_jobs_data(path):
    jobs_raw_df = pd.read_excel(
        path,
        sheet_name=1,  # zero-indexed, so this is the second sheet!
        usecols="A:BO",
        skiprows=5,
        skipfooter=2,
    )

    # get a DataFrame of all columns except the first two
    date_cols_df = jobs_raw_df.iloc[:, 2:]

    # split col 1 into codes and names
    ste_cols_df = (
        jobs_raw_df[jobs_raw_df.columns[0]]
        .str.split(r"\. ", expand=True)
        .rename(columns={0: "STE_CODE16", 1: "STE_NAME16"})
    )

    # split col 2 into codes and names
    sa4_cols_df = (
        jobs_raw_df[jobs_raw_df.columns[1]]
        .str.split(r"\. ", expand=True)
        .rename(columns={0: "SA4_CODE16", 1: "SA4_NAME16"})
    )

    # combine the 3 sets of columns into a single DataFrame, and then use the melt method
    # to convert it into long format
    jobs_df = pd.concat([ste_cols_df, sa4_cols_df, date_cols_df], axis=1).melt(
        id_vars=["STE_CODE16", "STE_NAME16", "SA4_CODE16", "SA4_NAME16"],
        var_name="Date",
        value_name="Index",
    )

    return jobs_df
