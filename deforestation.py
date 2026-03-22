import matplotlib.pyplot as plt
import cv2
import numpy as np
import rasterio
from functions import *

sciezka_1985 = r"D:\Studia\II stopien\progtamowanie analityczne\deforestation_analysis\images\1985.png" 
sciezka_1993 = r"D:\Studia\II stopien\progtamowanie analityczne\deforestation_analysis\images\1993.png" 
sciezka_2001 = r"D:\Studia\II stopien\progtamowanie analityczne\deforestation_analysis\images\2001.png" 
sciezka_2011 = r"D:\Studia\II stopien\progtamowanie analityczne\deforestation_analysis\images\2011.png" 


zdj_1985 = cv2.imread(sciezka_1985)
zdj_1993 = cv2.imread(sciezka_1993)
zdj_2001 = cv2.imread(sciezka_2001)
zdj_2011 = cv2.imread(sciezka_2011)


# rgb po eq
zdj_1985_eq = equalize_hist_hsv(zdj_1985)
zdj_1993_eq = equalize_hist_hsv(zdj_1993)
zdj_2001_eq = equalize_hist_hsv(zdj_2001)
zdj_2011_eq = equalize_hist_hsv(zdj_2011)

zdjecia = [
    (zdj_1985_eq, "1985"),
    (zdj_1993_eq, "1993"),
    (zdj_2001_eq, "2001"),
    (zdj_2011_eq, "2011"),
]

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, (zdj, rok) in zip(axes.flat, zdjecia):
    ax.imshow(cv2.cvtColor(zdj, cv2.COLOR_BGR2RGB))
    ax.set_title(f"{rok} - RGB po equalizacji")
    ax.axis("off")

plt.tight_layout()
plt.show()



# VARI
vari_1985 = calculate_vari(zdj_1985)
vari_1993 = calculate_vari(zdj_1993)
vari_2001 = calculate_vari(zdj_2001)
vari_2011 = calculate_vari(zdj_2011)


all_vari = np.concatenate([
    vari_1985.ravel(),
    vari_1993.ravel(),
    vari_2001.ravel(),
    vari_2011.ravel()
])

vmin_vari, vmax_vari = np.percentile(all_vari, [2, 98])


vari_zdjecia = [vari_1985, vari_1993, vari_2001, vari_2011]

plot_wskaznik([vari_1985, vari_1993, vari_2001, vari_2011], "VARI", vmin_vari, vmax_vari)


# GLI
gli_1985 = calculate_gli(zdj_1985)
gli_1993 = calculate_gli(zdj_1993)
gli_2001 = calculate_gli(zdj_2001)
gli_2011 = calculate_gli(zdj_2011)


all_gli = np.concatenate([
    gli_1985.ravel(),
    gli_1993.ravel(),
    gli_2001.ravel(),
    gli_2011.ravel()
])

vmin_gli, vmax_gli = np.percentile(all_gli, [2, 98])

gli_zdjecia = [gli_1985, gli_1993, gli_2001, gli_2011]

plot_wskaznik([gli_1985, gli_1993, gli_2001, gli_2011], "GLI", vmin_gli, vmax_gli)



# VIGREEN
vigreen_1985 = calculate_vigreen(zdj_1985)
vigreen_1993 = calculate_vigreen(zdj_1993)
vigreen_2001 = calculate_vigreen(zdj_2001)
vigreen_2011 = calculate_vigreen(zdj_2011)



all_vigreen = np.concatenate([
    vigreen_1985.ravel(),
    vigreen_1993.ravel(),
    vigreen_2001.ravel(),
    vigreen_2011.ravel()
])

vmin_vigreen, vmax_vigreen = np.percentile(all_vigreen, [2, 98])

plot_wskaznik([vigreen_1985, vigreen_1993, vigreen_2001, vigreen_2011], "GLI", vmin_vigreen, vmax_vigreen)



prog_vari = 0.05
prog_gli = 0.07
prog_vigreen = 0.04



maska_vari_1985 = threshold_index(vari_1985, prog_vari)
maska_vari_1993 = threshold_index(vari_1993, prog_vari)
maska_vari_2001 = threshold_index(vari_2001, prog_vari)
maska_vari_2011 = threshold_index(vari_2011, prog_vari)

plot_maska([maska_vari_1985, maska_vari_1993, maska_vari_2001, maska_vari_2011], "VARI", prog_vari)



maska_gli_1985 = threshold_index(gli_1985, prog_gli)
maska_gli_1993 = threshold_index(gli_1993, prog_gli)
maska_gli_2001 = threshold_index(gli_2001, prog_gli)
maska_gli_2011 = threshold_index(gli_2011, prog_gli)

plot_maska([maska_gli_1985, maska_gli_1993, maska_gli_2001, maska_gli_2011], "GLI", prog_gli)



maska_vigreen_1985 = threshold_index(vigreen_1985, prog_vigreen)
maska_vigreen_1993 = threshold_index(vigreen_1993, prog_vigreen)
maska_vigreen_2001 = threshold_index(vigreen_2001, prog_vigreen)
maska_vigreen_2011 = threshold_index(vigreen_2011, prog_vigreen)

plot_maska([maska_vigreen_1985, maska_vigreen_1993, maska_vigreen_2001, maska_vigreen_2011], "VIGREEN", prog_vigreen)


lata = [1985, 1993, 2001, 2011]

vegetation_vari = [
    vegetation_percent(maska_vari_1985),
    vegetation_percent(maska_vari_1993),
    vegetation_percent(maska_vari_2001),
    vegetation_percent(maska_vari_2011)
]

vegetation_gli = [
    vegetation_percent(maska_gli_1985),
    vegetation_percent(maska_gli_1993),
    vegetation_percent(maska_gli_2001),
    vegetation_percent(maska_gli_2011)
]

vegetation_vigreen = [
    vegetation_percent(maska_vigreen_1985),
    vegetation_percent(maska_vigreen_1993),
    vegetation_percent(maska_vigreen_2001),
    vegetation_percent(maska_vigreen_2011)
]


deforestation_vari = [100 - x for x in vegetation_vari]
deforestation_gli = [100 - x for x in vegetation_gli]
deforestation_vigreen = [100 - x for x in vegetation_vigreen]



plt.figure(figsize=(10, 6))

plt.plot(lata, vegetation_vari, marker="o", linewidth=2, label="VARI")
plt.plot(lata, vegetation_gli, marker="o", linewidth=2, label="GLI")
plt.plot(lata, vegetation_vigreen, marker="o", linewidth=2, label="VIGREEN")

plt.xlabel("Rok")
plt.ylabel("Udział roślinności [%]")
plt.title("Zmiany udziału roślinności w czasie")

plt.ylim(0, 100)  
plt.yticks(np.arange(0, 101, 20))  
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

tiff_1985 = r"D:\Studia\II stopien\progtamowanie analityczne\deforestation_analysis\images_geotiff\1985api.tif"
tiff_1993 = r"D:\Studia\II stopien\progtamowanie analityczne\deforestation_analysis\images_geotiff\1993api.tif"
tiff_2001 = r"D:\Studia\II stopien\progtamowanie analityczne\deforestation_analysis\images_geotiff\2001api.tif"
tiff_2011 = r"D:\Studia\II stopien\progtamowanie analityczne\deforestation_analysis\images_geotiff\2011api.tif"



red_1985, nir_1985 = read_red_nir(tiff_1985)
red_1993, nir_1993 = read_red_nir(tiff_1993)
red_2001, nir_2001 = read_red_nir(tiff_2001)
red_2011, nir_2011 = read_red_nir(tiff_2011)


ndvi_1985 = calculate_ndvi(red_1985, nir_1985)
ndvi_1993 = calculate_ndvi(red_1993, nir_1993)
ndvi_2001 = calculate_ndvi(red_2001, nir_2001)
ndvi_2011 = calculate_ndvi(red_2011, nir_2011)



all_ndvi = np.concatenate([
    ndvi_1985.ravel(),
    ndvi_1993.ravel(),
    ndvi_2001.ravel(),
    ndvi_2011.ravel()
])



plot_wskaznik([ndvi_1985, ndvi_1993, ndvi_2001, ndvi_2011], "NDVI", -1, 1)


print("Percentyle NDVI:", np.percentile(all_ndvi, [1, 50, 99]))

prog_ndvi = 0.57

maska_1985 = threshold_ndvi(ndvi_1985, prog_ndvi)
maska_1993 = threshold_ndvi(ndvi_1993, prog_ndvi)
maska_2001 = threshold_ndvi(ndvi_2001, prog_ndvi)
maska_2011 = threshold_ndvi(ndvi_2011, prog_ndvi)

plot_maska([maska_1985, maska_1993, maska_2001, maska_2011], "NDVI", prog_ndvi)


procent_roslinnosci = [
    vegetation_percent(maska_1985),
    vegetation_percent(maska_1993),
    vegetation_percent(maska_2001),
    vegetation_percent(maska_2011)
]


plt.figure(figsize=(10, 6))
plt.plot(lata, procent_roslinnosci, marker="o", linewidth=2)
plt.xlabel("Rok")
plt.ylabel("Udział roślinności [%]")
plt.title("Zmiana udziału roślinności na podstawie NDVI")
plt.ylim(0, 100)
plt.yticks(np.arange(0, 101, 20))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()