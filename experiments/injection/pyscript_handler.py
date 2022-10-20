from inspect import signature
from typing import get_type_hints

# noinspection PyUnresolvedReferences
import js

# noinspection PyUnresolvedReferences
from pyodide.ffi import create_proxy


def get_args(func, evt):
    """Inspect the target and prepare some args to call with."""
    args = {}
    sig = signature(func)
    hints = get_type_hints(func)
    for param_name, param_value in sig.parameters.items():
        if param_name == "event":
            args["event"] = evt
        else:
            # Try some convention. For example, underscores
            # imply dotted access.
            dotted = param_name.split("_")
            # We'd do recursion here, for now, hardwire.
            first = getattr(evt, dotted[0])
            param_value = getattr(first, dotted[1])

            # Some simple type coercion, just for illustration.
            param_type = hints.get(param_name)
            if param_type is int:
                param_value = int(param_value)
            args[param_name] = param_value
    return args


def handler(_func=None, *, event=None, element: str | None, options=None):
    if not js.hasOwnProperty("handlers"):
        js.handlers = js.Object.new()

    def decorator(func):
        def wrapper(evt):
            args = get_args(func, evt)
            return func(**args)

        proxy = create_proxy(wrapper)
        js.set_value(js.handlers, func.__name__, proxy)
        if event:
            this_element = js.document.querySelector(element)
            this_element.addEventListener(event, proxy, options)
        return wrapper

    return decorator
