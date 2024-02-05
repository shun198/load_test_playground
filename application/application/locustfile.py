import random
import time

from locust import HttpUser, between, run_single_user, task


class TestLoad(HttpUser):
    wait_time = between(1, 1)
    id = 1
    csrftoken = None
    headers = None

    def on_start(self):
        self.id = TestLoad.id
        TestLoad.id += 1

    @task
    def test_scenario(self):
        if not self.csrftoken:
            token_res = self.client.get(
                "/api/users/get_csrf_token",
                headers={"Cache-Control": "no-cache"},
            )
            self.csrftoken = token_res.cookies.get("csrftoken")
            self.headers = {
                "X-CSRFToken": self.csrftoken,
            }

        employee_number = str(self.id).zfill(8)
        self.client.post(
            "/api/login",
            json={
                "employee_number": employee_number,
                "password": "test",
            },
            headers=self.headers,
            cookies={"csrftoken": self.csrftoken},
        )

        time.sleep(random.randrange(5, 25))
        file_path=""
        files = {"file":file_path}
        response = self.client.post(
            "/api/customer/import_customer_csv",
            files=files,
            headers=self.headers,
            cookies={"csrftoken": self.csrftoken},
        )
        print(vars(response))

# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(TestLoad)
