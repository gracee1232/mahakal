import asyncio

locks = {}

def get_lock(key: str):
    if key not in locks:
        locks[key] = asyncio.Lock()
    return locks[key]