import pandas as pd
from math import isnan
from datetime import datetime, timedelta
from pprint import pprint

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


def is_nan_with_str(item):
    try:
        return isnan(item)
    except:
        return False


def time_delta(time1, time2):
    time1 = datetime.strptime(time1, date_format)
    time2 = datetime.strptime(time2, date_format)
    delta = time2 - time1
    delta_str = str(int(str(delta)[2:4]))
    return delta_str + " min"


def get_machine_name(csv_file):
    df = pd.read_csv(csv_file)
    machine_name = []
    for i in range(len(df)):
        machine_name.append(df["machine_name"][i])
    machine_name = list(set(machine_name))
    print(machine_name)
    return machine_name


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
    result_df.to_csv("result1.csv", index=False)


def generate_second_csv_file(first_csv_file, raw_data_file):
    def policy(csv_file, df):
        data_dict_2 = {"Machine": [], "Status": [], "Run": []}
        column_name = list(pd.read_csv(csv_file).columns)

        for i in range(len(df)):
            machine_name, status, dttm, even_type, remark = [df[key][i] for key in column_name]
            if i > 0:
                if status == "FINISHED" and df["Status"][i-1] == "STARTED" and str(even_type).replace(".", "").isdigit():
                    data_dict_2["Machine"].append(machine_name)
                    data_dict_2["Status"].append("Run")
                    data_dict_2["Run"].append(time_delta(df["DTTM"][i-1], dttm))
                elif status == "FINISHED" and df["Status"][i-1] == "STARTED" and is_nan_with_str(even_type):
                    data_dict_2["Machine"].append(machine_name)
                    data_dict_2["Status"].append("Run")
                    data_dict_2["Run"].append(time_delta(df["DTTM"][i-1], dttm))
                elif status == "FINISHED" and df["Status"][i - 1] == "STARTED" and isinstance(even_type, str):
                    data_dict_2["Machine"].append(machine_name)
                    data_dict_2["Status"].append("Run")
                    data_dict_2["Run"].append(time_delta(df["DTTM"][i-1], dttm))

                    data_dict_2["Machine"].append(machine_name)
                    data_dict_2["Status"].append("Stop")
                    data_dict_2["Run"].append(time_delta(dttm, df["DTTM"][i+1]))
                elif status == "ALARM" and df["Status"][i-1] == "FINISHED":
                    data_dict_2["Machine"].append(machine_name)
                    data_dict_2["Status"].append("Stop")
                    data_dict_2["Run"].append(time_delta(df["DTTM"][i-1], dttm))
        result_df = pd.DataFrame(data_dict_2)
        last_item_index = len(result_df) - 1
        if result_df["Status"][last_item_index] == "Stop" and result_df["Run"][last_item_index] == "0 min":
            result_df["Machine"][last_item_index] = ""
            result_df["Status"][last_item_index] = ""
            result_df["Run"][last_item_index] = ""
        return result_df

    # get machine name
    machine_names = get_machine_name(raw_data_file)
    raw_data_df = pd.read_csv(raw_data_file)
    raw_data_list = []
    for machine_name in machine_names:
        new_df = raw_data_df[raw_data_df["machine_name"] == machine_name]
        raw_data_list.append(new_df)

    for df in raw_data_list:
        result =




def main():
    # generate_first_csv_file("raw_data.csv")
    generate_second_csv_file("result1.csv", "raw_data2.csv")
    # get_machine_name("raw_data2.csv")


if __name__ == "__main__":
    main()
