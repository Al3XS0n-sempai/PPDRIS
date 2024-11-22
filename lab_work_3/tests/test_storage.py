import datetime
from unittest.mock import patch, MagicMock
import pytest
from storage import create_session, get_session


@pytest.fixture
def mock_redis():
    with patch("storage.__redis_server_connection") as mock_redis:
        yield mock_redis


@pytest.fixture
def mock_session():
    return {
        'role': 'user',
        'expiration_timestamp': (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y:%m:%d %H:%M:%S"),
    }


def test_create_session(mock_redis):
    # Замокать методы Redis
    mock_redis.incr.return_value = 1
    mock_redis.hmset.return_value = True

    session = create_session()

    # Проверка, что id был увеличен
    mock_redis.incr.assert_called_once_with('last_session_id', 1)

    # Проверка, что данные были записаны в Redis
    mock_redis.hmset.assert_called_once()
    args, _ = mock_redis.hmset.call_args
    assert args[0] == f"session:{session.id}"
    assert args[1] == {
        'role': 'user',
        'expiration_timestamp': session.expiration_timestamp.strftime("%Y:%m:%d %H:%M:%S"),
    }

    # Проверка, что возвращается корректный объект
    assert session.id == 1
    assert session.role == 'user'
    assert isinstance(session.expiration_timestamp, datetime.datetime)


def test_get_session_valid(mock_redis, mock_session):
    # Замокать возврат данных из Redis
    mock_redis.hgetall.return_value = mock_session

    session_id = 1
    session = get_session(session_id)

    # Проверка, что данные извлекались из Redis
    mock_redis.hgetall.assert_called_once_with(f"session:{session_id}")

    # Проверка, что возвращается корректный объект
    assert session.id == session_id
    assert session.role == mock_session['role']
    assert session.expiration_timestamp == datetime.datetime.strptime(
        mock_session['expiration_timestamp'], "%Y:%m:%d %H:%M:%S"
    )


def test_get_session_not_found(mock_redis):
    # Замокать пустой возврат данных из Redis
    mock_redis.hgetall.return_value = {}

    session_id = 1
    session = get_session(session_id)

    # Проверка, что данные извлекались из Redis
    mock_redis.hgetall.assert_called_once_with(f"session:{session_id}")

    # Проверка, что None возвращается, если данные не найдены
    assert session is None
