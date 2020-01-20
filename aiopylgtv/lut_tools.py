import numpy as np


def unity_lut_1d():
    lutmono = np.linspace(0.0, 32767.0, 1024, dtype=np.float64)
    lut = np.stack([lutmono] * 3, axis=0)
    lut = np.rint(lut).astype(np.uint16)
    return lut


def unity_lut_3d(n=33):
    spacing = complex(0, n)
    endpoint = 4096.0
    lut = np.mgrid[0.0:endpoint:spacing, 0.0:endpoint:spacing, 0.0:endpoint:spacing]
    lut = np.rint(lut).astype(np.uint16)
    lut = np.clip(lut, 0, 4095)
    lut = np.transpose(lut, axes=(1, 2, 3, 0))
    lut = np.flip(lut, axis=-1)
    return lut


def read_cube_file(filename):  # noqa: C901
    nheader = 0
    lut_1d_size = None
    lut_3d_size = None
    domain_min = None
    domain_max = None

    with open(filename) as f:
        lines = f.readlines()

    def domain_check(line, which):
        domain_limit = np.genfromtxt([line], usecols=(1, 2, 3), dtype=np.float64)
        if domain_limit.shape != (3,):
            raise ValueError(f"DOMAIN_{which} must provide exactly 3 values.")
        if np.amin(domain_limit) < -1e37 or np.amax(domain_limit) > 1e37:
            raise ValueError(
                f"Invalid value in DOMAIN_{which}, must be in range [-1e37,1e37]."
            )
        return domain_limit

    def lut_size(splitline, dim):
        lut_size = int(splitline[1])
        upper_limit = {1: 65536, 3: 256}[dim]
        if lut_size < 2 or lut_size > upper_limit:
            raise ValueError(
                f"Invalid value {lut_size} for LUT_{dim}D_SIZE,"
                f" must be in range [2, {upper_limit}]."
            )
        return lut_size

    for line in lines:
        icomment = line.find("#")
        if icomment >= 0:
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
            lut_1d_size = lut_size(splitline, dim=1)
        elif keyword == "LUT_3D_SIZE":
            lut_3d_size = lut_size(splitline, dim=3)
        elif keyword == "DOMAIN_MIN":
            domain_min = domain_check(line, "MIN")
        elif keyword == "DOMAIN_MAX":
            domain_max = domain_check(line, "MAX")
        else:
            break

        nheader += 1

    if lut_1d_size and lut_3d_size:
        raise ValueError("Cannot specify both LUT_1D_SIZE and LUT_3D_SIZE.")

    if not lut_1d_size and not lut_3d_size:
        raise ValueError("Must specify one of LUT_1D_SIZE or LUT_3D_SIZE.")

    if domain_min is None:
        domain_min = np.zeros((1, 3), dtype=np.float64)

    if domain_max is None:
        domain_max = np.ones((1, 3), dtype=np.float64)

    lut = np.genfromtxt(lines[nheader:], comments="#", dtype=np.float64)
    if np.amin(lut) < -1e37 or np.amax(lut) > 1e37:
        raise ValueError("Invalid value in DOMAIN_MAX, must be in range [-1e37,1e37].")

    # shift and scale lut to range [0.,1.]
    lut = (lut - domain_min) / (domain_max - domain_min)

    if lut_1d_size:
        if lut.shape != (lut_1d_size, 3):
            raise ValueError(
                f"Expected shape {(lut_1d_size, 3)} for 1D LUT, but got {lut.shape}."
            )
        # convert to integer with appropriate range
        lut = np.rint(lut * 32767.0).astype(np.uint16)
        # transpose to get the correct element order
        lut = np.transpose(lut)
    elif lut_3d_size:
        if lut.shape != (lut_3d_size ** 3, 3):
            raise ValueError(
                f"Expected shape {(lut_3d_size**3, 3)} for 3D LUT, but got {lut.shape}."
            )
        lut = np.reshape(lut, (lut_3d_size, lut_3d_size, lut_3d_size, 3))
        lut = np.rint(lut * 4096.0).astype(np.uint16)
        lut = np.clip(lut, 0, 4095)
    return lut


def read_cal_file(filename):
    with open(filename, "r") as f:
        caldata = f.readlines()

    dataidx = caldata.index("BEGIN_DATA\n")
    lut_1d_size_in = int(caldata[dataidx - 1].split()[1])

    lut = np.genfromtxt(
        caldata[dataidx + 1 : dataidx + 1 + lut_1d_size_in], dtype=np.float64
    )

    if lut.shape != (lut_1d_size_in, 4):
        raise ValueError(
            f"Expected shape {(lut_1d_size_in,3)} for 1D LUT, but got {lut.shape}."
        )

    lut_1d_size = 1024

    # interpolate if necessary
    if lut_1d_size_in != lut_1d_size:
        x = np.linspace(0.0, 1.0, lut_1d_size, dtype=np.float64)
        lutcomponents = [np.interp(x, lut[:, 0], lut[:, i]) for i in range(1, 4)]
        lut = np.stack(lutcomponents, axis=-1)
    else:
        lut = lut[:, 1:]

    # convert to integer with appropriate range
    lut = np.rint(32767.0 * lut).astype(np.uint16)
    # transpose to get the correct element order
    lut = np.transpose(lut)

    return lut
