# import logging
import esphome.config_validation as cv
import esphome.codegen as cg

from esphome.components import climate, uart
from esphome.const import (
    CONF_ID,
    # CONF_SUPPORTED_SWING_MODES,
)
# from esphome.components.climate import (
    # ClimateSwingMode,
# )

CODEOWNERS = ["@bekmansurov"]
DEPENDENCIES = ["climate", "uart"]

gree_ns = cg.esphome_ns.namespace("gree")
GreeClimate = gree_ns.class_(
    "GreeClimate", climate.Climate, cg.PollingComponent, uart.UARTDevice
)

# ALLOWED_CLIMATE_SWING_MODES = {
#     "BOTH": ClimateSwingMode.CLIMATE_SWING_BOTH,
#     "VERTICAL": ClimateSwingMode.CLIMATE_SWING_VERTICAL,
#     "HORIZONTAL": ClimateSwingMode.CLIMATE_SWING_HORIZONTAL,
# }

# validate_swing_modes = cv.enum(ALLOWED_CLIMATE_SWING_MODES, upper=True)

CONFIG_SCHEMA = cv.All(
    climate.CLIMATE_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(GreeClimate),
            # cv.Optional(CONF_SUPPORTED_SWING_MODES): cv.ensure_list(
                # validate_swing_modes
            # ),
        }
    )
    # changed from 5s (based on Haier component)
    .extend(cv.polling_component_schema("10s"))
    .extend(uart.UART_DEVICE_SCHEMA),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)
    await uart.register_uart_device(var, config)
    # if CONF_SUPPORTED_SWING_MODES in config:
        # cg.add(var.set_supported_swing_modes(config[CONF_SUPPORTED_SWING_MODES]))