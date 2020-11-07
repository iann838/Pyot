# Stores

Specify the backend of the store on the pipeline.
```python
{
    "BACKEND": "pyot.stores.RiotAPI",
    # ...
}
```

:::tip
The arguments keys passed to Pyot Settings Pipeline can be in ALL CAPS to maintain better code redability, it is automatically lowercased on activation anyways.
:::

# Legend

-<Badge text="Pyot Cache" vertical="middle"/>: Identifies the store of type Cache.

-<Badge text="Pyot Service" vertical="middle"/>: Identifies the store of type Service.

-<Badge text="Sharding" type="error" vertical="middle" />: This store supports multiple instances (hence sharding by separating multiple Cache to handle different type of objects) in the Pipeline.

-<Badge text="Model" type="warning" vertical="middle" />: This is a Pyot model.

-<Badge text="<model-name>" type="error" vertical="middle" />: The name of the model supported if not all.
