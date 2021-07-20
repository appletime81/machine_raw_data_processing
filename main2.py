import pandas as pd
from datetime import datetime
time_format = "%Y/%m/%d %H:%M"


def get_machine_name(raw_data_file):
    orig_data = pd.read_csv(raw_data_file)
    machine_names = list(orig_data.groupby(["machine_name"]).groups.keys())
    return machine_names


def get_dataframe(raw_data, machine_name):
    return raw_data[raw_data["machine_name"] == machine_name].reset_index(drop=True)


def cal_time_delta(time1, time2):
    time1 = datetime.strptime(time1, time_format)
    time2 = datetime.strptime(time2, time_format)
    return str(time2 - time1).split(":")[1]


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
            if status_name == "ERROR" and df["status_name"][i - 1] == "STARTED":
                res["Machine"].append(machine_name)
                res["Status"].append("Run")
                res["Start_DTTM"].append(df["log_datetime"][i - 1])
                res["Stop_DTTM"].append(df["log_datetime"][i + 1])
                res["Duration"].append(cal_time_delta(df["log_datetime"][i - 1], df["log_datetime"][i + 1]))
                res["error_code"].append("NA")
                res["error_name"].append("NA")
                res["stopped_reason"].append("NA")
            elif status_name == "FINISHED" and df["status_name"][i - 1] == "ERROR":
                try:
                    res["Machine"].append(machine_name)
                    res["Status"].append("Stop")
                    res["Start_DTTM"].append(log_datetime)
                    res["Stop_DTTM"].append(df["log_datetime"][i + 2])
                    res["Duration"].append(cal_time_delta(log_datetime, df["log_datetime"][i + 2]))
                    res["error_code"].append(df["error_code"][i - 1])
                    res["error_name"].append(df["error_name"][i - 1])
                    res["stopped_reason"].append(stopped_reason)
                except:
                    res["Machine"].pop(-1)
                    res["Status"].pop(-1)
                    res["Start_DTTM"].pop(-1)
            elif status_name == "FINISHED" and df["status_name"][i - 1] == "STARTED":
                res["Machine"].append(machine_name)
                res["Status"].append("Run")
                res["Start_DTTM"].append(df["log_datetime"][i - 1])
                res["Stop_DTTM"].append(log_datetime)
                res["Duration"].append(cal_time_delta(df["log_datetime"][i - 1], log_datetime))
                res["error_code"].append("NA")
                res["error_name"].append("NA")
                res["stopped_reason"].append(stopped_reason)
            elif status_name == "32trimform version 1.0.145" and df["status_name"][i - 1] == "FINISHED":
                res["Machine"].append(machine_name)
                res["Status"].append("Stop")
                res["Start_DTTM"].append(log_datetime)
                res["Stop_DTTM"].append(df["log_datetime"][i + 1])
                res["Duration"].append(cal_time_delta(log_datetime, df["log_datetime"][i + 1]))
                res["error_code"].append(event_type)
                res["error_name"].append(status_name)
                res["stopped_reason"].append("NA")
            elif status_name == "FINISHED" and df["status_name"][i - 1] == "State: Specific Running Continuous":
                res["Machine"].append(machine_name)
                res["Status"].append("Run")
                res["Start_DTTM"].append(df["log_datetime"][i - 1])
                res["Stop_DTTM"].append(log_datetime)
                res["Duration"].append(cal_time_delta(df["log_datetime"][i - 1], log_datetime))
                res["error_code"].append("NA")
                res["error_name"].append("NA")
                res["stopped_reason"].append("NA")
            else:
                pass
    result = pd.DataFrame(res)
    return result


if __name__ == "__main__":
    raw_data_csv_file = "raw_data.csv"  # 原始資料檔
    machine_names = get_machine_name(raw_data_csv_file)  # 抓取所有機台名稱    
    res_list = []  # 紀錄所有結果
    
    for machine_name in machine_names:
        df_by_machine = get_dataframe(pd.read_csv(raw_data_csv_file), machine_name)
        res = policy(df_by_machine)
        res_list.append(res)
        
    # 合併res_list的所有資料
    for i, data in enumerate(res_list):
        if i == 0:
            final_res = data
        else:
            final_res = pd.concat([final_res, data], axis=0)

    final_res.reset_index(drop=True, inplace=True)
    final_res.to_csv(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index=False)
