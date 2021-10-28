# pgrest-client

PostgREST client for Python. This library provides an ORM interface to PostgREST.

Fork of the supabase community Postgrest Client library for Python.

Status: **Unstable**

## INSTALLATION

### Requirements

- Python >= 3.7
- PostgreSQL >= 12
- PostgREST >= 7

### Local PostgREST server

If you want to use a local PostgREST server for development, you can use our preconfigured instance via Docker Compose.

```sh
docker-compose up
```

Once Docker Compose started, PostgREST is accessible at http://localhost:3000.

## USAGE

### Getting started

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

### General filters

### Stored procedures (RPC)

```py
r = await client.rpc("hello_world").execute()
```

```py
r = await client.rpc("echo_city", params={"name": "The Shire"}).execute()
```

All above methods also have synchronous counterparts, under `pgrest._sync_client.SyncClient`.
