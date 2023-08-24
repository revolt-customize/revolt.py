import asyncio
import aiohttp
from langchain import OpenAI
import revolt
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from revolt.enums import ChannelType
from revolt.stream_handler import StreamGenerator
from typing import Any
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from revolt.enums import ChannelType

from langchain.callbacks.base import AsyncCallbackHandler


chat_open_ai = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, streaming=True)
llm = OpenAI(streaming=True)

state: dict[str, list[BaseMessage]] = {}


class StreamingLLMCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming LLM responses."""

    def __init__(self, q: StreamGenerator):
        self.q = q

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        data = {"token": token}
        print(data)
        await self.q.push_message(token)

    async def on_llm_end(
        self,
        response,
        **kwargs: Any,
    ) -> None:
        await self.q.close()


async def process(
    history: list[BaseMessage],
    stream_handler: StreamGenerator,
) -> str:
    response = await chat_open_ai.agenerate(
        [history], callbacks=[StreamingLLMCallbackHandler(stream_handler)]
    )

    text = response.generations[0][0].text

    history.append(AIMessage(content=text))

    return text


class Client(revolt.Client):
    def need_reply(self, message: revolt.Message) -> bool:
        message_user = self.get_user(message.author.id)
        is_response = False
        for user in message.mentions:
            if user.id == self.user.id:
                is_response = True

        if message.channel.channel_type == ChannelType.direct_message:
            is_response = True

        return message_user.id != self.user.id and is_response

    async def on_message(self, message: revolt.Message):
        if not self.need_reply(message):
            return

        content = message.content

        if message.author.id not in state:
            state[message.author.id] = []

        history = state[message.author.id]
        history.append(HumanMessage(content=content))

        while len(history) > 10:
            history.pop(0)

        g = StreamGenerator()
        task1 = asyncio.create_task(
            message.channel.send(stream_generator=g.generator())
        )
        task2 = asyncio.create_task(process(history, g))

        await asyncio.gather(task1, task2)


async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(
            session,
            "Your Bot Token Here",
            api_url="API Url Here",
        )
        await client.start()


asyncio.run(main())
