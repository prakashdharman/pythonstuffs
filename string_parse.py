import re

input_string = "scheduler_nobody_bmghjhjhgjhgjasde_RMDjkshdkjfhsdjhfkjsdhfsdf_at_156773487687_12345_45ADFG56-C067-42F-8990-78AD9B6C1"

# Define the updated regular expression pattern
pattern = r"_at_(\d+\.\d+_\w+-\w+-\w+-\w+-\w+)"

# Use re.search to find the pattern in the string
match = re.search(pattern, input_string)

# Check if a match is found and extract the desired part
if match:
    result = match.group(1)
    print(result)
else:
    print("Pattern not found in the input string.")
