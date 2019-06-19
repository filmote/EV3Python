DEBUG_NONE                                  = (1 << 0)
DEBUG                                       = (1 << 1)
DEBUG_THREAD_LIFECYCLE                      = (1 << 2)

DEBUG_MOVEMENT_ROTATION                     = (1 << 20)
DEBUG_MOVEMENT_ROTATION_CURRENT_POSITION    = (1 << 21)
DEBUG_MOVEMENT_ROTATION_ALL                 = DEBUG_MOVEMENT_ROTATION | DEBUG_MOVEMENT_ROTATION_CURRENT_POSITION

# Infrared constants

IR_PROMIXITY_TO_CM_RATIO                    = 1.2


# Colour sensor

COLOUR_TOLERANCE                            = 20
LIFTED_MINIMUM_THRESHOLD                    = 10



# Robot

ROBOT_LIFTED_USE_TOUCH_SENSOR               = 0
ROBOT_LIFTED_USE_COLOUR_SENSOR              = 1
