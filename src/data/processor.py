# Inside the processing loop
for item in items:
    # Process the item
    processed_item = process_item(item)
    
    # Use the processed item
    # ...
    
    # Explicitly delete the object
    del processed_item