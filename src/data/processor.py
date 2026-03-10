import os

# Example of closing a file after reading
with open('data_file.txt', 'r') as file:
    data = file.read()
# The file is automatically closed here