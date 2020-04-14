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


class ManageRiskTest(TaskSet):
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

    @task
    def get_risk_list(self):
        header = {'Cookie': 'JWT=' + self.jwt_token, 'Content-type': 'application/json'}
        with self.client.get("/api/project/risk/" + self.locust.project_id, headers = header,
                             catch_response = True) as response:
            print(response.content)
            if 'status' in json.loads(response.text):
                if json.loads(response.text)['status'] == 'SUCCESS':
                    response.success()
                else:
                    response.failure('Get working hour list failed.')
            else:
                response.failure('Unknown issue.')

    @task
    def submit_risk(self):
        if self.user_id == 'SYKJ-20200201-0000':
            pass
        else:
            body_submit_risk = dict()
            body_submit_risk['risk_type'] = ["PS", "PD", "ST", "CU", "DE", "TE", "BU"][randint(0, 6)]
            body_submit_risk['risk_description'] = "测试" + str(randint(1000, 99999))
            body_submit_risk['risk_level'] = ["H", "M", "L"][randint(0, 2)]
            body_submit_risk['risk_impact'] = ["H", "M", "L"][randint(0, 2)]
            body_submit_risk['risk_countermeasure'] = "沟通"
            body_submit_risk['risk_status'] = ["已识别", "解决中", "已解决"][randint(0, 2)]
            body_submit_risk['risk_responsible_person'] = "SYKJ-20200101-0000"
            body_submit_risk['risk_track_frequency'] = "每周" + str(randint(1, 5)) + "次"
            body_submit_risk['risk_related_person'] = ["SYKJ-20200101-0000", "SYKJ-20200201-0000"]

            header = {'Cookie': 'JWT=' + self.jwt_token, 'Content-type': 'application/json'}
            body_submit_risk_json = json.dumps(body_submit_risk)
            print(body_submit_risk_json)
            with self.client.put("/api/project/risk/" + self.locust.project_id, body_submit_risk_json,
                                 headers = header,
                                 catch_response = True) as response:
                print(response.content)
                if 'status' in json.loads(response.text):
                    if json.loads(response.text)['status'] == 'SUCCESS':
                        response.success()
                    else:
                        response.failure('Submit risk failed.')
                else:
                    response.failure('Unknown issue.')


class ManageUser(HttpLocust):
    task_set = ManageRiskTest
    username = ["jun28@pingmao.net", "jie62@hotmail.com"]
    password = hashlib.md5(b"password").hexdigest()
    project_id = "2020-4577-D-01"
    config = configparser.ConfigParser()
    config.read('settings.ini')
    host = config.get('DEFAULT', 'host')
    wait_time = between(2, 10)
