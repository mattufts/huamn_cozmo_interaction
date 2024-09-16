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
file_data_texts = [# # Example data from the provided info.txt files (you would replace these with file reads)
# file_data_texts = [
    ''' JS8C6ZB52C
1725666124.6060157
Animate Eyes
MAZE NAME: B
hit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 9
inconsistent_cnt: 11
auto_cnt: 0
total_steps: 16
human_commands: 14
Status: Successfully completed the goal!
hit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 9
inconsistent_cnt: 11
auto_cnt: 0
total_steps: 16
human_commands: 14
end_health: 100
end_time: 1725666380.4885435
''',
    
    ''' 21OKU05A6S
1725665661.9267988
Animate Icons
MAZE NAME:  Ahit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 7
inconsistent_cnt: 11
auto_cnt: 0
total_steps: 14
human_commands: 12
end_health: 100
end_time: 1725665861.4933512
''',
    
    '''7K2XOXL64U
1725650772.7184544
Animate Icons
MAZE NAME:  BStatus: Robot failed (health = 0).
hit_wall_cnt: 0
hit_fire_cnt: 4
consistent_cnt: 11
inconsistent_cnt: 26
auto_cnt: 0
total_steps: 25
human_commands: 21
end_health: 20
end_time: 1725651202.5094192
 ''', 
    
    ''' JULJVJLRMY
1725650351.90299
Animate Eyes
MAZE NAME: A
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 8
inconsistent_cnt: 15
auto_cnt: 0
total_steps: 17
human_commands: 15
Status: Successfully completed the goal!
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 8
inconsistent_cnt: 15
auto_cnt: 0
total_steps: 17
human_commands: 15
end_health: 90
end_time: 1725650639.7671194
''',
   
   '''QGLJS7Z59N
1725648839.22754
Animate Eyes
MAZE NAME: B
hit_wall_cnt: 3
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 12
auto_cnt: 0
total_steps: 18
human_commands: 17
Status: Successfully completed the goal!
hit_wall_cnt: 3
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 12
auto_cnt: 0
total_steps: 18
human_commands: 17
end_health: 70
end_time: 1725649097.4341805
''', 
    
    ''' OT6DCG637D
1725648432.8997307
Animate Icons
MAZE NAME:  Ahit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 6
inconsistent_cnt: 14
auto_cnt: 0
total_steps: 16
human_commands: 11
end_health: 100
end_time: 1725648680.894953
''',
    
    ''' SBHTOE5ZRC
1725644940.4130304
Animate Icons
MAZE NAME:  Bhit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 9
inconsistent_cnt: 10
auto_cnt: 0
total_steps: 16
human_commands: 13
end_health: 90
end_time: 1725645193.29835
''', 
    
    '''0PDLGLUUZQ
1725644539.819977
Animate Eyes
MAZE NAME: A
hit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 3
inconsistent_cnt: 18
auto_cnt: 0
total_steps: 16
human_commands: 9
Status: Successfully completed the goal!
hit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 3
inconsistent_cnt: 18
auto_cnt: 0
total_steps: 16
human_commands: 9
end_health: 100
end_time: 1725644762.952817
 ''',
 '''STJ1AMSJKX
1725641351.6613069
Animate Eyes
MAZE NAME: B
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 8
auto_cnt: 0
total_steps: 16
human_commands: 15
Status: Successfully completed the goal!
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 8
auto_cnt: 0
total_steps: 16
human_commands: 15
end_health: 90
end_time: 1725641564.943999
''',
'''2W9H62MK7O
1725640440.5047982
Animate Icons
MAZE NAME BStatus: Robot failed (health = 0).
hit_wall_cnt: 2
hit_fire_cnt: 1
consistent_cnt: 14
inconsistent_cnt: 20
auto_cnt: 0
total_steps: 25
human_commands: 23
end_health: 60
end_time: 1725640875.334563
''',

''' TPZ2FFYHTN
1725638670.976825
Animate Icons
MAZE NAME BStatus: Robot failed (health = 0).
hit_wall_cnt: 2
hit_fire_cnt: 4
consistent_cnt: 3
inconsistent_cnt: 31
auto_cnt: 0
total_steps: 23
human_commands: 14
end_health: 0
end_time: 1725639092.3980699
''',

'''96M6ACQBWK
1725638005.339411
Animate Icons
MAZE NAME Ahit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 15
auto_cnt: 0
total_steps: 20
human_commands: 17
end_health: 100
end_time: 1725638311.4285374
''',

'''156X9L9JNO
1725637483.8807251
Animate Eyes
MAZE NAME: A
Status: Robot failed (too many moves).
hit_wall_cnt: 3
hit_fire_cnt: 0
consistent_cnt: 9
inconsistent_cnt: 31
auto_cnt: 0
total_steps: 25
human_commands: 23
end_health: 70
end_time: 1725637811.2101023
''',

''' AMT4QN8064
1725629966.9035172
Animate Eyes
MAZE NAME: A
Status: Robot failed (too many moves).
hit_wall_cnt: 0
hit_fire_cnt: 1
consistent_cnt: 13
inconsistent_cnt: 21
auto_cnt: 0
total_steps: 25
human_commands: 20
end_health: 80
end_time: 1725630291.2899168''',

''' AR4QRL3EW2
1725629456.0012975
Animate Icons
MAZE NAME Ahit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 9
inconsistent_cnt: 14
auto_cnt: 0
total_steps: 18
human_commands: 15
end_health: 100
end_time: 1725629718.8072662
''',
''' IWSI7JPNPN
1725589073.3913257
Animate Eyes
MAZE NAME: A
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 5
inconsistent_cnt: 20
auto_cnt: 2
total_steps: 17
human_commands: 9
Status: Successfully completed the goal!
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 5
inconsistent_cnt: 20
auto_cnt: 2
total_steps: 17
human_commands: 9
end_health: 80
end_time: 1725589378.9108088
''', 

'''  GA9YMCA3XT
1725587220.9442997
Animate Eyes
MAZE NAME: B
hit_wall_cnt: 1
hit_fire_cnt: 1
consistent_cnt: 8
inconsistent_cnt: 16
auto_cnt: 1
total_steps: 19
human_commands: 13
Status: Successfully completed the goal!
hit_wall_cnt: 1
hit_fire_cnt: 1
consistent_cnt: 8
inconsistent_cnt: 16
auto_cnt: 1
total_steps: 19
human_commands: 13
end_health: 70
end_time: 1725587469.8671327
''',

''' Z0JX2DRH06
1725586666.9615278
Animate Icons
MAZE NAME Ahit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 9
inconsistent_cnt: 25
auto_cnt: 0
total_steps: 23
human_commands: 18
end_health: 90
end_time: 1725586990.206155
''',
''' N0Q3RT9YT1
1725584628.3161137
Animate Icons
MAZE NAME Bhit_wall_cnt: 1
hit_fire_cnt: 1
consistent_cnt: 12
inconsistent_cnt: 21
auto_cnt: 0
total_steps: 24
human_commands: 22
end_health: 70
end_time: 1725585002.1211429
''',
''' UYYJ7R8DG6
1725584140.7028651
Animate Eyes
MAZE NAME: A
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 13
inconsistent_cnt: 10
auto_cnt: 0
total_steps: 19
human_commands: 18
Status: Successfully completed the goal!
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 13
inconsistent_cnt: 10
auto_cnt: 0
total_steps: 19
human_commands: 18
end_health: 80
end_time: 1725584402.9592714
''',
''' XYE78UU4PR
1725582946.901084
Animate Eyes
MAZE NAME: A
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 12
inconsistent_cnt: 6
auto_cnt: 0
total_steps: 16
human_commands: 15
Status: Successfully completed the goal!
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 12
inconsistent_cnt: 6
auto_cnt: 0
total_steps: 16
human_commands: 15
end_health: 90
end_time: 1725583244.9677408
''',
'''DDQU9Y7HOZ
1725582447.6438973
Animate Icons
MAZE NAME Bhit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 11
auto_cnt: 0
total_steps: 18
human_commands: 17
end_health: 90
end_time: 1725582747.7013698
''',
'''S0SLMYR3LJ
1725581577.2826722
Animate Icons
MAZE NAME Bhit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 5
inconsistent_cnt: 18
auto_cnt: 0
total_steps: 18
human_commands: 12
end_health: 100
end_time: 1725581851.38753
 ''',
'''X5JDIVQL2S
1725580890.452707
Animate Eyes
MAZE NAME: B
Status: Robot failed (too many moves).
hit_wall_cnt: 3
hit_fire_cnt: 0
consistent_cnt: 5
inconsistent_cnt: 36
auto_cnt: 1
total_steps: 25
human_commands: 16
end_health: 70
end_time: 1725581212.0274308
 ''',
''' NSB69P0T7L
1725579360.1918066
Animate Eyes
MAZE NAME: A
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 7
auto_cnt: 0
total_steps: 16
human_commands: 14
Status: Successfully completed the goal!
hit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 11
inconsistent_cnt: 7
auto_cnt: 0
total_steps: 16
human_commands: 14
end_health: 90
end_time: 1725579606.7208803
''',
''' EPHSLYTUY8
1725578634.220484
Animate Icons
MAZE NAME BStatus: Robot failed (health = 0).
hit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 13
inconsistent_cnt: 22
auto_cnt: 0
total_steps: 25
human_commands: 22
end_health: 100
end_time: 1725579044.2912173
''',
''' 93AXV8MMF8
1725576997.6946788
Animate Eyes
MAZE NAME: A
hit_wall_cnt: 1
hit_fire_cnt: 2
consistent_cnt: 9
inconsistent_cnt: 19
auto_cnt: 0
total_steps: 21
human_commands: 17
Status: Successfully completed the goal!
hit_wall_cnt: 1
hit_fire_cnt: 2
consistent_cnt: 9
inconsistent_cnt: 19
auto_cnt: 0
total_steps: 21
human_commands: 17
end_health: 50
end_time: 1725577307.3942807
''',
''' NIJCA67K5C
1725576274.7046144
Animate Icons
MAZE NAME Bhit_wall_cnt: 8
hit_fire_cnt: 0
consistent_cnt: 3
inconsistent_cnt: 36
auto_cnt: 1
total_steps: 22
human_commands: 8
end_health: 20
end_time: 1725576576.7381575
Status: Manually Quit by User
hit_wall_cnt: 8
hit_fire_cnt: 0
consistent_cnt: 3
inconsistent_cnt: 36
auto_cnt: 1
total_steps: 22
human_commands: 8
end_health: 20
end_time: 1725576576.7382448
''',
''' TKD9V8ZAFM
1725574523.136475
Animate Icons
MAZE NAME BStatus: Robot failed (health = 0).
hit_wall_cnt: 0
hit_fire_cnt: 2
consistent_cnt: 10
inconsistent_cnt: 24
auto_cnt: 0
total_steps: 25
human_commands: 18
end_health: 60
end_time: 1725574948.0724611
''',
''' VRSRPVJWPF
1725573958.4550433
Animate Eyes
MAZE NAME: A
Status: Robot failed (too many moves).
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 10
inconsistent_cnt: 29
auto_cnt: 0
total_steps: 25
human_commands: 24
end_health: 80
end_time: 1725574287.8551762
''',
'''H0084S2IRF
1725573124.2942681
Animate Eyes
MAZE NAME: A
Status: Robot failed (too many moves).
hit_wall_cnt: 1
hit_fire_cnt: 1
consistent_cnt: 7
inconsistent_cnt: 33
auto_cnt: 0
total_steps: 25
human_commands: 19
end_health: 70
end_time: 1725573459.0498068
 ''',
''' 372IQ1UCLT
1725569518.229348
Animate Eyes
MAZE NAME: B
hit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 10
inconsistent_cnt: 11
auto_cnt: 0
total_steps: 16
human_commands: 15
Status: Successfully completed the goal!
hit_wall_cnt: 0
hit_fire_cnt: 0
consistent_cnt: 10
inconsistent_cnt: 11
auto_cnt: 0
total_steps: 16
human_commands: 15
end_health: 100
end_time: 1725569741.2064235
''',
''' TLY7619J8U
1725569136.199157
Animate Icons
MAZE NAME BStatus: Robot failed (health = 0).
hit_wall_cnt: 0
hit_fire_cnt: 5
consistent_cnt: 0
inconsistent_cnt: 8
auto_cnt: 0
total_steps: 8
human_commands: 0
end_health: 0
end_time: 1725569320.0874648
''',
''' DIFEBR35CN
1725557548.6344967
Animate Icons
MAZE NAME AStatus: Robot failed (health = 0).
hit_wall_cnt: 0
hit_fire_cnt: 5
consistent_cnt: 2
inconsistent_cnt: 23
auto_cnt: 1
total_steps: 15
human_commands: 4
end_health: 0
end_time: 1725557773.7802942
''',
''' NY0XLHM6NP
1725556511.6754315
Animate Eyes
MAZE NAME: B
Status: Robot failed (health = 0).
hit_wall_cnt: 6
hit_fire_cnt: 2
consistent_cnt: 12
inconsistent_cnt: 27
auto_cnt: 1
total_steps: 27
human_commands: 21
end_health: 0
end_time: 1725556929.8393192
''',
'''RJGPC0XL4U
1725552384.149268
Animate Icons
MAZE NAME Ahit_wall_cnt: 2
hit_fire_cnt: 1
consistent_cnt: 24
inconsistent_cnt: 46
auto_cnt: 0
total_steps: 51
human_commands: 44
end_health: 60
end_time: 1725553154.7707396
''',
'''KCJ99IVOXO
1725489085.6281893
Animate Icons
MAZE NAME AStatus: Robot failed (health = 0).
hit_wall_cnt: 0
hit_fire_cnt: 5
consistent_cnt: 2
inconsistent_cnt: 10
auto_cnt: 0
total_steps: 10
human_commands: 3
end_health: 0
end_time: 1725489292.9234874
''',
''' HU87ADTCID
1725488397.9291842
Animate Eyes
MAZE NAME: B
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 13
inconsistent_cnt: 18
auto_cnt: 0
total_steps: 23
human_commands: 22
Status: Successfully completed the goal!
hit_wall_cnt: 2
hit_fire_cnt: 0
consistent_cnt: 13
inconsistent_cnt: 18
auto_cnt: 0
total_steps: 23
human_commands: 22
end_health: 80
end_time: 1725488902.8510838
''',
''' AO6ZCS03RV
1725487225.2654407
Animate Eyes
MAZE NAME: B
hit_wall_cnt: 2
hit_fire_cnt: 3
consistent_cnt: 5
inconsistent_cnt: 41
auto_cnt: 2
total_steps: 27
human_commands: 20
end_health: 20
end_time: 1725487608.7822874
Status: Manually Quit by User
hit_wall_cnt: 2
hit_fire_cnt: 3
consistent_cnt: 5
inconsistent_cnt: 41
auto_cnt: 2
total_steps: 27
human_commands: 20
end_health: 20
end_time: 1725487608.8072865
''',
''' 6IT1THP68Y
1725486256.6130497
Animate Icons
MAZE NAME Ahit_wall_cnt: 1
hit_fire_cnt: 0
consistent_cnt: 0
inconsistent_cnt: 23
auto_cnt: 5
total_steps: 15
human_commands: 5
end_health: 90
end_time: 1725486418.457066
'''
    
]

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