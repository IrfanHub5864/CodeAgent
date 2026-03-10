import gc

# Within the loop that processes items
for item in items:
    # Process the item
    process_item(item)
    # Trigger garbage collection
    gc.collect()