from locust import HttpUser, task, between
import time

class ProductsTestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_index(self):
        self.client.get(f"/?page=1")

    @task(3)
    def test_products(self):
        self.client.get("/products")

    @task(2)
    def test_products_query_by_name(self):
        self.client.get("/products/?query_name=onep&query_id=")


    @task(2)
    def test_product_subscription(self):
        self.client.post("/products/8", {
            "subscribe_button": "Subscribe product"
        })

    @task(2)
    def test_product_unsubscription(self):
        self.client.post("/products/8", {
            "unsubscribe_button": "Unsubscribe product"
        })

    def on_start(self):
        self.client.post("/login", {
            "email":"j@j.com",
            "password":"123456"
        })
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

    @task(3)
    def test_subscriptions(self):
        self.client.get("/subscriptions")


    def on_start(self):
        self.client.post("/login", {
            "email":"j@j.com",
            "password":"123456"
        })
    def on_stop(self):
        self.client.get("/logout")