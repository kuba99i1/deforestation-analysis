import cv2
import numpy as np
import rasterio
import matplotlib.pyplot as plt

#  RGB 
def equalize_hist_hsv(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def split_rgb(img):
    img = img.astype(np.float32)
    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    return r, g, b


def calculate_vari(img):
    r, g, b = split_rgb(img)
    vari = (g - r) / (g + r - b)
    vari[~np.isfinite(vari)] = 0
    return vari


def calculate_gli(img):
    r, g, b = split_rgb(img)
    gli = (2 * g - r - b) / (2 * g + r + b)
    gli[~np.isfinite(gli)] = 0
    return gli


def calculate_vigreen(img):
    r, g, _ = split_rgb(img)
    vi = (g - r) / (g + r)
    vi[~np.isfinite(vi)] = 0
    return vi


def threshold_index(index, t):
    return (index > t).astype(np.uint8)


def vegetation_percent(mask):
    return np.count_nonzero(mask) / mask.size * 100


#  NDVI 
def read_red_nir(path):
    with rasterio.open(path) as src:
        red = src.read(3).astype(np.float32)
        nir = src.read(4).astype(np.float32)
    return red, nir


def calculate_ndvi(red, nir):
    ndvi = (nir - red) / (nir + red)
    ndvi[~np.isfinite(ndvi)] = 0
    return ndvi


def threshold_ndvi(ndvi, t):
    ndvi_blur = cv2.GaussianBlur(ndvi, (5, 5), 0)
    return (ndvi_blur > t).astype(np.uint8)


def plot_wskaznik(dane, nazwa, vmin, vmax, lata=[1985, 1993, 2001, 2011]):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, (obraz, rok) in zip(axes.flat, zip(dane, lata)):
        im = ax.imshow(obraz, cmap="RdYlGn", vmin=vmin, vmax=vmax)
        ax.set_title(f"{rok} - {nazwa}")
        ax.axis("off")
        fig.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.show()

def plot_maska(dane, nazwa, prog, lata=[1985, 1993, 2001, 2011]):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, (maska, rok) in zip(axes.flat, zip(dane, lata)):
        ax.imshow(maska, cmap="gray", vmin=0, vmax=1)
        ax.set_title(f"{rok} - {nazwa} > {prog}")
        ax.axis("off")
    plt.tight_layout()
    plt.show()