import pluggy

hookspec = pluggy.HookspecMarker("drone_data_collect")  # 钩子函数标注装饰器
hookimpl = pluggy.HookimplMarker("drone_data_collect")  # 钩子函数实现装饰器


@hookspec
def connect_drone(drone_config: dict) -> bool:
    """
    establish the connection between drone and host
    """


@hookspec
def start_logger(logger_config: dict) -> bool:
    """
    start logging (enableing customized config)
    """


@hookspec
def tick_logger(logger_config: dict) -> bool:
    """
    record one piece of logging
    """


@hookspec
def send_command(command: dict) -> bool:
    """
    send one command to drone
    """
