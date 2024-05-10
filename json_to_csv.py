import json
import csv

# Specify the path to the JSON file
json_file_path = "team_users.json"

# Read JSON data from the file
with open(json_file_path, "r") as file:
    data = json.load(file)

# Extract required fields
csv_data = [["name", "username", "email"]]
for entry in data:
    name = entry.get("name", "")
    username = entry.get("username", "")
    email = entry.get("email", "")
    csv_data.append([name, username, email])

# Write data to CSV file
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print("CSV file generated successfully.")
