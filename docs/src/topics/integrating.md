# Integrating to another framework or environment

This **base template** generated using `pyot startproject` is not limited to that template, if you're integrating pyot to other frameworks (e.g. Flask, FastAPI), you can choose to import the tasks written in this module and execute it in your other framework, or integrate pyot to that framework by adding imports and applying settings.

For integrating in other modules, the procedure will most likely looks like:

1. Create a file that has the pyot settings activated.
2. Make the module, framework to import that file at boost, either by some framework constants (e.g. `INSTALLED_APPS` of django) or adding an import to `__init__.py`
3. Write your functions and methods anywhere you are accessible.
4. Import it on your framework tasks and execute them.
5. Check if `asyncio.run` is compatible with the framework, if not, use `async_to_sync` from `asgiref.sync`.

For example, you can check `pyot.__init__.py` on how is pyot integrated to django.
