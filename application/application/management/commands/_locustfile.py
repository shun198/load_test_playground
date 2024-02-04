from locust import HttpUser, between, run_single_user, task


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
            json={
                "employee_number": employee_number,
                "password": "test",
            },
            headers={"Cache-Control": "no-cache"},
        )
        print(vars(response))


# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(TestLoad)
