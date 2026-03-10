# Before (simplified example of a potential issue)
def process_items(items):
    processed_data = []
    for item in items:
        # Processing logic
        processed_item = process_item(item)
        processed_data.append(processed_item)
    return processed_data

# After (modified to reduce memory leak)
def process_items(items):
    for item in items:
        # Processing logic
        process_item(item)
        # Ensure no references are held to processed items
    return None

# Example of using a context manager for resource handling
def process_item(item):
    with open('output.txt', 'a') as file:
        # Use the file
        file.write(str(item) + '\n')
    # The file is automatically closed here