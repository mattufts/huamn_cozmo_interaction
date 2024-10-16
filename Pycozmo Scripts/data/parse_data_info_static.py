import pandas as pd

# Define the target CSV format columns
columns = [
    "Session ID", "Start Time", "Mode", "Maze Name", "Wall Hits", "Fire Hits", 
    "Consistent Commands", "Inconsistent Commands", "Autonomous Commands", 
    "Total Steps", "Human Commands", "End Health", "End Time", "Status"
]

# Initialize an empty DataFrame to store the extracted information
df_combined = pd.DataFrame(columns=columns)

# Function to extract data from each info.txt file
def extract_info_from_file(text):
    lines = text.split("\n")
    
    # Initialize default values
    data = {
        "Session ID": None,
        "Start Time": None,
        "Mode": None,
        "Maze Name": None,
        "Wall Hits": 0,
        "Fire Hits": 0,
        "Consistent Commands": 0,
        "Inconsistent Commands": 0,
        "Autonomous Commands": 0,
        "Total Steps": 0,
        "Human Commands": 0,
        "End Health": None,
        "End Time": None,
        "Status": None
    }
    
    consistent_cnt_value = None
    inconsistent_cnt_value = None
    
    for line in lines:
        line = line.strip()
        
        # Handle "MAZE NAME" when combined with other fields (e.g., hit_wall_cnt or Status)
        if "MAZE NAME" in line:
            if "hit_wall_cnt" in line:
                maze_hit_split = line.split("hit_wall_cnt:")
                data["Maze Name"] = maze_hit_split[0].replace("MAZE NAME", "").strip()
                data["Wall Hits"] = int(maze_hit_split[1].strip())
            elif "Status" in line:
                maze_status_split = line.split("Status:")
                data["Maze Name"] = maze_status_split[0].replace("MAZE NAME", "").strip()
                data["Status"] = maze_status_split[1].strip()
            else:
                # Handle cases where MAZE NAME is alone
                data["Maze Name"] = line.split(":")[1].strip()

        # Process all other normal lines
        elif "hit_wall_cnt" in line:
            data["Wall Hits"] = int(line.split(":")[1].strip())
        elif "hit_fire_cnt" in line:
            data["Fire Hits"] = int(line.split(":")[1].strip())
        elif "consistent_cnt" in line and "inconsistent_cnt" not in line:
            # Ensure consistent commands are correctly assigned
            consistent_cnt_value = int(line.split(":")[1].strip())
            print(f"Parsed consistent_cnt: {consistent_cnt_value}")  # Log the parsed value
        elif "inconsistent_cnt" in line:
            # Ensure inconsistent commands are correctly assigned
            inconsistent_cnt_value = int(line.split(":")[1].strip())
            print(f"Parsed inconsistent_cnt: {inconsistent_cnt_value}")  # Log the parsed value
        elif "auto_cnt" in line:
            data["Autonomous Commands"] = int(line.split(":")[1].strip())
        elif "total_steps" in line:
            data["Total Steps"] = int(line.split(":")[1].strip())
        elif "human_commands" in line:
            data["Human Commands"] = int(line.split(":")[1].strip())
        elif "end_health" in line:
            data["End Health"] = int(line.split(":")[1].strip())
        elif "end_time" in line:
            data["End Time"] = float(line.split(":")[1].strip())
        elif "Status" in line:
            data["Status"] = line.split(":")[1].strip()
        elif len(line.strip()) == 10:  # Assuming the first line is the Session ID
            data["Session ID"] = line.strip()
        elif line.strip().replace('.', '', 1).isdigit() and len(line.strip()) > 10:
            data["Start Time"] = float(line.strip())
        elif "Static" in line or "Animate" in line:
            data["Mode"] = line.strip()

    # Assign consistent and inconsistent values after parsing
    if consistent_cnt_value is not None:
        data["Consistent Commands"] = consistent_cnt_value
        print(f"Assigned consistent_cnt: {consistent_cnt_value}")  # Log the assignment
    if inconsistent_cnt_value is not None:
        data["Inconsistent Commands"] = inconsistent_cnt_value
        print(f"Assigned inconsistent_cnt: {inconsistent_cnt_value}")  # Log the assignment

    return data

# Example data from the provided info.txt files (you would replace these with file reads)
file_data_texts = [
    '''967I7E8IHU
1726099790.0013268
Static Icons
MAZE NAME: A
Status: Robot failed (health = 0).
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 13
inconsistent_cnt: 22
auto_cnt: 0
Total Steps: 25
"human_commands: 22
end_health: 90
end_time: 1726100168.5206048
''',
    '''4MSQ8LECFU
1726100636.0051637
Static Eyes
MAZE NAME: BStatus: Robot failed (health = 0).
hit_wall_cnt: 4
hit_fire_cnt: 1
consistent_cnt: 9
inconsistent_cnt: 33
auto_cnt: 0
Total Steps: 25
"human_commands: 25
end_health: 40
end_time: 1726101007.9941194
''',
    ''' JFQDP27VI7
1726101370.1643867
Static Eyes
MAZE NAME: Bhit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 13
inconsistent_cnt: 17
auto_cnt: 0
total_steps: 23
human_commands: 22
end_health: 80
end_time: 1726101687.111198
''',
    '''EU2WQBCGB9
1726102079.5556598
Static Icons
MAZE NAME: Ahit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 3
inconsistent_cnt: 14
auto_cnt: 0
total_steps: 14
human_commands: 8
end_health: 100
end_time: 1726102265.218285
''',
    '''CS6NY4XR8I
1726108318.0919755
Static Eyes
MAZE NAME: Bhit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 12
inconsistent_cnt: 16
auto_cnt: 0
total_steps: 21
human_commands: 20
end_health: 80
end_time: 1726108606.7861571
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 12
inconsistent_cnt: 16
auto_cnt: 0
total_steps: 21
"human_commands: 20
end_health: 80
end_time: 1726108622.7213583
''',
    ''' 2P42HR7XK1
1726109670.5402162
Static Eyes
MAZE NAME: Bhit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 13
auto_cnt: 0
total_steps: 20
human_commands: 16
end_health: 90
end_time: 1726109972.1514297
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 13
auto_cnt: 0
total_steps: 20
"human_commands: 16
end_health: 90
end_time: 1726109974.541043
''',
    '''FY1I8O7OFC
1726110308.6627278
Static Icons
MAZE NAME: Ahit_wall_cnt: 0
hit_fire_cnt: 1
consistent_cnt: 10
inconsistent_cnt: 18
auto_cnt: 0
total_steps: 21
human_commands: 18
end_health: 80
end_time: 1726110587.4861777
hit_wall_cnt: 0
hit_fire_cnt: 1
consistent_cnt: 10
inconsistent_cnt: 18
auto_cnt: 0
total_steps: 21
"human_commands: 18
end_health: 80
end_time: 1726110590.376087
''',
    '''OC3BQX9KR2
1726111136.1749873
Static Icons
MAZE NAME: Ahit_wall_cnt: 0
hit_fire_cnt: 1
consistent_cnt: 9
inconsistent_cnt: 16
auto_cnt: 0
total_steps: 19
human_commands: 17
end_health: 80
end_time: 1726111400.3785124
hit_wall_cnt: 0
hit_fire_cnt: 1
consistent_cnt: 9
inconsistent_cnt: 16
auto_cnt: 0
total_steps: 19
"human_commands: 17
end_health: 80
end_time: 1726111412.6561775
''',
    '''SVBYT6Z815
1726161212.730418
Static Eyes
MAZE NAME: Ahit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 14
inconsistent_cnt: 18
auto_cnt: 0
total_steps: 25
human_commands: 23
end_health: 80
end_time: 1726161573.3642862
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 14
inconsistent_cnt: 18
auto_cnt: 0
total_steps: 25
"human_commands: 23
end_health: 80
end_time: 1726161646.4483519
''',
    '''ON690BSOP5
1726161693.7446792
Static Icons
MAZE NAME: BStatus: Robot failed (health = 0).
hit_wall_cnt: 1
hit_fire_cnt: 1
consistent_cnt: 14
inconsistent_cnt: 21
auto_cnt: 0
total_steps: 25
"human_commands: 24
end_health: 70
end_time: 1726162070.4589791
''',
    '''JVI8SYCRRW
1726168385.6463175
Static Icons
MAZE NAME: Bhit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 8
inconsistent_cnt: 13
auto_cnt: 0
total_steps: 17
human_commands: 13
end_health: 80
end_time: 1726168650.9206548
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 8
inconsistent_cnt: 13
auto_cnt: 0
total_steps: 17
"human_commands: 13
end_health: 80
end_time: 1726168769.2306392
''',
'''   TH0SVNEAG4
1726169029.7742257
Static Eyes
MAZE NAME: Ahit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 8
inconsistent_cnt: 9
auto_cnt: 0
total_steps: 14
human_commands: 12
end_health: 100
end_time: 1726169233.770535
 ''',
'''   YHQZ4K0HBK
1726170676.882487
Static Eyes
MAZE NAME: Ahit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 3
inconsistent_cnt: 8
auto_cnt: 0
total_steps: 8
human_commands: 7
end_health: 100
end_time: 1726170783.202128
 ''',
'''  E0MU5Y01SX
1726171091.1626568
Static Icons
MAZE NAME: Bhit_wall_cnt: 0
hit_fire_cnt: 1
consistent_cnt: 9
inconsistent_cnt: 19
auto_cnt: 0
total_steps: 21
human_commands: 18
end_health: 80
end_time: 1726171439.8615758
hit_wall_cnt: 0
hit_fire_cnt: 1
consistent_cnt: 9
inconsistent_cnt: 19
auto_cnt: 0
total_steps: 21
"human_commands: 18
end_health: 80
end_time: 1726171492.3956594
 ''',
'''  53METRPKNR
1726172037.7082877
Static Icons
MAZE NAME: Ahit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 14
inconsistent_cnt: 12
auto_cnt: 0
total_steps: 21
human_commands: 20
end_health: 80
end_time: 1726172375.0861158
  ''',
'''    XGPA4KZMMN
1726172601.8040807
Static Eyes
MAZE NAME: Bhit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 10
inconsistent_cnt: 9
auto_cnt: 0
total_steps: 16
human_commands: 14
end_health: 90
end_time: 1726172831.3048735
''',
'''  JEH27LINK6
1726175372.8676496
Static Icons
MAZE NAME: Bhit_wall_cnt: 0
hit_fire_cnt: 1
consistent_cnt: 11
inconsistent_cnt: 23
auto_cnt: 0
total_steps: 23
human_commands: 20
end_health: 80
end_time: 1726175691.7822096
hit_wall_cnt: 0
hit_fire_cnt: 1
consistent_cnt: 11
inconsistent_cnt: 23
auto_cnt: 0
total_steps: 23
"human_commands: 20
end_health: 80
end_time: 1726175721.3794818
 ''',
'''  5IVHGQOR4X
1726176005.3158927
Static Eyes
MAZE NAME: BStatus: Robot failed (health = 0).
hit_wall_cnt: 3
hit_fire_cnt: 2
consistent_cnt: 2
inconsistent_cnt: 42
auto_cnt: 6
total_steps: 25
"human_commands: 13
end_health: 30
end_time: 1726176289.9186556
 ''',
'''  KZEKH3NU6Q
1726178107.9425788
Static Icons
MAZE NAME: AStatus: Robot failed (health = 0).
hit_wall_cnt: 1
hit_fire_cnt: 1
consistent_cnt: 12
inconsistent_cnt: 25
auto_cnt: 0
total_steps: 25
"human_commands: 25
end_health: 70
end_time: 1726178473.8135216
  ''',
''' 1UHMI27927
1726181159.6410832
Static Eyes
MAZE NAME: Ahit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 12
inconsistent_cnt: 6
auto_cnt: 0
total_steps: 16
human_commands: 15
end_health: 90
end_time: 1726181400.755383
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 12
inconsistent_cnt: 6
auto_cnt: 0
total_steps: 16
"human_commands: 15
end_health: 90
end_time: 1726181464.308134
 ''',
''' 2C1LMEZT8A
1726181679.9851594
Static Icons
MAZE NAME: BStatus: Robot failed (health = 0).
hit_wall_cnt: 0
hit_fire_cnt: 2
consistent_cnt: 11
inconsistent_cnt: 25
auto_cnt: 0
total_steps: 25
"human_commands: 22
end_health: 60
end_time: 1726182078.8113182
 ''',
''' 1SELDIASR7
1726184340.687292
Static Icons
MAZE NAME: AStatus: Robot failed (health = 0).
hit_wall_cnt: 3
hit_fire_cnt: 0
consistent_cnt: 8
inconsistent_cnt: 33
auto_cnt: 0
total_steps: 25
"human_commands: 24
end_health: 70
end_time: 1726184706.0856712
''',
''' FT4T5HWRD0
1726185159.3092794
Static Eyes
MAZE NAME: BStatus: Robot failed (health = 0).
hit_wall_cnt: 3
hit_fire_cnt: 1
consistent_cnt: 8
inconsistent_cnt: 30
auto_cnt: 0
total_steps: 25
"human_commands: 23
end_health: 50
end_time: 1726185536.4380136
   ''',
'''   QP5EO7V1RL
1726165288.7307022
Static Eyes
MAZE NAME: Ahit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 3
inconsistent_cnt: 36
auto_cnt: 1
total_steps: 23
human_commands: 10
end_health: 80
end_time: 1726165539.258386
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 3
inconsistent_cnt: 36
auto_cnt: 1
total_steps: 23
"human_commands: 10
end_health: 80
end_time: 1726165543.420595
 ''',
'''   QE5X1GYL7R
1726177919.000036
Static Eyes
MAZE NAME: Ahit_wall_cnt: 3
hit_fire_cnt: 0
consistent_cnt: 10
inconsistent_cnt: 12
auto_cnt: 0
total_steps: 18
human_commands: 15
end_health: 70
end_time: 1726178229.172032
hit_wall_cnt: 3
hit_fire_cnt: 0
consistent_cnt: 10
inconsistent_cnt: 12
auto_cnt: 0
total_steps: 18
"human_commands: 15
end_health: 70
end_time: 1726178288.675549
 ''',
''' JRRQMT8I9L
1726165870.558199
Static Icons
MAZE NAME: AStatus: Robot failed (health = 0).
hit_wall_cnt: 3
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 25
auto_cnt: 0
total_steps: 25
"human_commands: 22
end_health: 70
end_time: 1726166266.867674
   ''',
'''  SGVOCFZ6EX
1726188964.4294133
Static Icons
MAZE NAME: AStatus: Robot failed (health = 0).
hit_wall_cnt: 6
hit_fire_cnt: 0
consistent_cnt: 12
inconsistent_cnt: 24
auto_cnt: 0
total_steps: 25
"human_commands: 23
end_health: 40
end_time: 1726189367.5628326
  ''',
'''  LNTPJCPQ3J
1726189593.8236551
Static Eyes
MAZE NAME: BStatus: Robot failed (health = 0).
hit_wall_cnt: 3
hit_fire_cnt: 1
consistent_cnt: 0
inconsistent_cnt: 50
auto_cnt: 0
total_steps: 25
"human_commands: 25
end_health: 50
end_time: 1726189807.191954
  ''' ]
# Process each of the example data and append to the final DataFrame
for file_content in file_data_texts:
    extracted_data = extract_info_from_file(file_content)
    df_combined = pd.concat([df_combined, pd.DataFrame([extracted_data])], ignore_index=True)

# Sort the DataFrame by 'Start Time' in descending order
df_combined_sorted = df_combined.sort_values(by="Start Time", ascending=False)

# Save the combined and sorted data to a CSV file
output_csv_path = "desired_data_format_combined_fixed.csv"
df_combined_sorted.to_csv(output_csv_path, index=False)

print(f"Data successfully saved to {output_csv_path} in descending order by Start Time")
