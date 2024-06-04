from contextlib import nullcontext as does_not_raise

import aiohttp
import pytest

from tests.functional.utils.client_helpers import make_get_request, make_post_request


@pytest.mark.parametrize(
    "expected_answer, expectation",
    [
        (
                {
                    "status": 200,
                },
                does_not_raise(),
        )
    ],
)
@pytest.mark.asyncio
async def test_healthcheck(
        aiohttp_session,
        url_hash_service,
        expected_answer,
        expectation,
):
    url = url_hash_service + "/healthcheck"
    with expectation:
        response, response_status = await make_get_request(aiohttp_session, url, {})
        assert expected_answer["status"] == response_status