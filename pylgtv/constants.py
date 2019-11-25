import numpy as np
DEFAULT_CAL_DATA_ENCODED = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4C2QO36MOb19P4U/"
DEFAULT_CAL_DATA = np.array([0.,0.,0.,0.,0.,0.,0.0044,-0.0453,1.041],dtype=np.float32)

UNITY_1D_LUT_MONOCHROME = np.arange(0, 32768, 32, dtype=np.uint16)
UNITY_1D_LUT = np.stack( (UNITY_1D_LUT_MONOCHROME,UNITY_1D_LUT_MONOCHROME,UNITY_1D_LUT_MONOCHROME), axis=0)
DEFAULT_1D_LUT = UNITY_1D_LUT

UNITY_3D_LUT = np.mgrid[0:4096:33j,0:4096:33j,0:4096:33j].astype(np.uint16)
UNITY_3D_LUT = np.clip(UNITY_3D_LUT, 0, 4095)
UNITY_3D_LUT = np.transpose(UNITY_3D_LUT, axes=(1,2,3,0))
UNITY_3D_LUT = np.flip(UNITY_3D_LUT, axis=-1)

CALIBRATION_TYPE_MAP = { np.uint8 : "unsigned char", np.uint16 : "unsigned integer16", np.float32 : "float" }

#print(UNITY_1D_LUT)
#print(UNITY_3D_LUT)

#print(UNITY_3D_LUT.shape)

#for i in range(33):
    #print(UNITY_3D_LUT[i,0,0])
