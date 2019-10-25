import asyncio
import datetime
import json
from hwilib import commands
from sanic_cors import CORS, cross_origin

from sanic import Sanic
from sanic.response import file
from sanic.websocket import WebSocketProtocol
from sanic_graphql import GraphQLView

from graphql_ws.websockets_lib import WsLibSubscriptionServer

from rpc import BitcoinRPC
from gql import schema


hwi_lock = asyncio.Lock()
app = Sanic()
CORS(app, automatic_options=True)
rpc = BitcoinRPC(
    user='bitcoin',
    passwd='python',
    host='127.0.0.1',
    port=18332,
)

async def hwi_enumerate():
    async with hwi_lock:
        return commands.enumerate()

@app.websocket('/devices')
async def list_devices(request, ws):
    while True:
        devices = await hwi_enumerate()
        await ws.send(json.dumps(devices))
        await asyncio.sleep(1)

@app.websocket('/node')
async def node_state(request, ws):
    while True:
        try:
            response = await rpc.getblockchaininfo()
            data = {
                "error": False,
                "data": response,
            }
            await ws.send(json.dumps(data))
        except Exception as e:
            data = {
                "error": True,
                "description": str(e),
            }
            await ws.send(json.dumps(data))
        await asyncio.sleep(1)

@app.route('/')
async def index(request):
    return await file('index.html')



app.add_route(GraphQLView.as_view(schema=schema, graphiql=True), '/graphql')

# @app.listener('before_server_start')
# def init_graphql(app, loop):
    # app.add_route(GraphQLView.as_view(schema=schema, executor=AsyncioExecutor(loop=loop)), '/graphql')


subscription_server = WsLibSubscriptionServer(schema)

@app.websocket('/subscriptions', subprotocols=['graphql-ws'])
async def subscriptions(request, ws):
    await subscription_server.handle(ws)
    return ws

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)
