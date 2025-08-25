import pytest
from unittest.mock import patch, AsyncMock
from src.async_examples.concurrency import some_api_call


@pytest.mark.asyncio
async def test_some_api_call_empty_list():
    result = await some_api_call([])
    assert result == []


@pytest.mark.asyncio
async def test_some_api_call_single_url():
    with patch(
        "src.async_examples.concurrency.fake_api_call", new_callable=AsyncMock
    ) as mock_api:
        mock_api.return_value = "Processed: test_url"

        result = await some_api_call(["test_url"])

        assert result == ["Processed: test_url"]
        mock_api.assert_called_once()


@pytest.mark.asyncio
async def test_some_api_call_multiple_urls():
    urls = ["url1", "url2", "url3"]
    expected_results = ["Processed: url1", "Processed: url2", "Processed: url3"]

    with patch(
        "src.async_examples.concurrency.fake_api_call", new_callable=AsyncMock
    ) as mock_api:
        mock_api.side_effect = expected_results

        result = await some_api_call(urls)

        assert result == expected_results
        assert mock_api.call_count == 3


@pytest.mark.asyncio
async def test_some_api_call_sequential_execution():
    call_order = []

    async def mock_fake_api_call(delay, data):
        call_order.append(data)
        return f"Processed: {data}"

    with patch(
        "src.async_examples.concurrency.fake_api_call", side_effect=mock_fake_api_call
    ):
        urls = ["first", "second", "third"]
        await some_api_call(urls)

        assert call_order == ["first", "second", "third"]


@pytest.mark.asyncio
async def test_some_api_call_preserves_order():
    urls = ["a", "b", "c", "d"]

    with patch(
        "src.async_examples.concurrency.fake_api_call", new_callable=AsyncMock
    ) as mock_api:
        mock_api.side_effect = [
            "Processed: a",
            "Processed: b",
            "Processed: c",
            "Processed: d",
        ]

        result = await some_api_call(urls)

        expected = ["Processed: a", "Processed: b", "Processed: c", "Processed: d"]
        assert result == expected
