from __future__ import annotations

from typing import AsyncGenerator, Optional
import asyncio


class StreamGenerator:
    def __init__(self) -> None:
        self.q = asyncio.Queue[Optional[str]]()

    async def push_message(self, msg: str):
        if msg:
            await self.q.put(msg)

    async def close(self):
        await self.q.put(None)

    async def generator(self) -> AsyncGenerator[str, None]:
        while True:
            val = await self.q.get()
            if val == None:
                return
            yield val
