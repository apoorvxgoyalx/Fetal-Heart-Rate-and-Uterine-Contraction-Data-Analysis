
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
