import threading
import time
import random


class DressingRooms:
    def __init__(self, num_rooms=3):
        # Input validation for the number of rooms
        if not isinstance(num_rooms, int) or num_rooms < 1:
            raise ValueError("Number of rooms must be a positive integer.")
        self.num_rooms = num_rooms
        self.semaphore = threading.Semaphore(num_rooms)
        self.lock = threading.Lock()  # For thread-safe logging

    def requestRoom(self, customer_id):
        with self.lock:
            print("Customer {} is waiting for a dressing room.".format(customer_id))

        self.semaphore.acquire()
        with self.lock:
            print("Customer {} has entered a dressing room.".format(customer_id))

    def releaseRoom(self, customer_id):
        with self.lock:
            print("Customer {} has exited a dressing room.".format(customer_id))
        self.semaphore.release()


class Customer(threading.Thread):
    def __init__(self, customer_id, num_items, dressing_rooms):
        threading.Thread.__init__(self)
        # Validate number of items
        if not (1 <= num_items <= 6):
            raise ValueError("Customers can only take 1 to 6 items into the dressing room.")
        self.customer_id = customer_id
        self.num_items = num_items
        self.dressing_rooms = dressing_rooms

    def run(self):
        try:
            request_time = time.time()
            self.dressing_rooms.requestRoom(self.customer_id)
            wait_time = time.time() - request_time

            usage_time = 0
            for _ in range(self.num_items):
                try_on_time = random.randint(1, 3)
                time.sleep(try_on_time / 10)  # Simulate faster runtime
                usage_time += try_on_time

            self.dressing_rooms.releaseRoom(self.customer_id)

            with self.dressing_rooms.lock:
                print("Customer {} completed in {} minutes with a wait of {:.2f} seconds.".format(
                    self.customer_id, usage_time, wait_time))

        except Exception as e:
            with self.dressing_rooms.lock:
                print("Error for customer {}: {}".format(self.customer_id, str(e)))


class Scenario:
    def __init__(self, num_rooms, num_customers):
        # Validate inputs for room and customer counts
        if not (1 <= num_rooms <= 50):
            raise ValueError("Number of rooms must be between 1 and 50.")
        if not (1 <= num_customers <= 100):
            raise ValueError("Number of customers must be between 1 and 100.")
        self.num_rooms = num_rooms
        self.num_customers = num_customers

    def run_scenario(self):
        print("Running scenario with {} rooms and {} customers...".format(self.num_rooms, self.num_customers))
        dressing_rooms = DressingRooms(self.num_rooms)
        customers = []

        for i in range(self.num_customers):
            num_items = random.randint(1, 6)  # Random items (1 to 6)
            customer = Customer(i + 1, num_items, dressing_rooms)
            customers.append(customer)

        for customer in customers:
            customer.start()

        for customer in customers:
            customer.join()

        print("Scenario with {} customers completed.".format(self.num_customers))


# Running Scenarios
if __name__ == "__main__":
    try:
        scenarios = [
            Scenario(num_rooms=3, num_customers=10),
            Scenario(num_rooms=5, num_customers=20),
            Scenario(num_rooms=5, num_customers=30),
        ]
        for i, scenario in enumerate(scenarios, start=1):
            print("\n--- Scenario {} ---".format(i))
            scenario.run_scenario()
    except ValueError as ve:
        print("Input Error: {}".format(ve))
    except Exception as e:
        print("Unexpected Error: {}".format(e))
