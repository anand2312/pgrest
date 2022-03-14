# pgrest

Asynchronous PostgREST client for Python. This library provides an ORM interface to PostgREST.

Fork of the supabase community Postgrest Client library for Python.

[Documentation](https://anand2312.github.io/pgrest)

## Getting Started
Before running any queries, you need to initialize the client:
```py
from pgrest import Client

client = Client("http://localhost:3000")  # pass in your postgrest API url
client.auth("bearer token")  # pass in your API bearer token
```

You can insert new rows...
```py
await client.from_("countries").insert({ "name": "Việt Nam", "capital": "Hà Nội" }).execute()
```
or bulk insert multiple rows in a single query:
```py
rows = [{"name": "India", "capital": "New Delhi"}, {"name": "Japan", "capital": "Tokyo"}]
await client.from_("countries").insert_many(rows).execute()
```
Read rows
```py
r = await client.from_("countries").select("id", "name").execute()
countries = r[0]
```
Or run more complicated filters for your queries!
```py
from pgrest import Column
# you can merge multiple conditions with AND/OR clauses
# | means OR, & means AND
r = await client.from_("countries")
    .select("*")
    .where((Column("population") >= 10_000_000) & (Column("population") <= 20_000_000) | (Column("name").ilike("%stan")))
    .execute()
# this query fetches all countries whose population is between 10 million and 20 million, or whose name ends in `stan`
```

## PROJECT TODOS:

- [ ] upsert methods
- [x] AND/OR filtering (v0.7.0)
- [ ] allow users to pass response models?
- [ ] add configuration parameter to text-search functions
