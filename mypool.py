#!/usr/bin/env python3
import numpy as np
import netCDF4 as nc
from PIL import Image
import matplotlib.pyplot as plt


def pool(img, whs=2, pool_func=np.std, pool_func_kwargs={}):
    # allocating
    ws = 2*whs
    rows, cols = img.shape
    assert not (ws>rows and ws>cols)
    pool_rows = rows//ws + (rows-whs)//ws
    pool_cols = cols//ws + (cols-whs)//ws
    extra_col, extra_row = 0, 0
    if rows%whs != 0 and (rows-whs)%whs != 0: extra_row=1
    if cols%whs != 0 and (cols-whs)%whs != 0: extra_col=1
    pooling_layer = np.empty((pool_rows+extra_row, pool_cols+extra_col))

    for xpi in range(pool_cols):
        xi = whs*xpi
        xf = xi + ws
        for ypi in range(pool_rows):
            yi = whs*ypi
            yf = yi + ws
            subimg = img[yi:yf,xi:xf]
            pooling_layer[ypi, xpi] = pool_func(subimg, **pool_func_kwargs)
        if extra_row != 0:
            ypi += 1
            subimg = img[-ws:,xi:xf]
            pooling_layer[ypi, xpi] = pool_func(subimg, **pool_func_kwargs)

    if extra_col != 0:
        xpi += 1
        for ypi in range(pool_rows):
            yi = whs*ypi
            yf = yi + ws
            subimg = img[yi:yf,-ws:]
            pooling_layer[ypi, xpi] = pool_func(subimg, **pool_func_kwargs)
    return(pooling_layer)



whs = 64
pool_func = np.ptp
img = np.asarray(Image.open('img.jpg'))


img_pool0 = pool(img[:,:,0], whs, pool_func)
img_pool = np.empty((img_pool0.shape[0], img_pool0.shape[1], 3))
img_pool[:,:,0] = img_pool0
del img_pool0
img_pool[:,:,1] = pool(img[:,:,1], whs, pool_func)
img_pool[:,:,2] = pool(img[:,:,2], whs, pool_func)
img_pool /= np.max(img_pool)
#print(np.max(img_pool))
#print(img_pool)

fig, axes = plt.subplots(2,1)
axes[0].imshow(img)
axes[1].imshow(img_pool)
plt.show()
