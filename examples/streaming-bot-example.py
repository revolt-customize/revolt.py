import asyncio
import aiohttp
import revolt
from revolt.enums import ChannelType
from revolt.stream_handler import StreamGenerator


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

        g = StreamGenerator()

        async def stream_message():
            for i in range(10):
                await g.push_message(f"hello {i}  ")

            # needs to call g.close when generating has been finished
            await g.close()

        asyncio.create_task(stream_message())
        await message.channel.send(stream_generator=g.generator())


async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(
            session,
            "Your Bot Token Here",
            api_url="Your API Here",
        )
        await client.start()


asyncio.run(main())
