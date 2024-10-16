import os
import csv

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    response_times = []
    indicated_actions = []
    
    # Loop through each line in the file
    for line in lines:
        if line.strip():  # Check if the line is not empty
            print(f"Processing line: {line.strip()}")  # Debug: Print the line being processed
            try:
                parts = line.split(', ')  # Split the line by ", " to get parts
                step = int(parts[0].split(": ")[1])  # Extract Step number
                response_time = float(parts[1].split(": ")[1])  # Extract Response Time
                indicated_action = int(parts[2].split(": ")[1])  # Extract Indicated Action

                # Add the extracted values to the list
                response_times.append((step, response_time, indicated_action))

            except IndexError:
                # Handle any line that doesn't match the expected format
                print(f"Skipping malformed line: {line.strip()}")
            except ValueError:
                # Handle cases where conversion to int or float fails
                print(f"Skipping line with invalid data: {line.strip()}")

    # After processing all lines, calculate necessary statistics
    if response_times:
        longest_response_time = max(response_times, key=lambda x: x[1])
        shortest_response_time = min(response_times, key=lambda x: x[1])
        average_response_time = sum([x[1] for x in response_times]) / len(response_times)
        total_steps = response_times[-1][0]  # Last step in the file
    
        return {
            'average_response_time': average_response_time,
            'total_steps': total_steps,
            'shortest_response_time': shortest_response_time[1],
            'indicated_action_shortest': shortest_response_time[2],
            'longest_response_time': longest_response_time[1],
            'indicated_action_longest': longest_response_time[2],
        }
    else:
        print(f"No valid data found in file: {file_path}")
        return None

def save_to_csv(data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Participant ID', 'Average Response Time', 'Total Steps', 'Shortest Response Time', 
                         'Indicated Action at Shortest Response Time', 'Longest Response Time', 'Indicated Action at Longest Response Time'])
        for row in data:
            writer.writerow(row)

def main(input_folder, output_file):
    data = []
    for filename in os.listdir(input_folder):
        if filename.endswith("_traj.txt"):
            participant_id = filename.split('_traj.txt')[0]
            file_path = os.path.join(input_folder, filename)
            processed_data = process_file(file_path)
            data.append([
                participant_id,
                processed_data['average_response_time'],
                processed_data['total_steps'],
                processed_data['shortest_response_time'],
                processed_data['indicated_action_shortest'],
                processed_data['longest_response_time'],
                processed_data['indicated_action_longest'],
            ])
    
    save_to_csv(data, output_file)

# Example Usage:
input_folder = '.'
output_file = 'cozmo_trajectory_data.csv'
main(input_folder, output_file)
