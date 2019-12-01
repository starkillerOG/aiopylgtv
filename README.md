# aiopylgtv
Library to control webOS based LG Tv devices.  Based on pylgtv library at https://github.com/TheRealLink/pylgtv/tree/master/pylgtv which is no longer maintained.

## Requirements
- Python >= 3.8

## Install
```
pip install aiopylgtv
```

## Example

```python
import asyncio
from aiopylgtv import WebOsClient

async def runloop(client):
    await client.connect()
    apps = await client.get_apps()
    for app in apps:
        print(app)
    
    await client.disconnect()

client = WebOsClient('192.168.1.53', timeout_connect=2)            
asyncio.get_event_loop().run_until_complete(runloop(client))

```
