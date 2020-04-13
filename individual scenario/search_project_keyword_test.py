import configparser
import json
from random import randint
from locust import HttpLocust, TaskSet, task, between
import hashlib


class SearchProjectKeywordTest(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.jwt_token = None

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
            else:
                response.failure("Login failed.")
                self.interrupt()

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


class SearchUser(HttpLocust):
    task_set = SearchProjectKeywordTest
    keyword = ["SimpleManage", "Simple", "Manage", "开发", "Sim", "Sin", "fqoawejfio", "afuihqwu"]
    username = ["jun28@pingmao.net", "jie62@hotmail.com"]
    password = hashlib.md5(b"password").hexdigest()
    config = configparser.ConfigParser()
    config.read('settings.ini')
    host = config.get('DEFAULT', 'host')
    wait_time = between(1, 5)
