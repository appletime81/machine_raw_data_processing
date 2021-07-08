import pandas as pd
from math import isnan
from pprint import pprint
from datetime import datetime, timedelta


def is_nan(item):
    try:
        if isnan(item):
            return ""
    except TypeError:
        return item
    return item


def main():
    # load raw data
    raw_df = pd.read_csv("raw_data.csv")

    # column name
    column_name = list(raw_df.columns)

    # date format
    date_format = "%Y/%m/%d %H:%M"
    
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

    # print(type(raw_df["log_datetime"][0]))
    # print(datetime.strptime(raw_df["log_datetime"][0], date_format))

    first_started_index = int(raw_df[raw_df["status_name"] == "STARTED"].index[0])
    for i in range(len(raw_df)):
        serial, log_datetime, machine_name, event_type, status_name, error_code, error_name, stopped_reason = [raw_df[key][i] for key in column_name]
        # print(serial, log_datetime, machine_name, event_type, status_name, error_code, error_name, stopped_reason)
        if i == first_started_index:
            data_dict_1["Machine_name"].append(machine_name)
            data_dict_1["Status"].append(status_name)
            data_dict_1["DTTM"].append(log_datetime)
            data_dict_1["Even_type"].append(is_nan(event_type))
            data_dict_1["Remark"].append(is_nan(error_name))
        elif i > 0:
            if event_type == "STATUS" and status_name == "FINISHED" and stopped_reason == "Auto":
                data_dict_1["Machine_name"].append(machine_name)
                data_dict_1["Status"].append(status_name)
                data_dict_1["DTTM"].append(log_datetime)
                data_dict_1["Even_type"].append(is_nan(event_type))
                data_dict_1["Remark"].append(is_nan(error_name))
            elif event_type == "ERROR" and error_code.replace(".", "").isdigit():
                data_dict_1["Machine_name"].append(machine_name)
                data_dict_1["Status"].append("FINISHED")
                data_dict_1["DTTM"].append(log_datetime)
                data_dict_1["Even_type"].append(is_nan(error_code))
                data_dict_1["Remark"].append(is_nan(error_name))
            elif event_type == "STATUS" and status_name == "FINISHED" and raw_df["event_type"][i-1] == "ERROR":
                pass  # doing nothing
            elif event_type == "ALARM" and status_name == "Begin Repair":
                data_dict_1["Machine_name"].append(machine_name)
                data_dict_1["Status"].append("ALARM")
                data_dict_1["DTTM"].append(log_datetime)
                data_dict_1["Even_type"].append(is_nan(error_code))
                data_dict_1["Remark"].append(is_nan(error_name))
            # TODO: event_type為MACHINE的判斷式
            # elif

    # pprint(data_dict_1)


if __name__ == "__main__":
    main()
    # a = "2"
    # print(a.isdigit())
