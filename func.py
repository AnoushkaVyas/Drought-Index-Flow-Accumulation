from pysheds.grid import Grid
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import os

# Flow direction and acumulation

def setGlobals():
    global FLOW_DIR
    FLOW_DIR = np.array([32, 64, 128, 16, 0, 1, 8, 4, 2])
    global ROW_OFFSET
    ROW_OFFSET= np.array([-1, -1, -1, 0, 0, 0, 1, 1, 1])
    global COL_OFFSET
    COL_OFFSET = np.array([-1, 0, 1, -1, 0, 1, -1, 0, 1])

def drainsToMe(index, fdir):

    if index == 4:
        return False
    elif index == 0 and fdir == FLOW_DIR[8]:
        return True
    elif index == 1 and fdir == FLOW_DIR[7]:
        return True
    elif index == 2 and fdir == FLOW_DIR[6]:
        return True
    elif index == 3 and fdir == FLOW_DIR[5]:
        return True
    elif index == 5 and fdir == FLOW_DIR[3]:
        return True
    elif index == 6 and fdir == FLOW_DIR[2]:
        return True
    elif index == 7 and fdir == FLOW_DIR[1]:
        return True
    elif index == 8 and fdir == FLOW_DIR[0]:
        return True
    else:
        return False

def getColOffsetAscendingFDIR():
    return np.array([0,1,1,0,-1,-1,-1,0,1])

def getColOffsetIndexed():
    return np.array([-1, 0, 1, -1, 0, 1, -1, 0, 1])

def getFlowDirectionAscending(code = "ESRI"):
    if code == "ESRI":
        return np.array([0,1,2,4,8,16,32,64,128])
    elif code == "TauDEM":
        return None #Needs to be updated
    else:
        return None

def getFlowDirectionIndexed(code = "ESRI"):
    if code == "ESRI":
        return np.array([32, 64, 128, 16, 0, 1, 8, 4, 2])
    elif code == "TauDEM":
        return None #Needs to be updated
    else:
        return None

def getRowOffsetAscendingFDIR():
    return np.array([0,0,1,1,1,0,-1,-1,-1])

def getRowOffsetIndexed():
    return np.array([-1, -1, -1, 0, 0, 0, 1, 1, 1])

def facgroup(dem, fdir, nodata):
    setGlobals()
    group = np.empty((dem.shape[0]+2, dem.shape[1]+2))
    group.fill(0)
    demnew = np.empty((group.shape))
    demnew.fill(nodata)
    demnew[1:-1, 1:-1] = dem
    fdirnew = np.empty((group.shape))
    fdirnew.fill(nodata)
    fdirnew[1:-1, 1:-1] = fdir
    fac = np.empty((group.shape))
    fac.fill(0)
    demnan = dem
    demnan[demnan<0.0] = np.nan

    while np.nanmax(demnew) != nodata:
        cells = np.swapaxes(np.where(demnew == np.nanmax(demnew)), 0, 1)
        for cell in cells:
            demWin = demnew[cell[0]-1:cell[0]+2, cell[1]-1:cell[1]+2].reshape(1, 9)
            fdirWin = fdirnew[cell[0]-1:cell[0]+2, cell[1]-1:cell[1]+2].reshape(1, 9)
            gathers = 0
            maxgather = 0
            accum = 0
            for i in range(0, 9):
                if drainsToMe(i, fdirWin[0, i]):
                    gathers += 1
                    accum += fac[cell[0] + ROW_OFFSET[i], cell[1] + COL_OFFSET[i]] + 1
                    if group[cell[0] + ROW_OFFSET[i], cell[1] + COL_OFFSET[i]] > maxgather:
                        maxgather = group[cell[0] + ROW_OFFSET[i], cell[1] + COL_OFFSET[i]]

            if gathers > 0: group[cell[0], cell[1]] = maxgather + 1
            else: group[cell[0], cell[1]] = 1
            demnew[cell[0], cell[1]] = nodata
            fac[cell[0], cell[1]] = accum

    demnew[1:-1, 1:-1] = dem
    fac = np.where(group == 1, 0, fac)
    fac = np.where(demnew == nodata, nodata, fac)
    group = np.where(demnew == nodata, nodata, group)
    return group[1:-1, 1:-1], fac[1:-1, 1:-1]

def accumStop(array1, array2):
    result = False
    if array1 == array2:
        result = True
    return result

def flowaccum(flowto, groups, nodata):
    fac = np.zeros(flowto.shape)
    index = np.arange(flowto.shape[0] * flowto.shape[1]).reshape(flowto.shape)
    go = True
    ngroup = 1
    while go:
        group = flowto[groups==ngroup]
        if np.array_equal(group, index[groups == ngroup]):
            go = False
            break

        ngroup += 1
        indices, counts = np.unique(group, return_counts=True)
        
        np.put(groups, indices, ngroup)

    fac[flowto==nodata] = nodata
    return fac, groups

def fastfac(fdir, nodata, fdircode = "ESRI"):
    flowto = flowsTo(fdir, nodata, fdircode)
    group = firstGroup(flowto, nodata)
    return

def firstGroup(flowto, nodata):
    lindex = np.arange(flowto.shape[0]*flowto.shape[1])
    group1 = np.in1d(lindex, flowto.ravel(), invert=True)
    group1 = group1.reshape(flowto.shape)
    group1[flowto == nodata] = False
    return np.where(group1, 1, 0)

def getdem(filename):
    grid = Grid.from_raster(filename, data_name='dem')
    return grid, grid.dem

def flowsTo(fdir, nodata, fdircode = "ESRI"):
    """
    Using flow direction, determine the linear index of the cell that each cell flows into
    Args:
        fdir: 2d flow direction array
        nodata: no data value
        fdircode: flow direction encoding, can be either "ESRI" (default) or "TauDEM"
    Returns:
        2d array of linear (1d) indices
    """
    nrow, ncol = fdir.shape  # get number of rows and number of columns
    lindex = np.arange(nrow * ncol) #linear indices
    index = np.digitize(fdir.ravel(), getFlowDirectionAscending(fdircode), right=True) #index of flow direction value (0-8)
    rowoff = getRowOffsetAscendingFDIR()[index] #replace flow direction index with corresponding row offset
    coloff = getColOffsetAscendingFDIR()[index] #replace flow direction index with corresponding column offset
    flowto = (lindex + ncol * rowoff + coloff).reshape(fdir.shape) #add row and column offsets to linear indices to determine which cell each cell flows to
    flowto[fdir==nodata] = nodata #maintain no data values
    return flowto

def flowaccumulation(grid,dirmap):
    grid.accumulation(data='catch', dirmap=dirmap, out_name='acc')
    acc = grid.view('acc', nodata=np.nan) + 1
    return grid, acc

def flowDirectionOutward(dem, nodata): #all edge cells flow outward
    temp = np.empty((dem.shape[0]+2, dem.shape[1]+2)) #create temp array with buffer around dem
    temp.fill(nodata) #fill with value greater than the dem max
    temp[1:-1, 1:-1] = dem #fill in dem values (creates wall so all cells will flow inward)
    dem = temp #set new dem

    fdir = np.zeros(dem.shape)
    gradient = np.empty((8, dem.shape[0] - 2, dem.shape[1] - 2), dtype=np.float)
    code = np.empty(8, dtype=np.int)
    for k in range(8):
        theta = -k * np.pi / 4
        code[k] = 2 ** k
        j, i = np.int(1.5 * np.cos(theta)), -np.int(1.5 * np.sin(theta))
        d = np.linalg.norm([i, j])
        gradient[k] = (dem[1 + i: dem.shape[0] - 1 + i, 1 + j: dem.shape[1] - 1 + j] - dem[1: dem.shape[0] - 1,
                                                                                       1: dem.shape[1] - 1]) / d
    direction = (-gradient).argmax(axis=0)

    fdir[1:-1, 1:-1] = code.take(direction)
    fdir[dem==nodata] = nodata

    return fdir[1:-1, 1:-1]

def flowdirection(filename,grid):
    grid.read_raster(filename, data_name='dir')
    return grid, grid.dir

def flowDirectionTestInward(dem, nodata): #all edge cells flow inward
    temp = np.empty((dem.shape[0]+2, dem.shape[1]+2)) #create temp array with buffer around dem
    temp.fill(nodata) #fill with value greater than the dem max
    temp[1:-1, 1:-1] = dem #fill in dem values (creates wall so all cells will flow inward)
    dem = temp #set new dem

    demfill = np.nanmax(dem)+2.0
    dem[dem == nodata] = demfill

    fdir = np.zeros(dem.shape)
    gradient = np.empty((8, dem.shape[0] - 2, dem.shape[1] - 2), dtype=np.float)
    code = np.empty(8, dtype=np.int)
    for k in range(8):
        theta = -k * np.pi / 4
        code[k] = 2 ** k
        j, i = np.int(1.5 * np.cos(theta)), -np.int(1.5 * np.sin(theta))
        d = np.linalg.norm([i, j])
        gradient[k] = (dem[1 + i: dem.shape[0] - 1 + i, 1 + j: dem.shape[1] - 1 + j] - dem[1: dem.shape[0] - 1,
                                                                                       1: dem.shape[1] - 1]) / d
    direction = (-gradient).argmax(axis=0)

    fdir[1:-1, 1:-1] = code.take(direction)
    #hack to set outlet cell to valid value
    fdir[dem == np.nanmin(dem)] = 0
    fdir[dem == demfill] = nodata

    return fdir[1:-1, 1:-1]

def dilineatecatchmant(dirmap,x,y,grid):
    grid.catchment(data='dir', x=x, y=y, dirmap=dirmap, out_name='catch',recursionlimit=15000, xytype='label', nodata_out=0)
    grid.clip_to('catch')
    catch = grid.view('catch', nodata=np.nan)
    return grid, catch


