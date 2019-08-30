import sacn
import aiohttp.web
import aiohttp.web_request
import json

dmx = sacn.sACNsender()
dmx.activate_output(1)
dmx[1].multicast = True
dmx[1].dmx_data = (0,) * 8
dmx.start()

routes = aiohttp.web.RouteTableDef()


@routes.get('/')
async def handle(request: aiohttp.web_request.Request):
    del request  # unused
    return aiohttp.web.FileResponse('static/index.html')


websockets = set()


@routes.get('/ws')
async def handle(request: aiohttp.web_request.Request):
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    await ws.send_json({
        key: value
        for key, value in enumerate(dmx[1].dmx_data[:8], start=1)
    })

    websockets.add(ws)

    async for msg in ws:
        try:
            data = {int(key): int(value) for key, value in json.loads(msg.data).items()}

            for key, value in data.items():
                assert 1 <= key <= 8
                assert 0x00 <= value <= 0xFF

            dmx[1].dmx_data = tuple(
                value if key not in data else data[key]
                for key, value in enumerate(dmx[1].dmx_data[:8], start=1)
            )

            for other in websockets:
                if other == ws:
                    continue
                await other.send_json(data)

        except (json.decoder.JSONDecodeError, ValueError, AssertionError) as e:
            print(e)
            await ws.close()

    websockets.remove(ws)

    return ws


routes.static('/static', 'static')

if __name__ == '__main__':
    app = aiohttp.web.Application()
    app.add_routes(routes)
    aiohttp.web.run_app(app)
    dmx.stop()
