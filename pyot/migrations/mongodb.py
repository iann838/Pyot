from pyot.pipeline import pipelines
from pyot.stores import MongoDB
from pyot.utils import bytify, pytify


async def _iterate_and_update_serialization(store: MongoDB, method: str, to_type: str):
    col = store._cache[method]
    cursor = col.find({})
    docs = await cursor.to_list(length=10)
    while docs:
        for doc in docs:
            data_type = doc.get("dataType", "pickle")
            if data_type == to_type:
                continue
            if to_type == "bson":
                if data_type == "pickle":
                    await col.update_one({"_id": doc["_id"]}, {"$set": {"data": pytify(doc["data"]), "dataType": to_type}})
            elif to_type == "pickle":
                if data_type == "bson":
                    await col.update_one({"_id": doc["_id"]}, {"$set": {"data": bytify(doc["data"]), "dataType": to_type}})
        docs = await cursor.to_list(length=10)


async def migrate_serialization(model: str, to_type: str):
    model = model.lower()
    to_type = to_type.lower()
    if to_type not in {'pickle', 'bson'}:
        raise ValueError("MongoDB serialization type should be one of: 'pickle', 'bson'")
    pipeline = pipelines[model]
    for store in pipeline:
        if store.classname == "MongoDB":
            await store.connect()
            for method in store._manager:
                await _iterate_and_update_serialization(store, method, to_type)
