# Handler DI

Give handler functions a more Pythonic function signature.

## The Problem

We'd like to make writing PyScript apps friendly from a DX-perspective.
Tooling such as IDEs can help with autocomplete.
But some parts of the JS/Python bridge isn't friendly to typing.
For example, a handler function's `event` argument.

## The Proposal

In this experiment we work around this by letting people ask for the event value by name as a function parameter.
If they add a type hint, we try (in a limited fashion) to "cast" it.

For example, instead of this:

```python
@handler(event="mousemove", element=Element("empty_button").element )
def update_todo_status(e):
    todo_id = e.target.getAttribute("id")
    todo_input_value = e.target.value
    update_todo(todo_id, todo_input_value)
```

...you would instead say:

```
@handler(event="mousemove", element=Element("empty_button").element )
def update_todo_status(target_id: str, target_value: int):
    todo_id = e.target.getAttribute("id")
    todo_input_value = int(e.target.value)
    update_todo(todo_id, todo_input_value)
```

In a word: simple dependency injection.
This function is now super-easy to test in `pytest`, as it isn't tied to the JS engine at all.

PyScript would provide a set of well-known, frequently-used parts of the event object that people were interested in.
We'd then use those as keys to functions that plucked the value.
If the person provided a type hint on the function parameter, PyScript would try to coerce it.

What if you liked this, but wanted something off the event PyScript didn't provide?
What if the type coercion wasn't quite right?
What if people wanted to ship some really cool mediator stuff?
We could use either descriptors, generics, or `Annotated`, as being done in Textual and other systems:

```
@handler(event="mousemove", element=Element("empty_button").element )
def update_todo_status(targetId: str, targetValue: TargetValue[str]):
    update_todo(todo_id, todo_input_value)
```

This gives some of the benefit that people like from FastAPI, where the mediation by the framework, before calling user code.

## Related Ideas

- *Performance*. We could take the signature information over to the JS side and only call the function if the requested values changed from the last call.
