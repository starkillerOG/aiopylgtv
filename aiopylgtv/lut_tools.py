import numpy as np

def unity_lut_1d():
    lutmono = np.arange(0, 32768, 32, dtype=np.uint16)
    lut = np.stack([lutmono]*3, axis=0)
    return lut

def unity_lut_3d(n=33):
    spacing = complex(0,n)
    lut = np.mgrid[0.:4095.:spacing,0.:4095.:spacing,0.:4095.:spacing]
    lut = np.rint(lut).astype(np.uint16)
    lut = np.transpose(lut, axes=(1,2,3,0))
    lut = np.flip(lut, axis=-1)
    return lut

def read_cube_file(filename):
    nheader = 0
    lut_1d_size = None
    lut_3d_size = None
    domain_min = None
    domain_max = None
    with open(filename, "r") as f:
        for line in f:
            icomment = line.find("#")
            if icomment>=0:
                line = line[:icomment]
            
            splitline = line.split()
            if splitline:
                keyword = splitline[0]
            else:
                keyword = None
                
            if keyword is None:
                pass
            elif keyword == "TITLE":
                pass
            elif keyword == "LUT_1D_SIZE":
                lut_1d_size = int(splitline[1])
                if lut_1d_size<2 or lut_1d_size>65536:
                    raise ValueError(f"Invalid value {lut_1d_size} for LUT_1D_SIZE, must be in range [2,65536].")
            elif keyword == "LUT_3D_SIZE":
                lut_3d_size = int(splitline[1])
                if lut_3d_size<2 or lut_3d_size>256:
                    raise ValueError(f"Invalid value {lut_3d_size} for LUT_3D_SIZE, must be in range [2,256].")
            elif keyword == "DOMAIN_MIN":
                domain_min = np.genfromtxt([line], usecols=(1,2,3), dtype=np.float64)
                if domain_min.shape != (3,):
                    raise ValueError("DOMAIN_MIN must provide exactly 3 values.")
                if np.amin(domain_min) < -1e37 or np.amax(domain_min) > 1e37:
                    raise ValueError("Invalid value in DOMAIN_MIN, must be in range [-1e37,1e37].")
            elif keyword == "DOMAIN_MAX":
                domain_max = np.genfromtxt([line], usecols=(1,2,3), dtype=np.float64)
                if domain_max.shape != (3,):
                    raise ValueError("DOMAIN_MIN must provide exactly 3 values.")
                if np.amin(domain_max) < -1e37 or np.amax(domain_max) > 1e37:
                    raise ValueError("Invalid value in DOMAIN_MAX, must be in range [-1e37,1e37].")
            else:
                break
            
            nheader += 1
    
    if lut_1d_size and lut_3d_size:
        raise ValueError("Cannot specify both LUT_1D_SIZE and LUT_3D_SIZE.")
    
    if not lut_1d_size and not lut_3d_size:
        raise ValueError("Must specify one of LUT_1D_SIZE or LUT_3D_SIZE.")
    
    if domain_min is None:
        domain_min = np.zeros((3,), dtype=np.float64)
        
    if domain_max is None:
        domain_max = np.ones((3,), dtype=np.float64)
        
    lut = np.genfromtxt(filename, skip_header=nheader, comments="#", dtype=np.float64)
    if np.amin(lut) < -1e37 or np.amax(lut) > 1e37:
        raise ValueError("Invalid value in DOMAIN_MAX, must be in range [-1e37,1e37].")
    
    domain_min = np.reshape(domain_min, (1,3))
    domain_max = np.reshape(domain_max, (1,3))
    
    #shift and scale lut to range [0.,1.]
    lut = (lut-domain_min)/domain_max
    
    if lut_1d_size:
        if lut.shape != (lut_1d_size,3):
            raise ValueError(f"Expected shape {(lut_1d_size,3)} for 1D LUT, but got {lut.shape}.")
        #convert to integer with appropriate range
        lut = np.rint(lut*32767.).astype(np.uint16)
        #transpose to get the correct element order
        lut = np.transpose(lut)
    elif lut_3d_size:
        if lut.shape != (lut_3d_size**3, 3):
            raise ValueError(f"Expected shape {(lut_3d_size**3, 3)} for 3D LUT, but got {lut.shape}.")
        lut = np.reshape(lut, (lut_3d_size, lut_3d_size, lut_3d_size, 3))
        lut = np.rint(lut*4095.).astype(np.uint16)
        
    return lut

def read_cal_file(filename):
    nheader = 0
    with open(filename, "r") as f:
        caldata = f.readlines()
    
    dataidx = caldata.index("BEGIN_DATA\n")
    lut_1d_size_in = int(caldata[dataidx-1].split()[1])
    
    lut = np.genfromtxt(caldata[dataidx+1:dataidx+1+lut_1d_size_in], dtype=np.float64)
    
    if lut.shape != (lut_1d_size_in,4):
        raise ValueError(f"Expected shape {(lut_1d_size_in,3)} for 1D LUT, but got {lut.shape}.")

    lut_1d_size = 1024
    
    #interpolate if necessary
    if lut_1d_size_in != lut_1d_size:
        x = np.linspace(0., 1., lut_1d_size, dtype=np.float64)
        lutcomponents = []
        for i in range(1,4):
            lutcomponent = np.interp(x, lut[:,0], lut[:,i])
            lutcomponents.append(lutcomponent)
        lut = np.stack(lutcomponents, axis=-1)
    else:
        lut = lut[:,1:]
        
    #convert to integer with appropriate range
    lut = np.rint(32767.*lut).astype(np.uint16)
    #transpose to get the correct element order
    lut = np.transpose(lut)
            
    return lut
