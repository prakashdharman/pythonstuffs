import subprocess
import time

def collect_pstack(pid, samples, interval):
    filename = f"pstack_pid_{pid}.txt"
    with open(filename, "w") as f:
        for i in range(samples):
            pstack_output = subprocess.run(["pstack", str(pid)], capture_output=True, text=True)
            f.write(f"Sample {i+1}:\n{pstack_output.stdout}\n")
            time.sleep(interval)

if __name__ == "__main__":
    process_id = 1234  # Replace with your process ID
    samples_count = 15000
    sampling_interval = 1  # in seconds

    collect_pstack(process_id, samples_count, sampling_interval)
