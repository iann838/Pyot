from typing import List
from pyot.pipeline import pipelines
from pyot.stores import MongoDB
from pyot.utils import async_to_sync


@async_to_sync
async def migrate_serialization(model: str, to_type: str = None):
    model = model.lower()
    pipeline = pipelines[model]
    stores: List[MongoDB] = []
    for store in pipeline:
        if isinstance(store, MongoDB):
            stores.append(store)
    for store in stores:
        if to_type is None:
            to_type = store._serializer.serialization
        else:
            to_type = to_type.lower()
            store._serializer.valid_type(to_type, throw=True)
        await store.connect()
        for method in store._manager:
            col = store._cache[method]
            cursor = col.find({})
            docs = await cursor.to_list(length=10)
            while docs:
                for doc in docs:
                    data_type = doc.get("dataType", "pickle")
                    if data_type == to_type:
                        continue
                    await col.update_one(
                        {"_id": doc["_id"]},
                        {"$set": {
                            "data": store._serializer.transerialize(doc["data"], data_type, to_type),
                            "dataType": to_type
                        }}
                    )
                docs = await cursor.to_list(length=10)
