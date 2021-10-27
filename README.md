[![](https://img.shields.io/github/license/supabase/postgrest-py)](https://github.com/supabase/postgrest-py)
[![](https://img.shields.io/pypi/pyversions/postgrest-py)](https://pypi.org/project/postgrest-py)
[![](https://img.shields.io/pypi/v/postgrest-py)](https://pypi.org/project/postgrest-py)

# postgrest-py

PostgREST client for Python. This library provides an ORM interface to PostgREST.

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

### Instructions

#### With Poetry (recommended)

```sh
$ poetry add postgrest-py
```

#### With Pip

```sh
$ pip install postgrest-py
```

## USAGE

### Getting started

```py
import asyncio
from postgrest_py import AsyncPostgrestClient

async def main():
    async with AsyncPostgrestClient("http://localhost:3000") as client:
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
r = await client.rpc("hello_world")
r.json()
```
```py
r = await client.rpc("echo_city", params={"name": "The Shire"})
r.json()
```

All above methods also have synchronous counterparts, under `postgrest_py.PostgrestClient`.
## DEVELOPMENT

```sh
$ git clone https://github.com/supabase/postgrest-py.git
$ cd postgrest-py
$ poetry install
$ poetry run pre-commit install
```

### Testing

```sh
$ poetry run pytest
```

## CHANGELOG

Read more [here](https://github.com/supabase/postgrest-py/blob/master/CHANGELOG.md).

## TODO

Read more [here](https://github.com/supabase/postgrest-py/blob/master/TODO.md).

## SPONSORS

We are building the features of Firebase using enterprise-grade, open source products. We support existing communities wherever possible, and if the products don’t exist we build them and open source them ourselves. Thanks to these sponsors who are making the OSS ecosystem better for everyone.

[![Worklife VC](https://user-images.githubusercontent.com/10214025/90451355-34d71200-e11e-11ea-81f9-1592fd1e9146.png)](https://www.worklife.vc)
[![New Sponsor](https://user-images.githubusercontent.com/10214025/90518111-e74bbb00-e198-11ea-8f88-c9e3c1aa4b5b.png)](https://github.com/sponsors/supabase)
