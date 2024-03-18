import json

# Load JSON data from file
with open('E:\INZINT\Omaxe_work/4_ujjwal_data.json', 'r') as file:
    data = json.load(file)

# Initialize an empty list to store patterns
patterns_list = []

# Set batch size to control memory usage
batch_size = 1000
start_index = 0

# Use a while loop to iterate through the JSON data in batches
while start_index < len(data):
    end_index = min(start_index + batch_size, len(data))
    batch_data = data[start_index:end_index]
    
    # Extract patterns from the current batch
    for entry in batch_data:
        patterns_list.extend(entry['patterns'])

    start_index += batch_size

# Print the extracted patterns list
print(patterns_list)

# Save the extracted patterns list to a new JSON file
with open('extracted_patterns.json', 'w') as output_file:
    json.dump(patterns_list, output_file, indent=4)
