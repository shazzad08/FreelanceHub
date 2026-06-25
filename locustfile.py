from locust import HttpUser, task, between

class FreelanceHubUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def home(self):
        self.client.get("/")

    @task(5)
    def project_list(self):
        self.client.get("/projects/")

    @task(2)
    def project_detail(self):
        self.client.get("/projects/1/")