"""Mock the JS."""
from dataclasses import dataclass, field

handlers = {}


@dataclass
class Object:
    @classmethod
    def new(cls):
        return {}


@dataclass
class Document:
    listeners: dict[str, object] = field(default_factory=dict)

    def querySelector(self, selector):
        return Element()

    def addEventListener(self, event: str, proxy, options):
        document.listeners[event] = proxy


Element = Document

document = Document()


def hasOwnProperty(key: str):  # noqa
    return isinstance(handlers, dict)


def set_value(target, function_name, callable_):
    target[function_name] = callable_


def reset_module():
    """Everything needed from test to test."""

    global handlers
    handlers = {}
