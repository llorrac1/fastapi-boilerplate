from decouple import config
from redis_om import HashModel, Field, Migrator, get_redis_connection


REDIS_URL = config("REDIS_URL")
REDIS_PORT = config("REDIS_PORT")
REDIS_PASSWORD = config("REDIS_PASSWORD")


def redis_connection():
    try: 
        redis = get_redis_connection(
            port=REDIS_PORT,
            # password=REDIS_PASSWORD,
            # url=REDIS_URL,
            decode_responses=True,
        )
        return redis

    except Exception as e:
        print(e)
        return False

redis = redis_connection()


class BaseRedisClass(HashModel):
    class Meta:
        database = redis


class RedisUser(HashModel):
    id: str = Field(None, index=True)
    name: str = Field(None, index=True)
    password: str = None
    email: str = Field(None, index=True)
    is_active: str = None
    is_superuser: str = None

    class Meta:
        database = redis


class User(RedisUser):
    pass


Migrator().run()


# Sample Code ------------------------------------------------ https://github.com/redis/redis-om-python #
# from redis_om import HashModel, get_redis_connection

# redis = get_redis_connection(port=32769, decode_responses=True)


# class User(HashModel):
#     first_name: str
#     last_name: str
#     age: int

#     class Meta:
#         database = redis


# user = User(first_name="John", last_name="Doe", age=30)
# print(user.pk)
# # user.save()

# # user = User.get("1")

# print(user.get("01GQ11X8CPP6AR0MDXKZ03AV0W"))