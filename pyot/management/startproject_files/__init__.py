
# Imports the settings to use.
try:
    from . import settings
except KeyError as e:
    raise KeyError(str(e)[1:-1] + ", Please check if issue is related to environment variables and reopen the console") from e

# Other imports if needed...
