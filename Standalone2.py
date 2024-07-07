import simpy
import random
import matplotlib.pyplot as plt
from tabulate import tabulate  # Import tabulate for table formatting

# Parameters
NUM_JOBS = 100
ARRIVAL_MIN = 60
ARRIVAL_MAX = 180
SERVICE_MIN = 120
SERVICE_MAX = 300

# Function to simulate jobs with a given number of servers
def simulate_jobs(num_servers):
    # Data collection
    arrival_times = []
    service_times = []
    delay_times = []
    departure_times = []

    def job(env, name, servers):
        arrival_time = env.now
        arrival_times.append(arrival_time)

        # Request one of the servers
        with servers.request() as request:
            yield request
            delay_time = env.now - arrival_time
            delay_times.append(delay_time)

            service_time = random.randint(SERVICE_MIN, SERVICE_MAX)
            service_times.append(service_time)

            yield env.timeout(service_time)
            departure_time = env.now
            departure_times.append(departure_time)

    def setup(env, num_jobs, num_servers):
        servers = simpy.Resource(env, capacity=num_servers)
        for i in range(num_jobs):
            interarrival_time = random.randint(ARRIVAL_MIN, ARRIVAL_MAX)
            yield env.timeout(interarrival_time)
            env.process(job(env, f'Job {i}', servers))

    # Simulation environment
    env = simpy.Environment()
    env.process(setup(env, NUM_JOBS, num_servers))
    env.run()

    # Compute average delay
    average_delay = sum(delay_times) / len(delay_times)

    # Total time to finish all jobs
    total_time = max(departure_times)

    # Return results
    return arrival_times, delay_times, service_times, departure_times, average_delay, total_time


# Simulate with 1 server
arrival_times_1, delay_times_1, service_times_1, departure_times_1, avg_delay_1, total_time_1 = simulate_jobs(1)

# Simulate with 2 servers
arrival_times_2, delay_times_2, service_times_2, departure_times_2, avg_delay_2, total_time_2 = simulate_jobs(2)

# Print results for 1 server
print("Results for 1 server:")
print(f'Average Delay: {avg_delay_1:.2f} time units')
print(f'Total Time to Finish All Jobs: {total_time_1:.2f} time units')

# Print results for 2 servers
print("\nResults for 2 servers:")
print(f'Average Delay: {avg_delay_2:.2f} time units')
print(f'Total Time to Finish All Jobs: {total_time_2:.2f} time units')

# Format job details into a table using tabulate
def format_job_table(arrival_times, delay_times, service_times, departure_times):
    job_details = []
    for i in range(NUM_JOBS):
        job_details.append([i + 1, arrival_times[i], delay_times[i], service_times[i], departure_times[i]])

    headers = ["Job", "Arrival Time", "Delay Time", "Service Time", "Departure Time"]
    return tabulate(job_details, headers=headers, tablefmt="grid")

# Print job details table for 1 server
print("\nJob Details for 1 server:")
print(format_job_table(arrival_times_1, delay_times_1, service_times_1, departure_times_1))

# Print job details table for 2 servers
print("\nJob Details for 2 servers:")
print(format_job_table(arrival_times_2, delay_times_2, service_times_2, departure_times_2))

# Gantt Chart for 1 server
fig, (gnt1, gnt2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

gnt1.set_ylim(0, NUM_JOBS + 1)
gnt1.set_xlim(0, max(total_time_1, total_time_2) + 100)
gnt1.set_xlabel('Time units')
gnt1.set_ylabel('Job')
gnt1.set_title('Gantt Chart of Jobs (1 server)')
for i in range(NUM_JOBS):
    gnt1.broken_barh([(arrival_times_1[i], service_times_1[i])], (i + 1, 0.8), facecolors=('tab:blue'))

# Gantt Chart for 2 servers
gnt2.set_ylim(0, NUM_JOBS + 1)
gnt2.set_xlim(0, max(total_time_1, total_time_2) + 100)
gnt2.set_xlabel('Time units')
gnt2.set_ylabel('Job')
gnt2.set_title('Gantt Chart of Jobs (2 servers)')
for i in range(NUM_JOBS):
    gnt2.broken_barh([(arrival_times_2[i], service_times_2[i])], (i + 1, 0.8), facecolors=('tab:orange'))

plt.tight_layout()
plt.show()

# Delay per request chart for 1 server
plt.figure(figsize=(10, 4))
plt.bar(range(NUM_JOBS), delay_times_1, color='tab:blue')
plt.xlabel('Job')
plt.ylabel('Delay Time (units)')
plt.title('Delay Time per Request (1 server)')
plt.show()

# Delay per request chart for 2 servers
plt.figure(figsize=(10, 4))
plt.bar(range(NUM_JOBS), delay_times_2, color='tab:orange')
plt.xlabel('Job')
plt.ylabel('Delay Time (units)')
plt.title('Delay Time per Request (2 servers)')
plt.show()
