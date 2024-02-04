from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def health(self):
        response = self.client.get("/api/health")
        print(response.json())
