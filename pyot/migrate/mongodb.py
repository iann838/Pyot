from typing import List
from pyot.pipeline import pipelines
from pyot.stores import MongoDB
from pyot.utils import async_to_sync, pytify


@async_to_sync
async def migrate_all_to_bson(model: str):
    model = model.lower()
    pipeline = pipelines[model]
    stores: List[MongoDB] = []
    for store in pipeline:
        if isinstance(store, MongoDB):
            stores.append(store)
    for store in stores:
        await store.connect()
        for method in store._manager:
            col = store._cache[method]
            cursor = col.find({})
            docs = await cursor.to_list(length=10)
            while docs:
                for doc in docs:
                    data_type = doc.get("dataType", "pickle")
                    if data_type == "pickle":
                        await col.update_one(
                            {"_id": doc["_id"]},
                            {"$set": {
                                "data": pytify(doc["data"]),
                                "dataType": "bson"
                            }}
                        )
                docs = await cursor.to_list(length=10)
