# Getting Started

```py
import asyncio
from pgrest import Client

async def main():
    async with Client("http://localhost:3000") as client:
        r = await client.from_("countries").select("*").execute()
        # execute returns a two-tuple, where the first element is the data.
        countries = r[0]

asyncio.run(main())
```

### Create

```py
await client.from_("countries").insert({ "name": "Việt Nam", "capital": "Hà Nội" }).execute()
```

### Bulk Insert

```py
rows = [{"name": "India", "capital": "New Delhi"}, {"name": "Japan", "capital": "Tokyo"}]
await client.from_("countries").insert_many(rows).execute()
```

### Read

```py
r = await client.from_("countries").select("id", "name").execute()
countries = r[0]
```

### Update

```py
await client.from_("countries").update({"capital": "Hà Nội"}).eq("name", "Việt Nam").execute()
```

### Delete

```py
await client.from_("countries").delete().eq("name", "Việt Nam").execute()
```

### Stored procedures (RPC)

```py
r = await client.rpc("hello_world").execute()
```

```py
r = await client.rpc("echo_city", params={"name": "The Shire"}).execute()
```
