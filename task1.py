import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths

# Load dataset C:\Users\user\Desktop\jagriti\Simulator_readings.csv
# Assuming the dataset is in CSV format for demonstration.
data = pd.read_csv('Simulator_readings.csv')
print(data.columns)

# Convert time from milliseconds to seconds
data['Time_sec'] = data['Time(ms)'] / 1000

# 1. Plotting FHR and UC graphs
plt.figure(figsize=(12, 6))

# Time vs FHR
plt.subplot(2, 1, 1)
plt.plot(data['Time_sec'], data['Fhr1(BPM)'], label='FHR (bpm)', color='blue')
plt.xlabel('Time (seconds)')
plt.ylabel('FHR (bpm)')
plt.title('Time vs FHR')
plt.grid(True)

# Time vs UC
plt.subplot(2, 1, 2)
plt.plot(data['Time_sec'], data['Uc(TOCO)'], label='UC (TOCO)', color='orange')
plt.xlabel('Time (seconds)')
plt.ylabel('UC (TOCO)')
plt.title('Time vs UC')
plt.grid(True)

plt.tight_layout()
plt.show()

# 2. FHR Analysis (Epoch-based)
# Define epoch length (3.75 seconds) and calculate the number of data points per epoch
epoch_length = 3.75  # seconds
samples_per_epoch = int(epoch_length * 4)  # 4 data points per second

# Calculate the number of epochs
num_epochs = len(data) // samples_per_epoch

# Initialize lists to store epoch-wise FHR averages and pulse intervals
avg_fhr_bpm = []
avg_fhr_pulse_interval = []

# Calculate averages for each epoch
for epoch in range(num_epochs):
    start_idx = epoch * samples_per_epoch
    end_idx = start_idx + samples_per_epoch
    epoch_fhr = data['Fhr1(BPM)'][start_idx:end_idx]
    
    avg_bpm = np.mean(epoch_fhr)
    avg_pulse_interval = 60000 / avg_bpm  # Pulse interval in milliseconds (60000 ms per minute)
    
    avg_fhr_bpm.append(avg_bpm)
    avg_fhr_pulse_interval.append(avg_pulse_interval)

# Display FHR analysis


data['Avg_FHR_BPM'] = np.repeat(avg_fhr_bpm, samples_per_epoch)[:len(data)]
data['Avg_Pulse_Interval_ms'] = np.repeat(avg_fhr_pulse_interval, samples_per_epoch)[:len(data)]

# Save the modified dataframe to a new CSV file
data.to_csv('Simulator_readings.csv', index=False)

print("FHR analysis saved to CSV file with new columns 'Avg_FHR_BPM' and 'Avg_Pulse_Interval_ms'.")


# 3. UC Peak Detection
# Perform peak detection on UC data
peaks, _ = find_peaks(data['Uc(TOCO)'], height=5)  # Adjust height threshold as necessary

# Calculate peak widths at half maximum
widths, width_heights, left_ips, right_ips = peak_widths(data['Uc(TOCO)'], peaks, rel_height=0.5)

# Convert widths from data points to seconds (each data point is 0.25 seconds)
peak_widths_sec = widths * 0.25

# Count peaks where the width is more than 30 seconds
wide_peaks_count = np.sum(peak_widths_sec > 30)

# Calculate the average duration of counted UC peaks
if wide_peaks_count > 0:
    avg_peak_duration = np.mean(peak_widths_sec[peak_widths_sec > 30])
else:
    avg_peak_duration = 0

# Display peak analysis
print(f"Number of peaks wider than 30 seconds: {wide_peaks_count}")
print(f"Average duration of wide UC peaks: {avg_peak_duration:.2f} seconds")

