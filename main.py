import pandas as pd
from math import isnan
from pprint import pprint
from datetime import datetime, timedelta

# date format
date_format = "%Y/%m/%d %H:%M"
a = 0


def is_nan(item):
    try:
        if isnan(item):
            return ""
    except TypeError:
        return item
    return item


def generate_first_csv_file(raw_data_file):
    # load raw data
    raw_df = pd.read_csv(raw_data_file)

    # column name
    column_name = list(raw_df.columns)

    # record data
    data_dict_1 = {
        "Machine_name": [],
        "Status": [],
        "DTTM": [],
        "Even_type": [],
        "Remark": []
    }

    error_list = [
        "ERROR",
        "ALARM",
        "Begin Repair",
        "MACHINE",
        "State: Specific Running Continuous"
    ]

    first_started_index = int(raw_df[raw_df["status_name"] == "STARTED"].index[0])
    for i in range(len(raw_df)):
        serial, log_datetime, machine_name, event_type, status_name, error_code, error_name, stopped_reason = [raw_df[key][i] for key in column_name]

        if i == first_started_index:
            data_dict_1["Machine_name"].append(machine_name)
            data_dict_1["Status"].append(status_name)
            data_dict_1["DTTM"].append(log_datetime)
            data_dict_1["Even_type"].append("")
            data_dict_1["Remark"].append(is_nan(error_name))
        elif i > first_started_index:
            if event_type == "STATUS" and status_name == "STARTED" and isnan(stopped_reason):
                data_dict_1["Machine_name"].append(machine_name)
                data_dict_1["Status"].append("STARTED")
                data_dict_1["DTTM"].append(log_datetime)
                data_dict_1["Even_type"].append("")
                data_dict_1["Remark"].append("")
            elif event_type == "STATUS" and status_name == "FINISHED" and stopped_reason == "Auto":
                pass
            elif event_type == "STATUS" and status_name == "FINISHED" and stopped_reason == "MA":
                data_dict_1["Machine_name"].append(machine_name)
                data_dict_1["Status"].append("FINISHED")
                data_dict_1["DTTM"].append(log_datetime)
                data_dict_1["Even_type"].append(stopped_reason)
                data_dict_1["Remark"].append("")
            elif event_type == "STATUS" and status_name == "FINISHED" and stopped_reason == "Reset":
                data_dict_1["Machine_name"].append(machine_name)
                data_dict_1["Status"].append("FINISHED")
                data_dict_1["DTTM"].append(log_datetime)
                data_dict_1["Even_type"].append(stopped_reason)
                data_dict_1["Remark"].append("")
            elif event_type == "ERROR" and str(error_code).replace(".", "").isdigit():
                data_dict_1["Machine_name"].append(machine_name)
                data_dict_1["Status"].append("FINISHED")
                data_dict_1["DTTM"].append(log_datetime)
                data_dict_1["Even_type"].append(is_nan(error_code))
                data_dict_1["Remark"].append(is_nan(error_name))
            elif event_type == "ALARM" and status_name == "Begin Repair":
                data_dict_1["Machine_name"].append(machine_name)
                data_dict_1["Status"].append("ALARM")
                data_dict_1["DTTM"].append(log_datetime)
                data_dict_1["Even_type"].append(is_nan(status_name))
                data_dict_1["Remark"].append(is_nan(error_name))
            elif event_type == "MACHINE" and status_name == "State: Specific Running Continuous":
                data_dict_1["Machine_name"].append(machine_name)
                data_dict_1["Status"].append("MACHINE")
                data_dict_1["DTTM"].append(log_datetime)
                data_dict_1["Even_type"].append(is_nan(error_code))
                data_dict_1["Remark"].append(is_nan(error_name))

    result_df = pd.DataFrame(data_dict_1)

    # save result to the file
    result_df.to_csv("test.csv", index=False)


def generate_second_csv_file(first_csv_file):
    data_dict_2 = {
        "Machine": [],
        "Status": [],

    }
    df = pd.read_csv(first_csv_file)
    column_name = list(df.columns)
    for i in range(len(df)):
        machine_name, status, dttm, even_type, remark = [df[key][i] for key in column_name]

        if i > 0:




def main():
    generate_first_csv_file("raw_data.csv")
    generate_second_csv_file("test.csv")


if __name__ == "__main__":
    main()
