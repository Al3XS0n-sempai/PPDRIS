import datetime
from models import Session

import redis

__redis_server_connection = None

try:
    __redis_server_connection = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
except:
    __redis_server_connection = redis.Redis(host='0.0.0.0', port=6379, db=0, decode_responses=True)


def create_session() -> Session:
    session = Session()
    session.expiration_timestamp = datetime.datetime.now() + datetime.timedelta(hours=1)
    session.role = 'user'
    session.id = __redis_server_connection.incr('last_session_id', 1)

    _ = __redis_server_connection.hmset(
        f"session:{session.id}",
        {
            'role': session.role,
            'expiration_timestamp': session.expiration_timestamp.strftime("%Y:%m:%d %H:%M:%S"),
        }
    )
    return session


def get_session(session_id: int) -> Session:
    session = Session()

    data = __redis_server_connection.hgetall(f"session:{session_id}")

    if not data:
        return None
    
    session.id = session_id
    session.role = data['role']
    session.expiration_timestamp = datetime.datetime.strptime(
        data['expiration_timestamp'], 
        "%Y:%m:%d %H:%M:%S"
    )

    return session
