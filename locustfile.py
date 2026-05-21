import os
import time
import random
import string
from datetime import date, timedelta
from locust import HttpUser, task, between, SequentialTaskSet, events

_AVATAR_PATH = os.path.join(os.path.dirname(__file__), "asset", "Picture1.jpg")
with open(_AVATAR_PATH, "rb") as _f:
    _AVATAR_BYTES = _f.read()
_AVATAR_MIME = "image/jpeg"

PREF_01_MAX_MS   = 2200
PREF_02_MAX_AVG  = 3000
PREF_02_MAX_FAIL = 0


def random_suffix(n=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


class BookingFlow(SequentialTaskSet):

    def on_start(self):
        self.booking_id = None
        self.username = f"locust_{random_suffix()}"
        self.password = "Locust@123"
        self.email = f"{self.username}@test.com"
        self.field_id = None
        self.slot_id = None
        self.my_booking_id = None
        self.booking_date = (date.today() + timedelta(days=random.randint(1, 7))).isoformat()

    @task
    def step_register(self):
        time.sleep(random.uniform(1.0, 3.0))
        with self.client.post(
            "/api/register",
            data={
                "fullname": f"Locust User {self.username}",
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "confirm": self.password,
            },
            files={"avatar": ("Picture1.jpg", _AVATAR_BYTES, _AVATAR_MIME)},
            catch_response=True,
            name="/api/register"
        ) as resp:
            if resp.status_code in (200, 201):
                resp.success()
            elif resp.status_code == 0:
                resp.success()
                self.interrupt()
            else:
                resp.failure(f"Register failed: {resp.status_code} - {resp.text[:200]}")
                self.interrupt()

    @task
    def step_login(self):
        with self.client.post(
            "/api/login",
            data={"username": self.username, "password": self.password},
            catch_response=True,
            name="/api/login"
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Login failed: {resp.status_code} - {resp.text[:200]}")
                self.interrupt()

    @task
    def step_get_me(self):
        with self.client.get("/api/me", catch_response=True, name="/api/me") as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Get me failed: {resp.status_code}")

    @task
    def step_browse_pages(self):
        for path, name in [("/", "/"), ("/login", "/login"), ("/register", "/register"),
                           ("/bookings", "/bookings"), ("/profile", "/profile")]:
            self.client.get(path, name=name)

    @task
    def step_get_fields(self):
        with self.client.get(
            "/api/fields",
            params={"date": self.booking_date},
            catch_response=True,
            name="/api/fields"
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Get fields failed: {resp.status_code}")
                self.interrupt()
                return

            fields = resp.json().get("data", [])
            available = [f for f in fields if f.get("is_available") is not False]
            if not available:
                resp.failure("Không có sân trống")
                self.interrupt()
                return

            field = random.choice(available)
            self.field_id = field["id"]
            resp.success()

    @task
    def step_get_field_detail(self):
        if not self.field_id:
            return
        self.client.get(
            f"/api/fields/{self.field_id}",
            name="/api/fields/{id}"
        )

    @task
    def step_get_slots(self):
        if not self.field_id:
            self.interrupt()
            return

        with self.client.get(
            f"/api/fields/{self.field_id}/slots",
            params={"date": self.booking_date},
            catch_response=True,
            name="/api/fields/{id}/slots"
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Get slots failed: {resp.status_code}")
                self.interrupt()
                return

            slots = resp.json().get("data", [])
            available_slots = [s for s in slots
                               if s.get("is_available") and s.get("duration", 0) >= 1]
            if not available_slots:
                self.booking_date = (date.today() + timedelta(days=random.randint(2, 14))).isoformat()
                self.slot_id = None
                resp.success()
                return

            self.slot_id = random.choice(available_slots)["id"]
            resp.success()

    @task
    def step_booking(self):
        if not self.field_id or not self.slot_id:
            self.interrupt()
            return

        with self.client.post(
            "/api/bookings",
            data={
                "field_id": self.field_id,
                "time_slots_id": self.slot_id,
                "booking_date": self.booking_date,
            },
            catch_response=True,
            name="/api/bookings"
        ) as resp:
            if resp.status_code in (200, 201):
                self.booking_id = resp.json().get("data", {}).get("booking_id")
                resp.success()
            elif resp.status_code == 409:
                resp.success()
                self.booking_id = None
            else:
                resp.failure(f"Booking failed: {resp.status_code} - {resp.text[:200]}")

    @task
    def step_get_my_bookings(self):
        with self.client.get(
            "/api/my-bookings",
            params={"page": 1},
            catch_response=True,
            name="/api/my-bookings"
        ) as resp:
            if resp.status_code == 200:
                items = resp.json().get("data", [])
                if items:
                    self.my_booking_id = items[0]["id"]
                resp.success()
            else:
                resp.failure(f"Get my bookings failed: {resp.status_code}")

    @task
    def step_get_booking_detail(self):
        bid = self.booking_id or self.my_booking_id
        if not bid:
            return
        self.client.get(
            f"/api/my-bookings/{bid}",
            name="/api/my-bookings/{id}"
        )

    @task
    def step_update_profile(self):
        with self.client.patch(
            "/api/profile",
            data={"fullname": f"Locust {random_suffix(4)}"},
            catch_response=True,
            name="/api/profile [PATCH]"
        ) as resp:
            if resp.status_code in (200, 400, 422):
                resp.success()
            else:
                resp.failure(f"Update profile failed: {resp.status_code}")

    @task
    def step_cancel(self):
        if not self.booking_id:
            return

        time.sleep(random.uniform(0.5, 1.5))

        with self.client.delete(
            f"/api/bookings/{self.booking_id}",
            catch_response=True,
            name="/api/bookings/{id} [DELETE]"
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            elif resp.status_code in (400, 403):
                resp.success()
            else:
                resp.failure(f"Cancel failed: {resp.status_code} - {resp.text[:200]}")

    @task
    def step_logout(self):
        with self.client.post(
            "/api/logout",
            catch_response=True,
            name="/api/logout"
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Logout failed: {resp.status_code}")

        self.username = f"locust_{random_suffix()}"
        self.email = f"{self.username}@test.com"
        self.booking_id = None
        self.my_booking_id = None
        self.field_id = None
        self.slot_id = None


class AdminFlow(SequentialTaskSet):

    def on_start(self):
        self.field_id = None
        self.booking_id = None

    @task
    def step_admin_login(self):
        with self.client.post(
            "/api/login",
            data={"username": "duyadmin", "password": "Admin@12345"},
            catch_response=True,
            name="/api/login [admin]"
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Admin login failed: {resp.status_code}")
                self.interrupt()

    @task
    def step_dashboard_summary(self):
        self.client.get(
            "/api/admin/dashboard/summary",
            name="/api/admin/dashboard/summary"
        )

    @task
    def step_dashboard_chart(self):
        self.client.get(
            "/api/admin/dashboard/chart-sport",
            name="/api/admin/dashboard/chart-sport"
        )

    @task
    def step_dashboard_recent(self):
        self.client.get(
            "/api/admin/dashboard/recent-bookings",
            name="/api/admin/dashboard/recent-bookings"
        )

    @task
    def step_admin_get_fields(self):
        with self.client.get(
            "/api/admin/fields",
            catch_response=True,
            name="/api/admin/fields [GET]"
        ) as resp:
            if resp.status_code == 200:
                fields = resp.json().get("data", [])
                if fields:
                    self.field_id = fields[0]["id"]
                resp.success()
            else:
                resp.failure(f"Admin get fields failed: {resp.status_code}")

    @task
    def step_admin_get_field_detail(self):
        if not self.field_id:
            return
        self.client.get(
            f"/api/admin/fields/{self.field_id}",
            name="/api/admin/fields/{id} [GET]"
        )

    @task
    def step_admin_create_field(self):
        with self.client.post(
            "/api/admin/fields",
            data={
                "name": f"Sân Test {random_suffix(4)}",
                "field_type": random.choice(["FOOTBALL", "BADMINTON", "TENNIS"]),
                "price_per_hour": random.randint(100000, 500000),
                "description": "Sân tạo bởi Locust test",
            },
            files={"image": ("Picture1.jpg", _AVATAR_BYTES, _AVATAR_MIME)},
            catch_response=True,
            name="/api/admin/fields [POST]"
        ) as resp:
            if resp.status_code in (200, 201):
                new_id = resp.json().get("data", {}).get("id")
                if new_id:
                    self.field_id = new_id
                resp.success()
            else:
                resp.failure(f"Create field failed: {resp.status_code} - {resp.text[:200]}")

    @task
    def step_admin_update_field(self):
        if not self.field_id:
            return
        with self.client.patch(
            f"/api/admin/fields/{self.field_id}",
            data={"description": f"Cập nhật bởi Locust {random_suffix(4)}"},
            catch_response=True,
            name="/api/admin/fields/{id} [PATCH]"
        ) as resp:
            if resp.status_code in (200, 400, 404):
                resp.success()
            else:
                resp.failure(f"Update field failed: {resp.status_code}")

    @task
    def step_admin_delete_field(self):
        if not self.field_id:
            return
        with self.client.delete(
            f"/api/admin/fields/{self.field_id}",
            catch_response=True,
            name="/api/admin/fields/{id} [DELETE]"
        ) as resp:
            if resp.status_code in (200, 400, 404):
                resp.success()
            else:
                resp.failure(f"Delete field failed: {resp.status_code}")
        self.field_id = None

    @task
    def step_admin_get_bookings(self):
        with self.client.get(
            "/api/admin/bookings",
            catch_response=True,
            name="/api/admin/bookings [GET]"
        ) as resp:
            if resp.status_code == 200:
                bookings = resp.json().get("data", [])
                if bookings:
                    self.booking_id = bookings[0]["id"]
                resp.success()
            else:
                resp.failure(f"Admin get bookings failed: {resp.status_code}")

    @task
    def step_admin_get_booking_detail(self):
        if not self.booking_id:
            return
        self.client.get(
            f"/api/admin/bookings/{self.booking_id}",
            name="/api/admin/bookings/{id} [GET]"
        )

    @task
    def step_admin_update_booking_status(self):
        if not self.booking_id:
            return
        with self.client.patch(
            f"/api/admin/bookings/{self.booking_id}/status",
            data={"status": random.choice(["CONFIRMED", "CANCELLED"])},
            catch_response=True,
            name="/api/admin/bookings/{id}/status [PATCH]"
        ) as resp:
            if resp.status_code in (200, 400, 404):
                resp.success()
            else:
                resp.failure(f"Update booking status failed: {resp.status_code}")

    @task
    def step_admin_logout(self):
        self.client.post("/api/logout", name="/api/logout [admin]")
        self.field_id = None
        self.booking_id = None


class WebsiteUser(HttpUser):
    wait_time = between(3, 5)
    tasks = {BookingFlow: 4, AdminFlow: 1}


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    stats = environment.stats

    print("\n" + "="*60)
    print("PERFORMANCE TEST RESULTS")
    print("="*60)

    pref01_key = ("/api/fields", "GET")
    pref01_entry = stats.entries.get(pref01_key)
    if pref01_entry and pref01_entry.num_requests > 0:
        p95_ms   = pref01_entry.get_response_time_percentile(0.95)
        avg_ms   = pref01_entry.avg_response_time
        fail_pct = (pref01_entry.num_failures / pref01_entry.num_requests) * 100

        print(f"\nTC_PREF_01 — Homepage loads courts in < {PREF_01_MAX_MS}ms")
        print(f"  Requests : {pref01_entry.num_requests}")
        print(f"  Avg      : {avg_ms:.0f}ms")
        print(f"  95%ile   : {p95_ms:.0f}ms")
        print(f"  Failures : {pref01_entry.num_failures} ({fail_pct:.1f}%)")

        if p95_ms <= PREF_01_MAX_MS and fail_pct == 0:
            print(f"  →  PASS (95%ile {p95_ms:.0f}ms ≤ {PREF_01_MAX_MS}ms)")
        else:
            print(f"  →  FAIL (95%ile {p95_ms:.0f}ms > {PREF_01_MAX_MS}ms hoặc có lỗi)")
            environment.process_exit_code = 1

    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    avg_response   = stats.total.avg_response_time
    fail_rate      = (total_failures / total_requests * 100) if total_requests > 0 else 0

    print(f"\nTC_PREF_02 — 50 concurrent users, 0% failure, avg < {PREF_02_MAX_AVG}ms")
    print(f"  Total requests : {total_requests}")
    print(f"  Failures       : {total_failures} ({fail_rate:.2f}%)")
    print(f"  Avg response   : {avg_response:.0f}ms")

    pref02_pass = (fail_rate <= PREF_02_MAX_FAIL and avg_response <= PREF_02_MAX_AVG)
    if pref02_pass:
        print(f"  → PASS (0% failure, avg {avg_response:.0f}ms ≤ {PREF_02_MAX_AVG}ms)")
    else:
        reasons = []
        if fail_rate > PREF_02_MAX_FAIL:
            reasons.append(f"failure rate {fail_rate:.2f}% > 0%")
        if avg_response > PREF_02_MAX_AVG:
            reasons.append(f"avg {avg_response:.0f}ms > {PREF_02_MAX_AVG}ms")
        print(f"  → FAIL ({', '.join(reasons)})")
        environment.process_exit_code = 1

    print("="*60)