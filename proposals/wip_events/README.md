# Event implementation

This is an event implementation for HTML and Python in PyScript.

Goals:
 - Suport all JS events without listing or looping
 - Runtime add/remove listeners using on[event] and py-event attributes
 - Support for passing event objects
 - Support for exposing python handlers to js via decorator
 - Support for registering event handlers via decorator
 - Global JS `py` object to allow calling python from js at runtime
 - mutation observer for runtime add/remove of py-event
