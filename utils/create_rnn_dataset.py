import json
import datetime

def get_day_diff(date,diff):
    date_obj = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
    diff_day = date_obj - datetime.timedelta(days=diff)
    return datetime.datetime.strftime(diff_day,"%Y-%m-%dT%H:%M:%S")

def get_time_diff(date,diff_minutes):
    date_obj = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
    diff_day = date_obj - datetime.timedelta(minutes=diff_minutes)
    return datetime.datetime.strftime(diff_day,"%Y-%m-%dT%H:%M:%S")

needed_data = [ lambda x: get_day_diff(x,diff=7),
                lambda x: get_day_diff(x,diff=6),
                lambda x: get_day_diff(x,diff=5),
                lambda x: get_day_diff(x,diff=4),
                lambda x: get_day_diff(x,diff=3),
                lambda x: get_day_diff(x,diff=2),
                lambda x: get_day_diff(x,diff=1),
                lambda x: get_time_diff(x,diff_minutes=15),
                lambda x: get_time_diff(x,diff_minutes=30)]

result = {}
with open("final_output.txt") as fh:
    lines = fh.readlines()
for line in lines:
    line = line.strip()
    if not line:
        continue
    time,count = line.split('\t')
    result[time] = count

for result_time in result:
    temp = [result.get(x(result_time),-1) for x in needed_data]
    if sum([1 for x in temp if x == -1]) > 2:
        continue
    temp_2 = [str(x) if x != -1 else "0" for x in temp]
    temp_2.append(str(result[result_time]))
    temp_str = "\t".join(temp_2)
    print(f"{result_time}\t{temp_str}")



