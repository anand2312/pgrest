# Getting Started

```py
import asyncio
from pgrest import Client

async def main():
    async with Client("http://localhost:3000") as client:
        r = await client.from_("countries").select("*").execute()
        countries = r[0]

asyncio.run(main())
```

### Create

```py
await client.from_("countries").insert({ "name": "Việt Nam", "capital": "Hà Nội" }).execute()
```

### Read

```py
r = await client.from_("countries").select("id", "name").execute()
countries = r[0]
```

### Update

```py
await client.from_("countries").eq("name", "Việt Nam").update({"capital": "Hà Nội"}).execute()
```

### Delete

```py
await client.from_("countries").eq("name", "Việt Nam").delete().execute()
```

### Stored procedures (RPC)

```py
r = await client.rpc("hello_world").execute()
```

```py
r = await client.rpc("echo_city", params={"name": "The Shire"}).execute()
```

All above methods have synchronous counterparts in `pgrest._sync_client.SyncClient`, although the asynchronous functionality is the focus of this library, and is recommended to be used.
