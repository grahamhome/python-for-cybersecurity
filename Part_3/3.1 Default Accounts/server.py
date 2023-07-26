import asyncio

import telnetlib3


async def shell(reader, writer):
    writer.write("\r\nWould you like to play a game? ")
    inp = await reader.read(1)
    if inp:
        writer.echo(inp)
        writer.write("\r\nThey say the only way to win " "is to not play at all.\r\n")
        await writer.drain()
    writer.close()


loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=6023, shell=shell)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())
