from locust import HttpUser, between, task


class TestLoad(HttpUser):
    wait_time = between(1, 1)
    id = 1
    headers = None

    def on_start(self):
        self.id = TestLoad.id
        TestLoad.id += 1

    @task
    def test_scenario(self):
        employee_number = str(self.id).zfill(8)
        response = self.client.post(
            "/api/login",
            json={"employee_number": employee_number, "password": "test"},
            headers={"Cache-Control": "no-cache"},
        )
        print(vars(response))
