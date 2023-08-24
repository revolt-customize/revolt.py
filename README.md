# Revolt.py

An async library to interact with the <https://revolt.chat> API.

You can join the support server [here](https://rvlt.gg/FDXER6hr) and find the library's documentation [here](https://revoltpy.readthedocs.io/en/latest/).

## Installing

You can use `pip` to install revolt.py. It differs slightly depending on what OS/Distro you use.

On Windows

```
py -m pip install -U revolt-baidu.py # -U to update
```

On macOS and Linux

```
python3 -m pip install -U revolt-baidu.py
```

## Example

More examples can be found in the [examples folder](https://github.com/revolt-customize/revolt.py/tree/master/examples).

```py
import revolt
import asyncio

class Client(revolt.Client):
    async def on_message(self, message: revolt.Message):
        if message.content == "hello":
            await message.channel.send("hi how are you")

async def main():
    async with revolt.utils.client_session() as session:
        client = Client(session, "BOT TOKEN HERE")
        await client.start()

asyncio.run(main())
```

## Bot interaction example

```py
class Client(revolt.Client):
    async def on_interaction(
        self, interaction: InteractionEventPayload, message: revolt.Message
    ) -> None:
        logger.info("interaction %s", interaction)
        user = self.get_user(interaction["author_id"])
        await message.channel.send(
            f"Username: {user.name} Your choice is: {interaction['content']} "
        )
        components = message.components
        components[0]["label"] = "edited"
        components[0]["enabled"] = False

        # update the button component's label
        await message.edit(content="edited", components=components)

    async def on_message(self, message: revolt.Message):
        if message.content == "/button":
            await message.channel.send(
                "you have these options",
                components=[
                    Component(
                        type="button",
                        style="color:white; backgroundColor:green; fontSize:16px; fontWeight:400;",
                        label="continue",
                        enabled=True,
                    ),
                    Component(
                        type="button", style="color:green", label="quit", enabled=True
                    ),
                    Component(
                        type="button", style="color:red", label="restart", enabled=False
                    ),
                ],
            )
```

## Stream Message Example

```py
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
```
