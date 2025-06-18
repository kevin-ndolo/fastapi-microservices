import time
from payment.main import redis, Order
from redis_om import NotFoundError

# Redis stream and consumer group configuration
key = "refund_order"
group = "payment-group"
consumer = "payment-consumer"

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
                        # Fetch the order by primary key (pk) from the Order model
                        order = Order.get(obj['pk'])
                        print(f"Processing refund for order {order.pk}...")
                        # Update the order status to 'refunded' and save
                        order.status = "refunded"
                        order.save()
                        print(f"Order {order.pk} status updated to 'refunded'.")
                    except NotFoundError:
                        print(f"Order with pk {obj['pk']} not found.")
    except Exception as e:
        print(f"Error reading from stream: {repr(e)}")
    time.sleep(1)