import numpy as np

CALIBRATION_TYPE_MAP = {
    "uint8": "unsigned char",
    "uint16": "unsigned integer16",
    "float32": "float",
}
DEFAULT_CAL_DATA = np.array(
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0044, -0.0453, 1.041], dtype=np.float32
)
