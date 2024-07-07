import simpy
import random
import matplotlib.pyplot as plt

# Parameters
NUM_JOBS = 100
ARRIVAL_MIN = 60
ARRIVAL_MAX = 180
SERVICE_MIN = 120
SERVICE_MAX = 300

# Data collection
arrival_times = []
service_times = []
delay_times = []
departure_times = []


def job(env, name, server):
    arrival_time = env.now
    arrival_times.append(arrival_time)

    with server.request() as request:
        yield request
        delay_time = env.now - arrival_time
        delay_times.append(delay_time)

        service_time = random.randint(SERVICE_MIN, SERVICE_MAX)
        service_times.append(service_time)

        yield env.timeout(service_time)
        departure_time = env.now
        departure_times.append(departure_time)


def setup(env, num_jobs):
    server = simpy.Resource(env, capacity=1)
    for i in range(num_jobs):
        interarrival_time = random.randint(ARRIVAL_MIN, ARRIVAL_MAX)
        yield env.timeout(interarrival_time)
        env.process(job(env, f'Job {i}', server))


# Simulation
env = simpy.Environment()
env.process(setup(env, NUM_JOBS))
env.run()

# Compute average delay
average_delay = sum(delay_times) / len(delay_times)

# Total time to finish all jobs
total_time = max(departure_times)

# Display results
print(f'Average Delay: {average_delay:.2f} time units')
print(f'Total Time to Finish All Jobs: {total_time:.2f} time units')
print("Job\tArrival Time\tDelay Time\t\tService Time\tDeparture Time")
for i in range(NUM_JOBS):
    print(f"{i + 1}\t\t{arrival_times[i]} \t\t{delay_times[i]}          \t{service_times[i]}\t\t\t{departure_times[i]}")


# Gantt Chart
fig, gnt = plt.subplots()
gnt.set_ylim(0, NUM_JOBS + 1)
gnt.set_xlim(0, total_time + 100)
gnt.set_xlabel('Time units')
gnt.set_ylabel('Job')

for i in range(NUM_JOBS):
    gnt.broken_barh([(arrival_times[i], service_times[i])], (i + 1, 0.8), facecolors=('tab:blue'))

plt.title('Gantt Chart of Jobs')
plt.show()

# Delay per request chart
plt.figure()
plt.bar(range(NUM_JOBS), delay_times)
plt.xlabel('Job')
plt.ylabel('Delay Time (units)')
plt.title('Delay Time per Request')
plt.show()


