import pytest
from src.async_examples.main import hello_world


@pytest.mark.asyncio
async def test_hello_world():
    """Test that hello_world function returns 'World' and prints 'Hello'."""
    result = await hello_world()
    assert result == "World"


@pytest.mark.asyncio
async def test_hello_world_output(capsys):
    """Test that hello_world function prints 'Hello' to stdout."""
    await hello_world()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello"