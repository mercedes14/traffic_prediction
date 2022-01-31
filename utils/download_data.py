import datetime
import  requests
import os
import shutil

def generate_time_range_array(date):
    current_date = date
    while current_date.day == date.day:
        current_date += datetime.timedelta(minutes=15)
        yield current_date

def download_data(start_date, end_date):
    folders=os.listdir("./data/")
    images = {}
    start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    difference = end_date - start_date
    prev_days = [end_date - datetime.timedelta(x) for x in range(0, difference.days)]
    for prev_day in prev_days:
        for cur_date_time in generate_time_range_array(prev_day):
            try:
                date_string = datetime.datetime.strftime(cur_date_time,"%Y-%m-%dT%H:%M:%S")
                response = requests.get(f"https://api.data.gov.sg/v1/transport/traffic-images?date_time={date_string}")
                response_body = response.json()
                if not (response_body.get("items",[]) and response_body["items"][0].get("cameras",[])):
                    print(f"No data for - {prev_day}")
                    continue
                cameras_list = response_body["items"][0]["cameras"]
                for camera_data in cameras_list:
                    location = camera_data["location"]
                    location_string = f"{location['latitude']}_{location['longitude']}"
                    if location_string not in folders:
                        os.makedirs(f"./data/{location_string}")
                        folders.append(location_string)
                    # if location_string == "1.29792_103.78205":                        
                    #     if os.path.exists(f"./data/{location_string}/{date_string}.jpg"):
                    #         continue
                    image_path = camera_data['image']
                    image_response = requests.get(image_path,stream=True)
                    with open(f"./data/{location_string}/{date_string}.jpg",'wb') as fh:
                        image_response.raw.decode_content = True
                        shutil.copyfileobj(image_response.raw, fh)
                        # break
            except Exception as e:
                print(f"Error while getting data for day - {prev_day} - {str(e)}")
                continue
    return images

def get_weather_data():
    data = {}
    with open('rnn_dataset.txt') as fh:
        lines = fh.readlines()
        lines = [l.strip().split("\t") for l in lines]
        data = {l[0]:l for l in lines}
        lat = 1.29792
        lon = 103.78205
        nearest_station = ""

        for date in data:
            date_obj = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
            response = requests.get(f"https://api.data.gov.sg/v1/environment/rainfall?date_time={date}")
            response_body = response.json()
            items = response_body["items"]
            stations = response_body["metadata"]["stations"]
            if nearest_station == "":
                minimum_distance = 180
                for station in stations:
                    tem = abs(float(lat) - station["location"]["latitude"]) + abs(float(lon) - station["location"]["longitude"])
                    if tem < minimum_distance:
                        minimum_distance = tem
                        nearest_station = station["id"]
            for rain_fall in items[0]["readings"]:
                if rain_fall["station_id"] == nearest_station:
                    data[date].append(str(rain_fall["value"]))
                    break
    with open("rnn_dataset_with_weather.txt","w") as fh:
        for d in data:
            line = "\t".join(data[d])
            fh.write(f"{line}\n")



download_data('2021-08-30', '2022-01-28')
# get_weather_data()