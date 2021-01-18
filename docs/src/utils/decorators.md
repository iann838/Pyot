# Decorators

## `cached_property`
> Ported from `django.utils.functional`, when the property is accessed it will be cached for the instance lifetime, thus avoiding repeated execution of the property method. Note: This does not replace `property`.

## `silence_event_loop_closed`
> Silences the Exception `RuntimeError: Event loop is closed` in a class method.

## `async_to_sync`
> Wraps `asyncio.run` on an async function making it sync callable.
