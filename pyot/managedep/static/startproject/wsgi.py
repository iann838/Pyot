
from pyot.management.apps import Application

# Instantiate an Application. Usage:
# `app.task(<task-name>)` add a task.
# `app.routes.view(<path>)` add an aiohttp class based view.
# `app.routes.<http-method>(<path>)` add an aiohttp function based view.

app = Application()
