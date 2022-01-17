import types


def register_utilities_to_app(register_app_func: callable, module_name: types.ModuleType, cls_name: type) -> None:
    for func in module_name.__dict__.values():
        if isinstance(func, cls_name):
            # print(f'{func}')
            register_app_func(func)
