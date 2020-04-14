import configparser
import json
from random import randint
from locust import HttpLocust, TaskSet, task, between, seq_task
import hashlib


class ManageProjectRolePermissionTest(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.jwt_token = None

    def on_start(self):
        header = {'content-type': 'application/json'}
        body = dict()
        body['username'] = self.locust.username
        body['password'] = self.locust.password
        with self.client.post("/api/user/login", json.dumps(body), headers = header,
                              catch_response = True) as response:
            print(response.content)
            res = json.loads(response.text)
            if res['status'] == 'SUCCESS' and res['result']['JWT']:
                self.jwt_token = res['result']['JWT']
            else:
                response.failure("Login failed.")
                self.interrupt()

    @seq_task(1)
    def get_member_list(self):
        body_get_member = dict()
        body_get_member['project_id'] = self.locust.project_id
        header = {'Cookie': 'JWT=' + self.jwt_token, 'Content-type': 'application/json'}
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
        body_add_role = dict()
        body_add_role['project_id'] = self.locust.project_id
        body_add_role['user_id'] = "SYKJ-20200201-0000"
        body_add_role['project_role_id_list'] = list()
        project_role_id = dict()
        project_role_id['project_role_id'] = "290089467161608193"
        project_role_id['superior_id'] = "SYKJ-20200101-0000"
        body_add_role['project_role_id_list'].append(project_role_id)
        # body_add_role = {
        #     "project_id": "2020-4577-D-01",
        #     "user_id": "SYKJ-20200201-0000",
        #     "project_role_id_list": [
        #         {
        #             "project_role_id": "290089467161608193",
        #             "superior_id": "SYKJ-20200101-0000"
        #         }
        #     ]
        # }
        header = {'Cookie': 'JWT=' + self.jwt_token, 'Content-type': 'application/json'}
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
        body_add_permission = dict()
        body_add_permission['user_id'] = ["SYKJ-20200101-0000", "SYKJ-20200201-0000"][randint(0, 1)]
        body_add_permission['project_id'] = "2020-4577-D-01"
        body_add_permission['privilege_list'] = [
            "working_hour_modification",
            "working_hour_access",
            "working_hour_verification",
            "issue_tracker_modification",
            "issue_tracker_access"
        ]
        header = {'Cookie': 'JWT=' + self.jwt_token, 'Content-type': 'application/json'}
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


class ManageUser(HttpLocust):
    task_set = ManageProjectRolePermissionTest
    username = "jun28@pingmao.net"
    password = hashlib.md5(b"password").hexdigest()
    project_id = "2020-4577-D-01"
    config = configparser.ConfigParser()
    config.read('settings.ini')
    host = config.get('DEFAULT', 'host')
    wait_time = between(1, 5)
