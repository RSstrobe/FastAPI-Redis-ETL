import json


async def make_get_request(aiohttp_session, url: str, query_data: dict):
    kwarg = {
        "url": url,
        "params": query_data,
        "raise_for_status": True,
    }
    async with aiohttp_session.get(**kwarg) as response:
        return await response.json(), response.status


async def make_post_request(aiohttp_session, url: str, body: dict):
    header = {"accept": "application/json", "Content-Type": "application/json"}
    kwarg = {
        "url": url,
        "raise_for_status": True,
        "headers": header,
        "data": json.dumps(body),
    }
    async with aiohttp_session.post(**kwarg) as response:
        return await response.json(), response.status
