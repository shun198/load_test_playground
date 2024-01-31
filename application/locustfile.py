from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def health(self):
        self.client.get("http://127.0.0.1:8000/api/health/")
