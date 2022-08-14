# Module Based

Characteristics:
- Structure: Module based.
- Threading: Single Threaded.

Pros:
- Better code structure for higher maintainability.
- Conf imports is handled by `__init__.py` only for cleaner imports.
- Although not used in this example, using `__main__.py` may be more elegant in some situations.

Cons:
- No significant cons.

## Structure

!!!File=module/__init__.py
!!!File=module/pyotconf.py
!!!File=module/tasks.py
!!!File=main.py

## Run

```
python main.py <summoner_name>
```
