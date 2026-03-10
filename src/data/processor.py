import gc

# Example within the processing loop
for item in items_to_process:
    # Create a new object for each item
    obj = ProcessableObject(item)
    
    # Process the object
    process_result = obj.process()
    
    # After use, delete the object to prevent circular references
    del obj
    
    # Optionally, force garbage collection
    gc.collect()