from locust import HttpUser, task, between
import random


class ProductsTestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_index(self):
        self.client.get("/?page=1")

    @task(3)
    def test_products(self):
        self.client.get("/products")

    @task(3)
    def test_product(self):
        self.client.get("/products/5")

    @task(2)
    def test_products_query(self):
        self.client.get("/products/?query_name=onep&query_id=")

    def on_start(self):
        self.client.post("/login", {"email": "j@j.com", "password": "123456"})

    def on_stop(self):
        self.client.get("/logout")


class SubscriptionsTestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_index(self):
        self.client.get("/")

    @task(3)
    def test_subscriptions(self):
        self.client.get("/subscriptions")

    @task(2)
    def test_subscription(self):
        self.client.get("/subscriptions/5")

    @task(2)
    def test_subscription_query(self):
        self.client.get("/subscriptions/?query_name=one&query_id=")

    @task(2)
    def test_subscription_update(self):
        self.client.post(
            "/subscriptions/1/update",
            {
                "notification_frequency": random.choice(range(1, 100)),
                "notify_on_price_change": random.choice(["Yes", "No"]),
                "send_notification": random.choice(["Yes", "No"]),
            },
        )

    def on_start(self):
        self.client.post("/login", {"email": "j@j.com", "password": "123456"})

    def on_stop(self):
        self.client.get("/logout")
