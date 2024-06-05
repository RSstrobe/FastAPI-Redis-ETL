from contextlib import nullcontext as does_not_raise

import aiohttp
import pytest

from tests.functional.utils.client_helpers import make_post_request, make_get_request, make_patch_request


@pytest.mark.parametrize(
    "data, expected_answer, expectation",
    [
        # Первичная запись
        (
                {
                    "phone": "89090000000",
                    "address": "Street",
                },
                {
                    "key": "+79090000000",
                    "address": "Street",
                    "status": 201,
                },
                does_not_raise(),
        ),
        # Повторная запись
        (
                {
                    "phone": "89090000000",
                    "address": "Street",
                },
                {
                    "status": 409,
                },
                pytest.raises(aiohttp.ClientResponseError),
        ),
        # Номер меньше 11 символов
        (
                {
                    "phone": "8909000000",
                    "address": "Street",
                },
                {
                    "status": 409,
                },
                pytest.raises(aiohttp.ClientResponseError),
        ),
        # Некорректный номер
        (
                {
                    "phone": "8909000000abc",
                    "address": "Street",
                },
                {
                    "status": 409,
                },
                pytest.raises(aiohttp.ClientResponseError),
        ),
        # # Пустой адресс
        # (
        #         {
        #             "phone": "89090000001",
        #             "address": "",
        #         },
        #         {
        #             "key": "+79090000001",
        #             "address": "",
        #             "status": 409,
        #         },
        #         pytest.raises(aiohttp.ClientResponseError),
        # ),
    ],
)
@pytest.mark.asyncio
async def test_write_data(
        aiohttp_session,
        redis_read_data,
        url_service,
        data,
        expected_answer,
        expectation,
):
    url = url_service + "/data"
    with expectation:
        response, response_status = await make_post_request(aiohttp_session, url, data)
        assert expected_answer["status"] == response_status
        redis_response = await redis_read_data(expected_answer["key"])
        assert expected_answer["address"] == redis_response.decode()
        assert expected_answer["key"] == response["phone"]


@pytest.mark.parametrize(
    "data, expected_answer, expectation",
    [
        # Проверка с +7
        (
                {
                    "phone": "+79090000000",
                },
                {
                    "key": "+79090000000",
                    "address": "Street",
                    "status": 200,
                },
                does_not_raise(),
        ),
        # Проверка с 8
        (
                {
                    "phone": "89090000000",
                },
                {
                    "key": "+79090000000",
                    "address": "Street",
                    "status": 200,
                },
                does_not_raise(),
        ),
        # Несуществующий номер
        (
                {
                    "phone": "+79090000002",
                },
                {
                    "key": "+79090000002",
                    "address": "Street",
                    "status": 409,
                },
                pytest.raises(aiohttp.ClientResponseError),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_data(
        aiohttp_session,
        redis_read_data,
        url_service,
        data,
        expected_answer,
        expectation,
):
    url = url_service + "/data"
    with expectation:
        response, response_status = await make_get_request(aiohttp_session, url, data)
        assert expected_answer["status"] == response_status
        redis_response = await redis_read_data(expected_answer["key"])
        assert expected_answer["address"] == redis_response.decode()
        assert expected_answer["address"] == response["address"]
        assert expected_answer["key"] == response["phone"]

@pytest.mark.parametrize(
    "data, expected_answer, expectation",
    [
        # Проверка с +7
        (
                {
                    "phone": "89090000000",
                    "address": "New Street",
                },
                {
                    "key": "+79090000000",
                    "address": "New Street",
                    "status": 200,
                },
                does_not_raise(),
        ),
        # Несуществующий номер
        (
                {
                    "phone": "+79090000002",
                },
                {
                    "key": "+79090000002",
                    "address": "Street",
                    "status": 409,
                },
                pytest.raises(aiohttp.ClientResponseError),
        ),
    ],
)
@pytest.mark.asyncio
async def test_change_data(
        aiohttp_session,
        redis_read_data,
        url_service,
        data,
        expected_answer,
        expectation,
):
    url = url_service + "/data"
    with expectation:
        response, response_status = await make_patch_request(aiohttp_session, url, data)
        assert expected_answer["status"] == response_status
        redis_response = await redis_read_data(expected_answer["key"])
        assert expected_answer["address"] == redis_response.decode()
        assert expected_answer["address"] == response["address"]
        assert expected_answer["key"] == response["phone"]