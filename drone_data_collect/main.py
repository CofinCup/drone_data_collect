import asyncio

import pluggy
import itertools
import toml
from pathlib import Path
from loguru import logger

import hooks
import plugin_crazyflie


class Host:
    __slots__ = ["hook", ]  # 减少自身attribute

    def __init__(self, hook):
        self.hook = hook

    def host_connect_drone(self, drone_config: dict):
        logger.info("Connecting drone...")
        results: list = self.hook.connect_drone(drone_config=drone_config)
        clear: bool = False not in list(itertools.chain(results))
        if clear:
            logger.info("Drone connected, all clear")
        else:
            logger.error("Drone not connected.")
            raise RuntimeError("Drone not connected.")

    def host_start_logger(self, logger_config: dict):
        logger.info("Starting custom loggers...")
        results: list = self.hook.start_logger(logger_config=logger_config)
        clear: bool = False not in list(itertools.chain(results))
        if clear:
            logger.info("Customized loggers started.")
        else:
            logger.error("Customized loggers failed.")
            raise RuntimeError("Logger failed.")

    def host_tick_logger(self, logger_config: dict):
        logger.debug("Ticking loggers...")
        results: list = self.hook.tick_logger(logger_config=logger_config)
        clear: bool = False not in list(itertools.chain(results))
        if not clear:
            logger.error("Cusomized logger ticks failed.")
            raise RuntimeError("Logger failed.")

    def send_command(self, command: dict):
        logger.debug(f"Sending one command: {command}")
        results: list = self.hook.send_command(command=command)
        clear: bool = False not in list(itertools.chain(results))
        if not clear:
            logger.error("Command send failed.")
            raise RuntimeError("Command send failed.")


def get_plugin_manager() -> pluggy.PluginManager:
    pm = pluggy.PluginManager("drone_data_collect")
    pm.add_hookspecs(hooks)
    pm.register(plugin_crazyflie)
    return pm


async def timer(time: float) -> None:
    await asyncio.sleep(time)


async def drone_task_one_loop(host, config):
    """
    add command calculation here
    """
    host.send_command(command={"command": [1, 1, 1]})
    host.host_tick_logger(logger_config=config["logger"])


async def main() -> None:
    config = toml.load(str(Path(__file__).parent / "config.toml"))
    pm: pluggy.PluginManager = get_plugin_manager()
    host = Host(pm.hook)
    host.host_connect_drone(drone_config=config["drone"])
    host.host_start_logger(logger_config=config["logger"])
    for i in range(5):
        await asyncio.gather(timer(0.1), drone_task_one_loop(host, config))
        logger.info("finish one loop")


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
