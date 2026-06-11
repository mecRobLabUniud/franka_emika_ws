import csv

### DEFINE CSV PATHS ###
# csv elements delimiter (e.g., ' ', ',', ';')
element_delimiter = ','
# path to setpoint csv file (input)
csv_file_path_in = '/franka/franka_ws/src/script_python/traiettorie/traiettorie_lorenzo/test_franka_pictures.csv'
# path to measurement csv file (output)
csv_file_path_out = '/franka/franka_ws/src/script_python/traj_data/traiettorie_lorenzo/test_franka_pictures.csv'
### END DEFINE CSV PATHS ###


with open(csv_file_path_in, "r") as csv_file:
        # create csv reader object
        csv_reader = csv.reader(csv_file, delimiter=element_delimiter)

        # skip the first row with headers
        # next(csv_reader)

        # loop through each row in the csv file
        for i, row in enumerate(csv_reader):
            # convert each element to a float and add the row to the list
            if i == 0: continue     # skip the header row
            data.append([float(i) for i in row])
    ### END READ DATA ###




### WRITE TO CSV ###
# Create headers for CSV
headers =['time [s]']
for i in range(1,7+1):
    pos_string = 'position J' + str(i) + ' [rad]'
    headers.append(pos_string)
for i in range(1,7+1):
    vel_string = 'velocity J' + str(i) + ' [rad/s]'
    headers.append(vel_string)
for i in range(1,7+1):
    tau_string = 'torque J' + str(i) + ' [Nm]'
    headers.append(tau_string)

if save_measurements:
    # Open the file in write mode and create a CSV writer object
    with open(csv_file_path_out, mode='w') as file:
        writer = csv.writer(file)

        # Write the header row to the CSV file
        writer.writerow(headers)

        # Loop through each row of the list and write it to the CSV file
        for row in measurements:
            writer.writerow(row)
    ### END WRITE TO CSV ###