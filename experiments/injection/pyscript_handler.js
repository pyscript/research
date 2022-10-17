window.set_value = (target, name, value) => {
    target[name] = value;
};
window.get_value = (target, name) => {
    return target[name];
};
window.py = new Proxy(
    {
        get: get_value,
        set: set_value
    },
    {
        get: function (target, prop, receiver) {
            if (target.handlers !== window.handlers) {
                target.handlers = window.handlers;
            }
            if (prop in target) {
                return Reflect.get(...arguments);
            }
            if (prop in target.handlers) {
                return target.handlers[prop];
            } else {
                throw new Error("No handler exists");
            }
        }
    }
);