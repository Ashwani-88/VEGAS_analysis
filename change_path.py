import os
import sys

# Check if the user provided an argument
if len(sys.argv) != 2:
    print("Usage: python change_path.py <new_path>")
    sys.exit(1)

new_path = sys.argv[1]

# Iterate through all text files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        with open(filename, 'r') as file:
            content = file.read()

        # Replace occurrences of "/yourpath" with the new path
        content = content.replace("/yourPath", new_path)

        with open(filename, 'w') as file:
            file.write(content)

        print(f"Updated: {filename}")

print("Replaced path in all the templates.")
