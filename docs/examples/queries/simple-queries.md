# Simple-style Queries

This style of querying reads almost like SQL, making most queries easier to write using this style.
Multiple conditions can also be joined together using AND/OR clauses in this style, which is not possible in the filter style queries.

!!! tip
If you have difficulty choosing, just pick this style of queries 😉. It can do everything the filter-style queries can do, and more!

!!! tip
Refer the [PostgREST docs](https://postgrest.org/en/v8.0/api.html?highlight=filters#operators) for more info about operators.

### Simple example

```py
from pgrest import Column

res = await client.from_("countries").select("*").where(Column("name") == "India")
```

!!! note
The comparison operators (`==`, `!=`, `>`, `<`, `<=`, `>=`) have been implemented directly as Python operators, although they also have equivalent methods on the Column class. That is, `Column("name") == "India"` and `Column("name").eq("India")` are both valid.

### Join conditions with an OR/AND clause

```py
res = await client
    .from_("countries")
    .select("*")
    .where(Column("capital") == "Rome" | Column("capital") == "Berlin")
    .execute()
```

```py
res = await client
    .from_("countries")
    .select("*")
    .where(Column("continent") == "Asia" & Column("population") >= 5000000)
    .execute()
```

```py
res = await client
    .from_("countries")
    .select("*")
    .where(Column("continent") == "Asia" & Column("population") >= 5000000 | Column("name").ilike("%stan"))
    .execute()
```

!!! tip
In case both AND (`&`) and OR (`|`) appear in the query, the order of precedence is to first evalute AND, then OR.
