import os
import csv

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    response_times = []
    step = None
    respond_time = None
    indicated_action = None
    
    # Loop through each line in the file
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        
        print(f"Processing line: {line}")  # Debugging statement

        # Look for step, response time, and indicated action
        if "current_step" in line:
            step = int(line.split(": ")[1])  # Extract Step number
        elif "respond_time" in line:
            respond_time = float(line.split(": ")[1])  # Extract Response Time
        elif "indicated next action" in line:
            action_value = line.split(": ")[1]
            if action_value.isdigit():
                indicated_action = int(action_value)  # Extract Indicated Action if it's a valid number
            else:
                print(f"Skipping invalid action: {action_value}")  # Skip invalid action
                indicated_action = None

        # When all three values are found, add them to the list
        if step is not None and respond_time is not None and indicated_action is not None:
            response_times.append((step, respond_time, indicated_action))
            step = None
            respond_time = None
            indicated_action = None
    
    # If no valid lines were processed, log and return None
    if not response_times:
        print(f"No valid data found in file: {file_path}. The file might not contain the expected Step, Response Time, or Indicated Action.")
        return None

    # Calculate necessary statistics
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
        # Skip hidden files (those starting with ".")
        if filename.startswith(".") or not filename.endswith("_traj.txt"):
            print(f"Skipping hidden or irrelevant file: {filename}")  # Debugging statement
            continue
        
        participant_id = filename.split('_traj.txt')[0]
        file_path = os.path.join(input_folder, filename)
        processed_data = process_file(file_path)
        
        # Only append if valid data is returned
        if processed_data:
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
