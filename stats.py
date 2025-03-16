import time


class Stats:
    def __init__(self):
        self.total_steps = 0  # Total steps taken in the game
        self.step_runs = []  # List to store step runs before each meeting
        self.run_times = []  # Store the time duration of each game
        self.start_time = None  # Track when the game starts

    def increment_steps(self): #increase the step counter
          self.total_steps += 1

    def record_step_run(self, steps): # records the number of steps before players meet
     self.step_runs.append(steps)

    def get_total_steps(self): # returnes total number of steps
        return self.total_steps

    def start_timer(self): # starts timer
        if self.start_time is None:
            self.start_time = time.time()


    def stop_timer(self): #stops timer and stores time
        if self.start_time:
            elapsed_time = round(time.time() - self.start_time, 2)  # Calculate duration
            self.run_times.append(elapsed_time)

            self.start_time = None  # Reset timer


    def get_longest_run(self): #return longest run
        return max(self.run_times, default=0)

    def get_shortest_run(self): #return shortest times
        return min(self.run_times, default=0)

    def get_average_run_time(self): #average run time
        if not self.run_times:
            return 0
        return round(sum(self.run_times) / len(self.run_times), 2)

    def save_stats(self, filename="game_stats.txt"):

        with open(filename, "w") as file:
            file.write(f"Total Runs: {len(self.run_times)}\n")
            file.write(f"Longest Run: {self.get_longest_run()} seconds\n")
            file.write(f"Shortest Run: {self.get_shortest_run()} seconds\n")
            file.write(f"Average Run Time: {self.get_average_run_time()} seconds\n")
