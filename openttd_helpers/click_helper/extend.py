def extend(additional_func):
    """
    Extend a function to accept click parameters, which can be included in
    the main click.command() later.

    For usage, see logging_helper / sentry_helper or the examples.
    """

    def decorator(func):
        additional_params = []
        for param in getattr(additional_func, "__click_params__", []):
            additional_params.append(param.name)

        def inner_decorator(**kwargs):
            additional_kwargs = {param: kwargs[param] for param in additional_params}
            additional_func(**additional_kwargs)

            # Remove the kwargs that are consumed by the additional_func
            [kwargs.pop(kwarg) for kwarg in additional_kwargs]

            func(**kwargs)

        inner_decorator.__click_params__ = getattr(func, "__click_params__", []) + getattr(
            additional_func, "__click_params__", []
        )
        inner_decorator.__doc__ = func.__doc__
        return inner_decorator

    return decorator
