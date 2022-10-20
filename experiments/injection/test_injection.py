import sys
from dataclasses import dataclass

import pytest


@dataclass
class FakeJs:
    pass


@dataclass
class FakeTarget:
    value: str = "987"


@dataclass
class FakeEvent:
    target: FakeTarget = FakeTarget()


@pytest.fixture
def fake_event():
    return FakeEvent()


@pytest.fixture(scope="function")
def fake_js():
    """Put a fake js environment in builtins."""

    sys.modules["js"] = __import__("fake_js")
    sys.modules["pyodide"] = __import__("fake_pyodide")
    yield
    sys.modules["js"].reset_module()
    del sys.modules["js"]
    del sys.modules["pyodide"]


def test_initializes_handlers(fake_js):
    """Does the handler install ``js.handlers`` object?"""
    from pyscript_handler import handler
    from fake_js import handlers, document

    assert handlers == {}

    @handler(event="click", element="nothing")
    def some_func():
        pass

    assert "some_func" in handlers
    assert document.listeners["click"] is some_func


def test_injects_inject_no_args(fake_js):
    """The handler asked for nothing."""
    from pyscript_handler import handler
    from fake_js import handlers

    @handler(event="click", element="nothing")
    def some_func():
        return f"the func"

    wrapper = handlers["some_func"]
    result = wrapper(9)
    assert result == "the func"


def test_get_args_event(fake_event):
    from pyscript_handler import get_args

    def some_func(event):
        pass

    args = get_args(some_func, fake_event)
    assert args["event"].target.value == "987"


def test_get_args_target_value(fake_event):
    from pyscript_handler import get_args

    def some_func(target_value):
        pass

    args = get_args(some_func, fake_event)
    assert args["target_value"] == "987"


def test_get_args_target_value_coercion(fake_js, fake_event):
    """Use a type hint to convert string to int."""
    from pyscript_handler import get_args

    def some_func(target_value: int):
        pass

    args = get_args(some_func, fake_event)
    assert args["target_value"] == 987


def test_injects_inject_event(fake_js, fake_event):
    """The handler asked for the event."""
    from pyscript_handler import handler
    from fake_js import handlers

    @handler(event="click", element="nothing")
    def some_func(event: FakeEvent):
        return f"the func {event.target.value}"

    wrapper = handlers["some_func"]
    result = wrapper(fake_event)
    assert result == "the func 987"


def test_injects_inject_target_value(fake_js, fake_event):
    """The handler asked for something on the event."""
    from pyscript_handler import handler
    from fake_js import handlers

    @handler(event="click", element="nothing")
    def some_func(target_value):
        return f"the func {target_value}"

    wrapper = handlers["some_func"]
    result = wrapper(fake_event)
    assert result == "the func 987"
