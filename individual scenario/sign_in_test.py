import hashlib
import json
from random import randint
from locust import HttpLocust, TaskSet, task, between
import configparser


class SignInTask(TaskSet):
    def on_start(self):
        pass

    @task
    def sign_in(self):
        header = {'content-type': 'application/json'}
        body = dict()
        body['username'] = self.locust.username[randint(0, 1)]
        body['password'] = self.locust.password
        with self.client.post("/api/user/login", json.dumps(body), headers = header, catch_response = True) as response:
            print(response.content)
            if json.loads(response.text)['status'] == "SUCCESS":
                response.success()
            else:
                response.failure("Login failed.")


class SignInUser(HttpLocust):
    username = ["jun28@pingmao.net", "jie62@hotmail.com"]
    password = hashlib.md5(b"password").hexdigest()
    task_set = SignInTask
    config = configparser.ConfigParser()
    config.read('settings.ini')
    host = config.get('DEFAULT', 'host')
    # 思考时间1-5秒
    wait_time = between(1, 5)
