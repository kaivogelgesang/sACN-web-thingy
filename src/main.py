import aiohttp.web

routes = aiohttp.web.RouteTableDef()


@routes.get('/')
async def handle(request: aiohttp.web.Request):
    del request  # unused
    print('get /')
    return aiohttp.web.FileResponse('static/index.html')

routes.static('/static', 'static')

if __name__ == '__main__':
    app = aiohttp.web.Application()
    app.add_routes(routes)
    aiohttp.web.run_app(app)
