import configparser
import json
from random import randint
from locust import HttpLocust, TaskSet, task, between, seq_task
import hashlib
from datetime import datetime, timedelta


def iso_format(dt: datetime):
    try:
        utc = dt + dt.utcoffset()
    except TypeError:
        utc = dt
    iso_string = datetime.strftime(utc, '%Y-%m-%d %H:%M:%S')
    return iso_string.format(int(round(utc.microsecond / 1000.0)))


class ManageWorkingHourTest(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.jwt_token = None
        self.user_id = None

    def on_start(self):
        header = {'content-type': 'application/json'}
        body = dict()
        body['username'] = self.locust.username[randint(0, 1)]
        body['password'] = self.locust.password
        with self.client.post("/api/user/login", json.dumps(body), headers = header,
                              catch_response = True) as response:
            print(response.content)
            res = json.loads(response.text)
            if res['status'] == 'SUCCESS' and res['result']['JWT']:
                self.jwt_token = res['result']['JWT']
                self.user_id = res['result']['user_id']
            else:
                response.failure("Login failed.")
                self.interrupt()

    @seq_task(1)
    def get_working_hour_list(self):
        if self.user_id == 'SYKJ-20200101-0000':
            pass
        else:
            header = {'Cookie': 'JWT=' + self.jwt_token, 'Content-type': 'application/json'}
            with self.client.get("/api/project/workingHour/" + self.locust.project_id, headers = header,
                                 catch_response = True) as response:
                print(response.content)
                if 'status' in json.loads(response.text):
                    if json.loads(response.text)['status'] == 'SUCCESS':
                        response.success()
                    else:
                        response.failure('Get working hour list failed.')
                else:
                    response.failure('Unknown issue.')

    @seq_task(2)
    def submit_working_hour(self):
        if self.user_id == 'SYKJ-20200101-0000':
            pass
        else:
            body_submit_working_hour = dict()
            body_submit_working_hour['referred_activity_type_id'] = "299308584200568834"
            body_submit_working_hour['referred_function_id'] = "001"
            body_submit_working_hour['start_time'] = iso_format(datetime.now() + timedelta(hours = randint(-8, -1)))
            body_submit_working_hour['end_time'] = iso_format(datetime.now())

            header = {'Cookie': 'JWT=' + self.jwt_token, 'Content-type': 'application/json'}
            body_submit_working_hour_json = json.dumps(body_submit_working_hour)
            print(body_submit_working_hour_json)
            with self.client.put("/api/project/workingHour/" + self.locust.project_id, body_submit_working_hour_json,
                                 headers = header,
                                 catch_response = True) as response:
                print(response.content)
                if 'status' in json.loads(response.text):
                    if json.loads(response.text)['status'] == 'SUCCESS':
                        response.success()
                    else:
                        response.failure('Submit working hour failed.')
                else:
                    response.failure('Unknown issue.')

    @seq_task(3)
    def verify_working_hour(self):
        if self.user_id == 'SYKJ-20200201-0000':
            pass
        else:
            body_verify = dict()
            body_verify['project_id'] = self.locust.project_id

            header = {'Cookie': 'JWT=' + self.jwt_token, 'Content-type': 'application/json'}
            print(json.dumps(body_verify))
            with self.client.post("/api/project/workingHour/verify", json.dumps(body_verify), headers = header,
                                  catch_response = True) as response:
                print(response.content)
                if 'status' in json.loads(response.text):
                    if json.loads(response.text)['status'] == 'SUCCESS':
                        response.success()
                    else:
                        response.failure('Get verify working hour list failed.')
                else:
                    response.failure('Unknown issue.')


class ManageUser(HttpLocust):
    task_set = ManageWorkingHourTest
    username = ["jun28@pingmao.net", "jie62@hotmail.com"]
    password = hashlib.md5(b"password").hexdigest()
    project_id = "2020-4577-D-01"
    config = configparser.ConfigParser()
    config.read('settings.ini')
    host = config.get('DEFAULT', 'host')
    wait_time = between(2, 10)
