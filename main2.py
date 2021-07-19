import pandas as pd
from datetime import datetime
from math import isnan
from pprint import pprint


def get_machine_name(raw_data_file):
    orig_data = pd.read_csv(raw_data_file)
    machine_names = list(orig_data.groupby(["machine_name"]).groups.keys())
    return machine_names


def get_dataframe(raw_data, machine_name):
    return raw_data[raw_data["machine_name"] == machine_name].reset_index(drop=True)


def policy(df):
    # variables
    col_names = df.columns
    res = {
        "Machine": [], "Status": [], "Start_DTTM": [], "Stop_DTTM": [], "Duration": [],
        "error_code": [], "error_name": [], "stopped_reason": []
    }

    for i in range(len(df)):
        serial, log_datetime, machine_name, event_type, status_name, error_code, error_name, stopped_reason = \
            [df[key][i] for key in col_names]
        # print(serial, log_datetime, machine_name, event_type, status_name, error_code, error_name, stopped_reason)

        # start processing
        if i > 0:
            pass


if __name__ == "__main__":
    raw_data_csv_file = "raw_data.csv"
    machine_names = get_machine_name(raw_data_csv_file)
    pprint(machine_names)

    df_by_machine = get_dataframe(
        pd.read_csv(raw_data_csv_file),
        machine_names[1]
    )

    pprint(df_by_machine)


