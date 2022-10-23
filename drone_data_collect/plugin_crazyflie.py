import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from loguru import logger

from hooks import hookimpl


@hookimpl
def connect_drone(drone_config: dict) -> bool:
    uri = drone_config["uri"]
    logger.info(f"Trying to connect drone at {uri}")
    return True


@hookimpl
def start_logger(logger_config: dict) -> bool:
    logger.info("logger for crazyflie started.")
    return True


@hookimpl
def tick_logger(logger_config: dict) -> bool:
    logger.debug("Tick!")
    return True


@hookimpl
def send_command(command: dict) -> bool:
    _command = command["command"]
    logger.debug(f"sending command {_command}")
    return True
