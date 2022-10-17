# noinspection PyUnresolvedReferences
import js

from pyscript_handler import handler


@handler(event="click", element="#btn1")
def foo(event):
    js.console.log("foo called", event)


@handler(event="click", element="#input1")
def boo(target_value: int):
    new_value = target_value - 23
    js.console.log("boo called with target value", new_value)
