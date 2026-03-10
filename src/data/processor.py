# Before (assuming 'open_file' is a function that opens a file for processing)
for item in items:
    file = open_file(item)
    # Process the file
    file.close()  # Explicitly close the file

# After (using a context manager)
for item in items:
    with open_file(item) as file:
        # Process the file
        pass  # File is automatically closed here