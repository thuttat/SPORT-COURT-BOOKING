import os
import random
import string
from datetime import date, timedelta

from locust import HttpUser, task, between, constant, events
from locust.runners import MasterRunner, WorkerRunner

_AVATAR_PATH = os.path.join(os.path.dirname(__file__), "asset", "Picture1.jpg")
with open(_AVATAR_PATH, "rb") as _f:
    _AVATAR_BYTES = _f.read()
_AVATAR_MIME = "image/jpeg"


def random_suffix(n=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

PREF_01_MAX_MS   = 2000
PREF_02_MAX_AVG  = 3000
PREF_02_MAX_FAIL = 0.0

class PerfTest01(HttpUser):
    wait_time = constant(1)
    host = "http://localhost:5000"

    @task
    def tc_pref_01_load_courts(self):
        today = date.today().isoformat()
        with self.client.get(
            "/api/fields",
            params={"date": today, "page": 1},
            catch_response=True,
            name="TC_PREF_01 /api/fields (load courts)"
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"TC_PREF_01 FAIL: status {resp.status_code}")
                return

            data = resp.json().get("data", [])
            elapsed_ms = resp.elapsed.total_seconds() * 1000

            if elapsed_ms > PREF_01_MAX_MS:
                resp.failure(
                    f"TC_PREF_01 FAIL: {elapsed_ms:.0f}ms > {PREF_01_MAX_MS}ms threshold"
                )
            elif len(data) == 0:
                resp.failure("TC_PREF_01 FAIL: Không có court nào — cần seed data trước")
            else:
                resp.success()
                print(f"\n TC_PREF_01 PASS: {len(data)} courts loaded in {elapsed_ms:.0f}ms")

class PerfTest02(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:5000"

    def on_start(self):
        self.username = "user_normal"
        self.password = "User@12345"
        self.booking_id = None
        self.booking_date = (date.today() + timedelta(days=random.randint(1, 7))).isoformat()
        self._login()

    def _login(self):
        with self.client.post(
            "/api/login",
            data={"username": self.username, "password": self.password},
            catch_response=True,
            name="TC_PREF_02 /api/login"
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Login failed: {resp.status_code}")

    @task(3)
    def tc_pref_02_get_fields(self):
        with self.client.get(
            "/api/fields",
            params={"date": self.booking_date},
            catch_response=True,
            name="TC_PREF_02 /api/fields"
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Get fields failed: {resp.status_code}")

    @task(2)
    def tc_pref_02_book(self):
        with self.client.post(
            "/api/bookings",
            data={
                "field_id": random.randint(1, 5),
                "time_slots_id": random.randint(1, 7),
                "booking_date": self.booking_date,
            },
            catch_response=True,
            name="TC_PREF_02 /api/bookings"
        ) as resp:
            if resp.status_code in (201, 400, 409):
                if resp.status_code == 201:
                    data = resp.json().get("data", {})
                    self.booking_id = data.get("booking_id")
                resp.success()
            else:
                resp.failure(f"Book failed: {resp.status_code} - {resp.text[:100]}")

    @task(1)
    def tc_pref_02_my_bookings(self):
        with self.client.get(
            "/api/my-bookings",
            catch_response=True,
            name="TC_PREF_02 /api/my-bookings"
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"My bookings failed: {resp.status_code}")

    def on_stop(self):
        self.client.post("/api/logout", name="TC_PREF_02 /api/logout")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    stats = environment.stats

    print("\n" + "="*60)
    print("PERFORMANCE TEST RESULTS")
    print("="*60)

    # TC_PREF_01
    pref01_entry = stats.get("TC_PREF_01 /api/fields (load courts)", "GET")
    if pref01_entry and pref01_entry.num_requests > 0:
        p95_ms = pref01_entry.get_response_time_percentile(0.95)
        avg_ms = pref01_entry.avg_response_time
        fail_pct = (pref01_entry.num_failures / pref01_entry.num_requests) * 100

        print(f"\nTC_PREF_01 — Homepage loads courts in < {PREF_01_MAX_MS}ms")
        print(f"  Requests : {pref01_entry.num_requests}")
        print(f"  Avg      : {avg_ms:.0f}ms")
        print(f"  95%ile   : {p95_ms:.0f}ms")
        print(f"  Failures : {pref01_entry.num_failures} ({fail_pct:.1f}%)")

        if p95_ms <= PREF_01_MAX_MS and fail_pct == 0:
            print(f"  → ✓ PASS (95%ile {p95_ms:.0f}ms ≤ {PREF_01_MAX_MS}ms)")
        else:
            print(f"  → ✗ FAIL (95%ile {p95_ms:.0f}ms > {PREF_01_MAX_MS}ms hoặc có lỗi)")
            environment.process_exit_code = 1

    # TC_PREF_02
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
        print(f"  → ✓ PASS (0% failure, avg {avg_response:.0f}ms ≤ {PREF_02_MAX_AVG}ms)")
    else:
        reasons = []
        if fail_rate > PREF_02_MAX_FAIL:
            reasons.append(f"failure rate {fail_rate:.2f}% > 0%")
        if avg_response > PREF_02_MAX_AVG:
            reasons.append(f"avg {avg_response:.0f}ms > {PREF_02_MAX_AVG}ms")
        print(f"  → ✗ FAIL ({', '.join(reasons)})")
        environment.process_exit_code = 1

    print("="*60)