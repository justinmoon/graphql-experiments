import graphene
import json
import asyncio
from datetime import datetime
from hwilib import commands
from rpc import BitcoinRPC

class Device(graphene.ObjectType):
    fingerprint = graphene.String()
    path = graphene.String()
    type = graphene.String()
    model = graphene.String()
    needs_passphrase = graphene.String()
    needs_pin_entry = graphene.String()  # is this correct?

def list_devices():
    devices = commands.enumerate()
    devices = [Device(**device) for device in devices]
    return devices

class Node(graphene.ObjectType):
    online = graphene.Boolean()

def list_nodes():
    nodes = []
    rpc = BitcoinRPC(
        user='bitcoin',
        passwd='python',
        host='127.0.0.1',
        port=18332,
    )
    try:
        response = rpc.getblockchaininfo()
        nodes.append(Node(online=True))
    except Exception as e:
        nodes.append(Node(online=False))
    return nodes

class Query(graphene.ObjectType):
    devices = graphene.List(Device)
    nodes = graphene.List(Node)

    def resolve_devices(self, info):
        return commands.enumerate()

    def resolve_nodes(self, info):
        return list_nodes()

class Subscription(graphene.ObjectType):
    devices = graphene.List(Device)
    nodes = graphene.List(Node)

    async def resolve_devices(root, info):
        while True:
            devices = enumerate()
            yield devices
            await asyncio.sleep(1)

    async def resolve_nodes(root, info):
        while True:
            nodes = list_nodes()
            yield nodes
            await asyncio.sleep(1)

schema = graphene.Schema(query=Query, subscription=Subscription)
