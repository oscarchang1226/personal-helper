from dotenv import load_dotenv
import os
import json
import requests
import aiohttp
import asyncio

class BaseService:

    def __init__(self, host, token):
        self.host = 'https://' + host
        self.token = token
        self.headers = {"Authorization": "Token " + self.token}

    async def get(self, url):
        url = self.host + url
        # Create an HTTP connection
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as res:
                print("GET: %s" % (url))
                return await res.json()
            
    async def post(self, url, data=None):
        url = self.host + url

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=self.headers) as res:
                print("POST: %s" % (url))
                return await res.json()

class PlaceService(BaseService):

    def __init__(self, host, token):
        super().__init__(host, token)
        self.data = {}
        self.place_url = '/api/v1/places'

    def get_place(self, id):
        url = "%s/%d" % (self.place_url, id)
        if id not in self.data:
            place_details = self.get(url)
            self.data[id] = {
                'id' : place_details['place']['id'],
                'name' : place_details['place']['name'],
                'reservations': place_details['place']['reservations'],
                'fully_reserved_dates': place_details['place']['fully_reserved_dates'][:14]
            }
        return self.data[id]
    
    def add_place_id(future):
        try:
            res = future.result()
            res['place']
        except Exception as e:
            print(f"{e}")
    
    def get_timetable(self, place_id, date):
        url = "%s/%d/reservations/%s/timetable" % (self.place_url, place_id, date)
        res = asyncio.ensure_future(self.get(url))

        def add_place_id(future):
            try:
                res = future.result()
                res['place_id'] = place_id
            except Exception as e:
                print(f"{e}")

        res.add_done_callback(add_place_id)
        
        return res
    
    def reserve_time(self, place_id, date, time_slot):
        url = "%s/%d/reservations/%s/%s" % (self.place_url, place_id, date, time_slot)
        res = asyncio.ensure_future(self.post(url))

        def add_place_id(future):
            try:
                res = future.result()
                res['place_id'] = place_id
            except Exception as e:
                print(f"{e}")

        res.add_done_callback(add_place_id)
        return res
    
class User:

    def __init__(self, user_key, user_value):
        self.user_key = user_key
        token = os.getenv(user_value['token_key'])
        api_host = os.getenv("HOST")
        self.place_service = PlaceService(api_host, token)
        self.reservation_targets = user_value['reservation_targets']
        self.tasks = []

    def get_time_table_callback(self, future):
        try:
            res = future.result()
            target_date = res['date']
            place_id_key = str(res['place_id'])
            res['user_key'] = self.user_key

            if (res['success'] and 
                str(res['place_id']) in self.reservation_targets and 
                target_date in self.reservation_targets[place_id_key]):
                target_times = self.reservation_targets[place_id_key][target_date]
                time_slots = res['time_slots']
                for time_slot in target_times:
                    for open_time_slot in time_slots:
                        if open_time_slot['time'] == time_slot:
                            if open_time_slot['state'] == 'available':
                                task = self.place_service.reserve_time(place_id_key, target_date, time_slot)
                                self.tasks.append(task)

            # if res['success'] and str(res['place_id']) in self.reservation_targets:
            #     target_times = self.reservation_targets[res['place_id']][res['date']]
            #     res['target_times'] = target_times
            #     return res
            
            return res
                
        except Exception as e:
            print(f"{e}")

    async def check_time_table(self):
        for place_id, reservation_targets in self.reservation_targets.items():
            for target_date in reservation_targets:

                task = asyncio.ensure_future(self.place_service.get_timetable(int(place_id), target_date))
                task.add_done_callback(self.get_time_table_callback)
                self.tasks.append(task)

        results = await asyncio.gather(*self.tasks)
        return results


async def main():
    load_dotenv()
    db = {}
    file_name = 'hg_data.json'
    db_file_name = 'db.json'

    with open(file_name, 'r') as file:
        data = json.load(file)

    with open(db_file_name, 'r') as file:
        db = json.load(file)

    tasks = []

    for user_key, user_value in db.items():
        user = User(user_key, user_value)
        result = await user.check_time_table()
        tasks = tasks + result

    for task in tasks:
        print(task)


# service = PlaceService(api_host, oscar_token)
# service.get_place(145)
# service.get_place(144)
# service.get_timetable(145, '2023-10-28')
# service.get_timetable(144, '2023-10-29')
# data['places'] = service.data

if __name__ == '__main__':
    asyncio.run(main())