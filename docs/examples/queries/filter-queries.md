# Filter queries

This is the original style of queries established by existing Supabase client side libraries, including the Javascript client.
It lets you chain multiple methods to form complex filters, although this can become a little untidy at times. Moreover, this form of querying
does not let you combine multiple conditions using AND/OR clauses (currently).

!!! tip
Refer the [PostgREST docs](https://postgrest.org/en/v8.0/api.html?highlight=filters#operators) for more info about operators.

```py
res = await client
    .from_("countries")
    .select("*")
    .filter("name", "eq", "India")
    .execute()
```

```py
res = await client
  .from_("cities)
  .select("name, country_id")
  .gte("population", 1000)
  .lt("population", 10000)
```
