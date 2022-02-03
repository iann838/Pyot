# Pipeline

A data pipeline is a series of caches, databases, and data sources that provides and/or stores data, they are generally called as "stores". The data pipeline is a list of data stores, where the order the data stores specifies how data is pulled and stored. Usually faster data stores go at the beginning of the data pipeline.

When data is queried, a query token is constructed containing the information needed to uniquely identify an object in a data source (e.g. a `region` and `summoner.id` are required when querying for `Summoner` objects). This query is passed up the data pipeline through, and at each data store in the data pipeline asks if that source can supply the requested object. If the store can supply the object (for example, if the object is in the cache, or if the Riot API can send the object/data), it is returned. If the source does not supply the object, the next data store in the pipeline is queried. If no data store can provide an object for the query, a `pyot.core.exceptions.NotFindable` is thrown.

After an object is returned by a data store, the object gets passed backwards in the pipeline. Any data store placed before the store that returned the object will attempt to store the data (e.g. cache it).

Each model requires to have its own pipelines configured.
