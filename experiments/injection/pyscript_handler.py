# noinspection PyUnresolvedReferences
import js
# noinspection PyUnresolvedReferences
from pyodide.ffi import create_proxy


def handler(_func=None, *, event=None, element=js.document, options=None):
    if not js.hasOwnProperty("handlers"):
        js.handlers = js.Object.new()

    def decorator(func):
        proxy = create_proxy(func)
        js.set_value(js.handlers, func.__name__, proxy)
        if event:
            element.addEventListener(event, proxy, options)
        return func

    # just @handler( None, **kargs )
    if _func is None:
        return decorator

    # just @handler
    else:
        js.set_value(js.handlers, _func.__name__, create_proxy(_func))
        return _func
