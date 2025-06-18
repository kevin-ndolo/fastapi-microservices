import time
from inventory.main import redis, Product
from redis_om import NotFoundError

# Redis stream and consumer group configuration
key = "order_completed"
group = "inventory-group"
consumer = "inventory-consumer"

# Ensure the consumer group exists (create if not)
try:
    redis.xgroup_create(key, group, mkstream=True)
except Exception as e:
    print(f"Group already exists or error: {e}")

while True:
    try:
        # Read new messages from the Redis stream for this group/consumer
        results = redis.xreadgroup(group, consumer, {key: '>'}, None)
        if results:
            for stream, messages in results:
                for message_id, obj in messages:
                    try:
                        # Fetch the product and update its quantity
                        product = Product.get(obj['product_id'])
                        print(product)
                        product.quantity = int(product.quantity) - int(obj['quantity'])
                        product.save()
                        print(f"Updated product {product.pk}: new quantity {product.quantity}")
                    except NotFoundError:
                        print(f"Product with id {obj['product_id']} not found in inventory!")
    except Exception as e:
        print(f"Error reading from stream: {repr(e)}")
    time.sleep(1)