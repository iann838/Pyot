# Methods

### Submodule: `common`

> ## `loop_run(coro)` <Badge text="function" type="error" vertical="middle"/>
> Run the coroutine in the current event loop or a new one if `set_event_loop()` has not yet been called.

> ## `thread_run(func)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Run a blocking function in a thread.

> ## `snakecase(camel_str: str) -> str` <Badge text="function" type="error" vertical="middle"/>
> Convert string to python snakecase.

> ## `camelcase(snake_str: str) -> str` <Badge text="function" type="error" vertical="middle"/>
> Convert string to json camelcase.
    
> ## `import_class(path: str) -> Any` <Badge text="function" type="error" vertical="middle"/>
> Return the class given its python path

> ## `fast_copy(obj)` <Badge text="function" type="error" vertical="middle"/>
> 30x faster copy than `copy.deepcopy`, not all objects can be copied.

> ## `bytify(obj)` <Badge text="function" type="error" vertical="middle"/>
> Convert a python object to byte string.

> ## `pytify(obj)` <Badge text="function" type="error" vertical="middle"/>
> Convert a byte string to python object.

> ## `shuffle_list(li: List[Any], param: str, size: int = 10)` <Badge text="function" type="error" vertical="middle"/>
> Shuffle a list by a specified param and chunk size.
> - `param` <Badge text="param" type="warning" vertical="middle"/>: param to shuffle based on, either the an attribute or key.
> - `size` <Badge text="param" type="warning" vertical="middle"/>: size of the returned chunks, e.g. `size=10` will return a new list with items of the same `param` every 10 items. Typically used for mixing pyot objects regions and platforms to better regulate rate limits.


### Submodule: `cdragon`

> ## `start_k(string: str) -> str`  <Badge text="function" type="error" vertical="middle"/> 
> Removes k if string start with k.
> - `string` <Badge text="param" type="warning" vertical="middle"/>: String to remove k prefix.

> ## `cdragon_url(link: str) -> str`  <Badge text="function" type="error" vertical="middle"/> 
> Return the CDragon url for the given game asset url.
> - `link` <Badge text="param" type="warning" vertical="middle"/>: Original returned url 

> ## `tft_url(link: str) -> str`  <Badge text="function" type="error" vertical="middle"/> 
> Return the CDragon url for the given tft asset url.
> - `link` <Badge text="param" type="warning" vertical="middle"/>: Original returned url

> ## `cdragon_sanitize(string: str) -> str`  <Badge text="function" type="error" vertical="middle"/> 
> Sanitize CDragon descriptions.
> - `string` <Badge text="param" type="warning" vertical="middle"/>: Dirty string to sanitize

> ## `tft_item_sanitize(string: str, obj: dict) -> str`  <Badge text="function" type="error" vertical="middle"/> 
> Sanitize CDragon tft item descriptions.
> - `string` <Badge text="param" type="warning" vertical="middle"/>: Dirty string to sanitize
> - `obj` <Badge text="param" type="warning" vertical="middle"/>: Dict containing tft item variables.

> ## `tft_champ_sanitize(string: str, list_of_obj: list) -> str`  <Badge text="function" type="error" vertical="middle"/> 
> Sanitize CDragon tft champion descriptions.
> - `string` <Badge text="param" type="warning" vertical="middle"/>: Dirty string to sanitize
> - `obj` <Badge text="param" type="warning" vertical="middle"/>: List of dict containing tft champion variables.

### Submodule: `champion`

:::tip INFO
Responses (All the champions) will be cached for 3 hours
:::

> ## `champion_id_by_key(value)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Convert champion key to id

> ## `champion_id_by_name(value)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Convert champion name to id

> ## `champion_key_by_id(value)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Convert champion id to key

> ## `champion_key_by_name(value)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Convert champion name to key

> ## `champion_name_by_id(value)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Convert champion id to name

> ## `champion_name_by_key(value)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Convert champion key to name

### Submodule: `time`

> ## `timeit(func_or_coro, iters: int = 1 concurrent: bool = True)` <Badge text="function" type="error" vertical="middle"/>
> Measures the running time of a function or coroutine. Functions/Coroutines with arguments should be passed using `functools.partial`.
> - `iters` <Badge text="param" type="warning" vertical="middle"/> may be passed to specify the amount of repeat executions.
> - `concurrent`<Badge text="param" type="warning" vertical="middle"/> to signify concurrent running of coroutines.

> ## `atimeit(coro, iters: int = 1, concurrent: bool = True)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Awaitable, measures the running time of a coroutine. Coroutines with arguments should be passed using `functools.partial`.
> - `iters` <Badge text="param" type="warning" vertical="middle"/> may be passed to specify the amount of repeat executions.
> - `concurrent`<Badge text="param" type="warning" vertical="middle"/> to signify concurrent running of coroutines.

### Submodule: `objects`

> ## `ptr_cache(expiration=60*60*3, max_entries=2000)` <Badge text="function" type="error" vertical="middle"/>
> Create an PtrCache and return it. Takes the same params as the object class constructor.

> ## `frozen_generator(li)` <Badge text="function" type="error" vertical="middle"/>
> Create a FrozenGenerator and return it. Takes the same params as the object class constructor.

### Submodule: `dicts`

> ## `multi_defaultdict(default: Callable)` <Badge text="function" type="error" vertical="middle"/>
> Create a MultiDefaultDict and return it. Takes the same params as the object class constructor.

> ## `redis_defaultdict(redi: redis.Redis, default: Callable, prefix: str = "")` <Badge text="function" type="error" vertical="middle"/>
> Create a RedisDefaultDict and return it. Takes the same params as the object class constructor.

### Submodule: `lor`

> ## `batch_to_ccac(batch)` <Badge text="function" type="error" vertical="middle"/>
> Converts a Batch object to CardCodeAndCount object.

> ## `ccac_to_batch(ccac: CardCodeAndCount, locale: str = None) -> "Batch"` <Badge text="function" type="error" vertical="middle"/>
> Converts a CardCodeAndCount object to Batch object. `locale` is set if passed.
