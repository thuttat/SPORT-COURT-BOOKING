# Sport Court Booking

A React and Flask application for reserving sports courts. Customers choose a court, date and available time slot, then track or cancel their reservation. Administrators manage courts and review bookings.

![Selecting a time slot in the booking interface](https://raw.githubusercontent.com/thuttat/selenium-sport/b54f264c45ffe9cd4278325f231a0f858a5da351/screenshots/booking/TC_BOOK_01_slot_selected.png)

## Booking and testing

The booking screen requests availability for the selected court and date. The API checks the reservation, and the customer can review it in booking history. The companion browser suite exercises both successful reservations and cases such as conflicting slots, booking quotas and cancellation restrictions. [Booking UI](frontend/src/pages/customer/CourtBooking) · [API specification](bapp/swagger.yml) · [Selenium suite](https://github.com/thuttat/selenium-sport)

The integration tests exercise the Flask application directly. The Selenium project drives the React UI through Chrome using page objects. The Locust script models a sequence of requests from registration through booking. [Integration test commit](https://github.com/thuttat/SPORT-COURT-BOOKING/commit/99f40582cc39864b87ec754f88440566a4b757b3) · [API collections](postman) · [Load scenario](locustfile.py) · [Recorded performance results](results)

## Team contributions

| Contributor | Role and implemented work | Selected commits |
| --- | --- | --- |
| Trịnh Thị Anh Thư (`thuttat`) | Test automation and integration. Added Flask integration tests and fixtures, Postman collections, Locust load scenarios and Selenium browser tests with page objects. | [Integration tests](https://github.com/thuttat/SPORT-COURT-BOOKING/commit/99f40582cc39864b87ec754f88440566a4b757b3) · [Load tests](https://github.com/thuttat/SPORT-COURT-BOOKING/commit/181a7bd26675c1451b991f8a9a23c3e837a48dc6) · [Browser tests](https://github.com/thuttat/selenium-sport/commit/580034d77f16d560f5c3b0b20d4faa2344b450be) |
| Lê Hoàng Bảo Trân (`TranLe05`) | Frontend and API integration. Built the customer profile screen, connected it to the profile API and integrated VNPay into the booking and payment-result screens. | [Customer profile](https://github.com/thuttat/SPORT-COURT-BOOKING/commit/8910aa003c0d29bda99e8c9e030583022a6d15ba) · [Booking and payment UI](https://github.com/thuttat/SPORT-COURT-BOOKING/commit/2d4afbe31c096880feafd96f7ac1c50f31aa2fa8) |
| Nguyễn Triệu Duy (`duynguyenntd`) | Backend and API testing. Implemented the database schema and booking API, updated cancellation rules and added tests for access restrictions and booking edge cases. | [Schema and booking API](https://github.com/thuttat/SPORT-COURT-BOOKING/commit/6f4063de615a78d5025f478406051dbb68dfdfe6) · [Cancellation rules and tests](https://github.com/thuttat/SPORT-COURT-BOOKING/commit/26dbdf985a0eb2e6f4072efd0161f3e2b4aea72b) · [Security tests](https://github.com/thuttat/SPORT-COURT-BOOKING/commit/5f4d420ea3f1171a579fba9680b0cbb9214add5e) |

## Run locally

From the repository root, install the backend dependencies in a Python virtual environment. Use a disposable database for the seed command: it drops and recreates tables. The following commands use a local SQLite file and POSIX shell syntax. For image uploads, set `CLOUDINARY_URL` in the backend environment using your own Cloudinary configuration.

```sh
python -m pip install -r requirements.txt
export DATABASE_URL=sqlite:///sport_demo.db
python -m bapp.seed
python -m bapp.index
```

In another terminal run `npm ci` and `npm run dev` from `frontend/`. Open <http://localhost:5173> with Flask running at <http://localhost:5000>.

## Reproduce the checks

Run the backend suite from the repository root with `DATABASE_URL=sqlite:///:memory: TESTING=true python -m pytest tests/ -v --ignore=tests/test_sel.py`. Browser test setup and screenshots are documented in [selenium-sport](https://github.com/thuttat/selenium-sport). For a load run against your local test instance, use `locust -f locustfile.py --host http://localhost:5000`. The archived CSVs describe a previous run. They do not establish the capacity of the current application.
