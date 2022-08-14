# Multi Root

Characteristics:
- Structure: Multi Root.
- Threading: Single Threaded.

Pros:
- Playground style, easy for testing small features.
- Conf and working code are in separate files.

Cons:
- Some linters may complain about `wrong-import-order`, due to conf must be placed before `from pyot.models import ...`. Can be disabled in linter conf files (e.g. `.pylintrc`) or use python syntax `import ...` instead of `import_confs(...)` but that will cause linters to complain `unused-import`.

## Structure

!!!File=main.py
!!!File=pyotconf.py

## Run

```
python main.py <summoner_name>
```
