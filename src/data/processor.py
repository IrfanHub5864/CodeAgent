import weakref
from contextlib import contextmanager

# Example of using a context manager to ensure resources are cleaned up
@contextmanager
def process_item(item):
    try:
        # Process the item
        yield process_data(item)
    finally:
        # Cleanup
        del item  # Remove the reference to the item

# Usage within the loop
for item in items_to_process:
    with process_item(item) as processed_item:
        # Use the processed item
        store_result(processed_item)