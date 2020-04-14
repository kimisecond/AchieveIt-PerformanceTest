import configparser
import json
from random import randint
import random
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


def random_pick(some_list, probabilities):
    global item
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


class MixedScenarioTest(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.jwt_token = None
        self.user_id = None

    def on_start(self):
        header = {'content-type': 'application/json'}
        body = dict()
        body['username'] = random_pick(self.locust.username, [0.05, 0.95])
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
    def view_project_list(self):
        body_list_relative = dict()
        body_list_relative['page_size'] = 20
        body_list_relative['current_page'] = 1
        header = {'Cookie': 'JWT=' + self.jwt_token, 'content-type': 'application/json'}
        print(json.dumps(body_list_relative))
        with self.client.post("/api/project/listRelative", json.dumps(body_list_relative), headers = header,
                              catch_response = True) as response:
            print(response.content)
            if 'status' in json.loads(response.text):
                if json.loads(response.text)['status'] == 'SUCCESS':
                    response.success()
                else:
                    response.failure('Browse failed.')
            else:
                response.failure('Unknown issue.')

    @task
    def search(self):
        body = dict()
        body['key_word'] = self.locust.keyword[randint(0, 7)]
        body['page_size'] = 20
        body['current_page'] = 1
        header = {'Cookie': 'JWT=' + self.jwt_token, 'content-type': 'application/json'}
        print(json.dumps(body))
        with self.client.post("/api/project/search", json.dumps(body), headers = header,
                              catch_response = True) as response:
            print(response.content)
            if 'status' in json.loads(response.text):
                if json.loads(response.text)['status'] == 'SUCCESS':
                    response.success()
                else:
                    response.failure('Search failed.')
            else:
                response.failure('Unknown issue.')

    @task
    class ManageProjectRolePermissionTest(TaskSet):
        @seq_task(1)
        def get_member_list(self):
            body_get_member = dict()
            body_get_member['project_id'] = self.parent.locust.project_id
            header = {'Cookie': 'JWT=' + self.parent.jwt_token, 'Content-type': 'application/json'}
            print(json.dumps(body_get_member))
            with self.client.post("/api/user/projectMember", json.dumps(body_get_member), headers = header,
                                  catch_response = True) as response:
                print(response.content)
                if 'status' in json.loads(response.text):
                    if json.loads(response.text)['status'] == 'SUCCESS':
                        response.success()
                    else:
                        response.failure('Get project member failed.')
                else:
                    response.failure('Unknown issue.')

        @seq_task(2)
        def set_member_role(self):
            if self.parent.user_id == 'SYKJ-20200101-0000':
                body_add_role = dict()
                body_add_role['project_id'] = self.parent.locust.project_id
                body_add_role['user_id'] = "SYKJ-20200201-0000"
                body_add_role['project_role_id_list'] = list()
                project_role_id = dict()
                project_role_id['project_role_id'] = "290089467161608193"
                project_role_id['superior_id'] = "SYKJ-20200101-0000"
                body_add_role['project_role_id_list'].append(project_role_id)
                header = {'Cookie': 'JWT=' + self.parent.jwt_token, 'Content-type': 'application/json'}
                body_add_role_json = json.dumps(body_add_role)
                print(body_add_role_json)
                with self.client.put("/api/user/userProjectRole", body_add_role_json, headers = header,
                                     catch_response = True) as response:
                    print(response.content)
                    if 'status' in json.loads(response.text):
                        if json.loads(response.text)['status'] == 'SUCCESS':
                            response.success()
                        else:
                            response.failure('Set project member role failed.')
                    else:
                        response.failure('Unknown issue.')

        @seq_task(3)
        def set_member_permission(self):
            if self.parent.user_id == 'SYKJ-20200101-0000':
                body_add_permission = dict()
                body_add_permission['user_id'] = ["SYKJ-20200101-0000", "SYKJ-20200201-0000"][randint(0, 1)]
                body_add_permission['project_id'] = self.parent.locust.project_id
                body_add_permission['privilege_list'] = [
                    "working_hour_modification",
                    "working_hour_access",
                    "working_hour_verification",
                    "issue_tracker_modification",
                    "issue_tracker_access"
                ]
                header = {'Cookie': 'JWT=' + self.parent.jwt_token, 'Content-type': 'application/json'}
                print(json.dumps(body_add_permission))
                with self.client.put("/api/user/permission", json.dumps(body_add_permission), headers = header,
                                     catch_response = True) as response:
                    print(response.content)
                    if 'status' in json.loads(response.text):
                        if json.loads(response.text)['status'] == 'SUCCESS':
                            response.success()
                        else:
                            response.failure('Set member permission failed.')
                    else:
                        response.failure('Unknown issue.')

    @task
    class ManageWorkingHourTest(TaskSet):
        @seq_task(1)
        def get_working_hour_list(self):
            if self.parent.user_id == 'SYKJ-20200101-0000':
                pass
            else:
                header = {'Cookie': 'JWT=' + self.parent.jwt_token, 'Content-type': 'application/json'}
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
            if self.parent.user_id == 'SYKJ-20200101-0000':
                pass
            else:
                body_submit_working_hour = dict()
                body_submit_working_hour['referred_activity_type_id'] = "299308584200568834"
                body_submit_working_hour['referred_function_id'] = "001"
                body_submit_working_hour['start_time'] = iso_format(datetime.now() + timedelta(hours = randint(-8, -1)))
                body_submit_working_hour['end_time'] = iso_format(datetime.now())

                header = {'Cookie': 'JWT=' + self.parent.jwt_token, 'Content-type': 'application/json'}
                body_submit_working_hour_json = json.dumps(body_submit_working_hour)
                print(body_submit_working_hour_json)
                with self.client.put("/api/project/workingHour/" + self.locust.project_id,
                                     body_submit_working_hour_json,
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
            if self.parent.user_id == 'SYKJ-20200201-0000':
                pass
            else:
                body_verify = dict()
                body_verify['project_id'] = self.parent.locust.project_id

                header = {'Cookie': 'JWT=' + self.parent.jwt_token, 'Content-type': 'application/json'}
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
    task_set = MixedScenarioTest
    keyword = ["SimpleManage", "Simple", "Manage", "开发", "Sim", "Sin", "fqoawejfio", "afuihqwu"]
    username = ["jun28@pingmao.net", "jie62@hotmail.com"]
    password = hashlib.md5(b"password").hexdigest()
    project_id = "2020-4577-D-01"
    config = configparser.ConfigParser()
    config.read('settings.ini')
    host = config.get('DEFAULT', 'host')
    wait_time = between(2, 10)
