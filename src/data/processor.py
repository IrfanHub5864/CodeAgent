def process_items(items):
    results = []
    for item in items:
        # Process the item
        result = process_item(item)
        results.append(result)
        # Potential memory leak: not clearing references
    return results

def process_item(item):
    # Simulate processing
    return item * 2