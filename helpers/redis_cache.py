# import redis

# # Connect to Redis server
# r = redis.Redis(host='localhost', port=6379, db=0)

# # Set a value in Redis
# r.set('key', 'value')
# # Get the value from Redis
# value = r.get('key')


# r.set('username', 'john_doe')
# username = r.get('username')
# print(username.decode('utf-8'))

# r.lpush('numbers', 1, 2, 3)
# numbers = r.lrange('numbers', 0, -1)
# print([int(num) for num in numbers])  # Output: [3, 2, 1]

# r.sadd('tags', 'python', 'redis', 'flask')
# tags = r.smembers('tags')
# print(tags)

# # Print the value (it will be in bytes, so decode to a string)
# print(value.decode('utf-8'))  # Output: value

# # r.close()

import redis
from typing import Optional
from datetime import timedelta

# Redis client setup
# redis_client = redis.Redis(host='localhost', port=6379, db=0)
# 127.0.0.1:6379
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Cache expiration time (optional)
# CACHE_EXPIRATION = timedelta(minutes=30)
CACHE_EXPIRATION = timedelta(minutes=1)