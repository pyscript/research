from pyscript_handler import handler
# noinspection PyUnresolvedReferences
import js


@handler
def foo():
    js.console.log("foo called")


@handler
def boo(e):
    js.console.log("boo called with event")
    js.console.log(e)


@handler
def loo(*e):
    js.console.log("loo called with *event")
    js.console.log(e[0])
    js.console.log(e[1])


@handler(event="click")
def doc_click(*e):
    js.console.log("doc_click called with *event")
    js.console.log(e[0])


@handler(event="mousemove", element=Element("empty_button").element)
def button_mousemove(*e):
    js.console.log("button_mousemove called with *event")
    js.console.log(e[0])
