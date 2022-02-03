# Logging 

Module: `pyot.utils.logging` 

### _class_ Logger

> Lazy logger which its `log()` method will do nothing if level equals 0

Extends: 
* `logging.Logger` 
* `logging.Filterer` 

Definitions: 
* `__init__` -> `None` 
  * `name`: `None` 
* `__reduce__` -> `None` 
* `__repr__` -> `None` 

Methods: 
* _method_ `addFilter` -> `None` 
  * `filter`: `None` 
  > Add the specified filter to this handler. 
* _method_ `addHandler` -> `None` 
  * `hdlr`: `None` 
  > Add the specified handler to this logger. 
* _method_ `callHandlers` -> `None` 
  * `record`: `None` 
  > Pass a record to all relevant handlers.
  > 
  > Loop through all handlers for this logger and its parents in the
  > logger hierarchy. If no handler was found, output a one-off error
  > message to sys.stderr. Stop searching up the hierarchy whenever a
  > logger with the "propagate" attribute set to zero is found - that
  > will be the last logger whose handlers are called. 
* _method_ `critical` -> `None` 
  * `msg`: `None` 
  * `args`: `None` 
  * `kwargs`: `None` 
  > Log 'msg % args' with severity 'CRITICAL'.
  > 
  > To pass exception information, use the keyword argument exc_info with
  > a true value, e.g.
  > 
  > logger.critical("Houston, we have a %s", "major disaster", exc_info=1) 
* _method_ `debug` -> `None` 
  * `msg`: `None` 
  * `args`: `None` 
  * `kwargs`: `None` 
  > Log 'msg % args' with severity 'DEBUG'.
  > 
  > To pass exception information, use the keyword argument exc_info with
  > a true value, e.g.
  > 
  > logger.debug("Houston, we have a %s", "thorny problem", exc_info=1) 
* _method_ `error` -> `None` 
  * `msg`: `None` 
  * `args`: `None` 
  * `kwargs`: `None` 
  > Log 'msg % args' with severity 'ERROR'.
  > 
  > To pass exception information, use the keyword argument exc_info with
  > a true value, e.g.
  > 
  > logger.error("Houston, we have a %s", "major problem", exc_info=1) 
* _method_ `exception` -> `None` 
  * `msg`: `None` 
  * `args`: `None` 
  * `exc_info`: `bool = True` 
  * `kwargs`: `None` 
  > Convenience method for logging an ERROR with exception information. 
* _method_ `fatal` -> `None` 
  * `msg`: `None` 
  * `args`: `None` 
  * `kwargs`: `None` 
  > Log 'msg % args' with severity 'CRITICAL'.
  > 
  > To pass exception information, use the keyword argument exc_info with
  > a true value, e.g.
  > 
  > logger.critical("Houston, we have a %s", "major disaster", exc_info=1) 
* _method_ `filter` -> `None` 
  * `record`: `None` 
  > Determine if a record is loggable by consulting all the filters.
  > 
  > The default is to allow the record to be logged; any filter can veto
  > this and the record is then dropped. Returns a zero value if a record
  > is to be dropped, else non-zero.
  > 
  > .. versionchanged:: 3.2
  > 
  >    Allow filters to be just callables. 
* _method_ `findCaller` -> `None` 
  * `stack_info`: `bool = False` 
  * `stacklevel`: `int = 1` 
  > Find the stack frame of the caller so that we can note the source
  > file name, line number and function name. 
* _method_ `getChild` -> `None` 
  * `suffix`: `None` 
  > Get a logger which is a descendant to this one.
  > 
  > This is a convenience method, such that
  > 
  > logging.getLogger('abc').getChild('def.ghi')
  > 
  > is the same as
  > 
  > logging.getLogger('abc.def.ghi')
  > 
  > It's useful, for example, when the parent logger is named using
  > __name__ rather than a literal string. 
* _method_ `getEffectiveLevel` -> `None` 
  > Get the effective level for this logger.
  > 
  > Loop through this logger and its parents in the logger hierarchy,
  > looking for a non-zero logging level. Return the first one found. 
* _method_ `handle` -> `None` 
  * `record`: `None` 
  > Call the handlers for the specified record.
  > 
  > This method is used for unpickled records received from a socket, as
  > well as those created locally. Logger-level filtering is applied. 
* _method_ `hasHandlers` -> `None` 
  > See if this logger has any handlers configured.
  > 
  > Loop through all handlers for this logger and its parents in the
  > logger hierarchy. Return True if a handler was found, else False.
  > Stop searching up the hierarchy whenever a logger with the "propagate"
  > attribute set to zero is found - that will be the last logger which
  > is checked for the existence of handlers. 
* _method_ `info` -> `None` 
  * `msg`: `None` 
  * `args`: `None` 
  * `kwargs`: `None` 
  > Log 'msg % args' with severity 'INFO'.
  > 
  > To pass exception information, use the keyword argument exc_info with
  > a true value, e.g.
  > 
  > logger.info("Houston, we have a %s", "interesting problem", exc_info=1) 
* _method_ `isEnabledFor` -> `None` 
  * `level`: `None` 
  > Is this logger enabled for level 'level'? 
* _method_ `log` -> `None` 
  * `level`: `None` 
  * `msg`: `None` 
  > Same as logging.Logger.log, with a new level (0) to skip logging. 
* _method_ `makeRecord` -> `None` 
  * `name`: `None` 
  * `level`: `None` 
  * `fn`: `None` 
  * `lno`: `None` 
  * `msg`: `None` 
  * `args`: `None` 
  * `exc_info`: `None` 
  * `func`: `None` 
  * `extra`: `None` 
  * `sinfo`: `None` 
  > A factory method which can be overridden in subclasses to create
  > specialized LogRecords. 
* _method_ `removeFilter` -> `None` 
  * `filter`: `None` 
  > Remove the specified filter from this handler. 
* _method_ `removeHandler` -> `None` 
  * `hdlr`: `None` 
  > Remove the specified handler from this logger. 
* _method_ `setLevel` -> `None` 
  * `level`: `None` 
  > Set the logging level of this logger.  level must be an int or a str. 
* _method_ `warn` -> `None` 
  * `msg`: `None` 
  * `args`: `None` 
  * `kwargs`: `None` 
* _method_ `warning` -> `None` 
  * `msg`: `None` 
  * `args`: `None` 
  * `kwargs`: `None` 
  > Log 'msg % args' with severity 'WARNING'.
  > 
  > To pass exception information, use the keyword argument exc_info with
  > a true value, e.g.
  > 
  > logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1) 


