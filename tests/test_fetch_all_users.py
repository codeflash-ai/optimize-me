import pytest
from src.asynchrony.various import fetch_all_users


@pytest.mark.asyncio
async def test_fetch_all_users_empty_list():
    """Test fetch_all_users with an empty list of user IDs"""
    result = await fetch_all_users([])
    assert result == []


@pytest.mark.asyncio
async def test_fetch_all_users_single_user():
    """Test fetch_all_users with a single user ID"""
    result = await fetch_all_users([1])
    assert len(result) == 1
    assert result[0] == {"id": 1, "name": "User1"}


@pytest.mark.asyncio
async def test_fetch_all_users_multiple_users():
    """Test fetch_all_users with multiple user IDs"""
    user_ids = [1, 2, 3, 4, 5]
    result = await fetch_all_users(user_ids)

    assert len(result) == 5
    for i, user in enumerate(result, start=1):
        assert user == {"id": i, "name": f"User{i}"}


@pytest.mark.asyncio
async def test_fetch_all_users_order_preserved():
    """Test that fetch_all_users preserves the order of user IDs"""
    user_ids = [5, 2, 8, 1, 3]
    result = await fetch_all_users(user_ids)

    assert len(result) == 5
    assert result[0] == {"id": 5, "name": "User5"}
    assert result[1] == {"id": 2, "name": "User2"}
    assert result[2] == {"id": 8, "name": "User8"}
    assert result[3] == {"id": 1, "name": "User1"}
    assert result[4] == {"id": 3, "name": "User3"}


@pytest.mark.asyncio
async def test_fetch_all_users_duplicate_ids():
    """Test fetch_all_users with duplicate user IDs"""
    user_ids = [1, 2, 1, 3, 2]
    result = await fetch_all_users(user_ids)

    assert len(result) == 5
    assert result[0] == {"id": 1, "name": "User1"}
    assert result[1] == {"id": 2, "name": "User2"}
    assert result[2] == {"id": 1, "name": "User1"}
    assert result[3] == {"id": 3, "name": "User3"}
    assert result[4] == {"id": 2, "name": "User2"}


@pytest.mark.asyncio
async def test_fetch_all_users_large_list():
    """Test fetch_all_users with a large number of user IDs"""
    user_ids = list(range(1, 101))
    result = await fetch_all_users(user_ids)

    assert len(result) == 100
    for i, user in enumerate(result, start=1):
        assert user == {"id": i, "name": f"User{i}"}
