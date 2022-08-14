# Single File

Characteristics:
- Structure: Single File.
- Threading: Single Threaded.

Pros:
- Playground style, easy for testing small features.

Cons:
- Conf and working code mixed together, reducing code readability.
- Some linters may complain about `wrong-import-order`, due to conf must be placed before `from pyot.models import ...`. Can be disabled in linter conf files (e.g. `.pylintrc`)

## Structure

!!!File=main.py

## Run

```
python main.py <summoner_name>
```
