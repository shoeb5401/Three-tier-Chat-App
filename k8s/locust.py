from locust import HttpUser, task, between
import random

# Test accounts
USERS = [
    {"email": "shoeb123@gmail.com", "password": "Shoebshoeb1@", "username": "shoeb123"},
    {"email": "zaid123.com", "password": "Shoebshoeb1@", "username": "zaid"}
]

class ChatAppUser(HttpUser):
    wait_time = between(1, 3)

    chat_ids = [
        "68b3db1df23915a857fcadab",
        "7fa9db12e29345a123b9fdef",
        "5bc7cd8aee993a3b5679c8aa"
    ]

    def on_start(self):
          # 🚨 Disable SSL verification globally
        self.client.verify = False  
        # Assign one test account to this simulated user
        self.user = random.choice(USERS)
        self.partner = [u for u in USERS if u["email"] != self.user["email"]][0]

        # Step 1: Sign in
        resp = self.client.post("/login", json={
            "email": self.user["email"],
            "password": self.user["password"]
        })
        token = resp.json().get("token")

        # Save token in headers for all requests
        self.client.headers = {"Authorization": f"Bearer {token}"}

    @task(6)  # 60%: fetch messages
    def get_messages(self):
        chat_id = random.choice(self.chat_ids)
        self.client.get(f"/api/messages/{chat_id}")

    @task(3)  # 30%: send message to partner
    def send_message(self):
        chat_id = random.choice(self.chat_ids)
        self.client.post(
            f"/api/messages/send/{chat_id}",
            json={
                "from": self.user["username"],
                "to": self.partner["username"],
                "msg": f"Hello {self.partner['username']} from {self.user['username']}!"
            }
        )

    @task(5)  # 10%: health check
    def health(self):
        self.client.get("/health")
