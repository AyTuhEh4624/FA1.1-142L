import simpy
import matplotlib.pyplot as plt

# Define the arrival and service times
arrival_times = [15, 47, 71, 111, 123, 142, 166, 266, 310, 320]
service_times = [43, 36, 34, 30, 38, 40, 31, 29, 36, 30]


# Define a job process
def job(env, name, server, arrival_time, service_time, delays, services, departures):
    yield env.timeout(arrival_time - env.now)  # Wait until arrival time
    arrival = env.now  # Job arrives
    with server.request() as request:
        yield request  # Request a server
        wait = env.now - arrival  # Calculate delay time
        delays.append(wait)
        services.append(service_time)
        yield env.timeout(service_time)  # Service time
        departures.append(env.now)  # Record departure time


# Simulation setup
def simulate_queue(arrival_times, service_times):
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)  # Single server
    delays, services, departures = [], [], []

    for i, arrival_time in enumerate(arrival_times):
        env.process(job(env, f"Job {i + 1}", server, arrival_time, service_times[i], delays, services, departures))

    env.run()

    return delays, services, departures


# Run the simulation
delays, services, departures = simulate_queue(arrival_times, service_times)

# Calculate the arrival times and the departure times
arrivals = arrival_times
departure_times = departures

# Print the results
print("Job\tArrival\tDelay\tService\tDeparture")
for i in range(len(arrival_times)):
    print(f"{i + 1}\t{arrivals[i]}\t\t{delays[i]}\t\t{services[i]}\t\t{departure_times[i]}")

# Calculate averages
average_delay = sum(delays) / len(delays)
average_service_time = sum(services) / len(services)
average_waiting_time = average_delay + average_service_time

print(f"\nAverage Delay Time: {average_delay:.2f}")
print(f"Average Service Time: {average_service_time:.2f}")
print(f"Average Waiting Time: {average_waiting_time:.2f}")

# Plot the Gantt chart
plt.figure(figsize=(10, 6))
for i in range(len(arrival_times)):
    start_time = arrivals[i] + delays[i]
    plt.barh(i, services[i], left=start_time, edgecolor='black', color='skyblue')
    plt.text(start_time + services[i] / 2, i, f'Job {i + 1}', ha='center', va='center')

plt.yticks(range(len(arrival_times)), [f'Job {i + 1}' for i in range(len(arrival_times))])
plt.xlabel('Time')
plt.ylabel('Job')
plt.title('FIFO Queue Simulation Gantt Chart')
plt.grid(True)
plt.show()