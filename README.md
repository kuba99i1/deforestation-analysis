# Deforestation Analysis

Analiza zmian pokrywy roślinnej na podstawie zdjęć satelitarnych z lat 1985, 1993, 2001 i 2011.

## Opis

Projekt wykorzystuje wskaźniki wegetacji (VARI, GLI, VIGREEN, NDVI) do śledzenia zmian powierzchni roślinności w czasie. Dane wejściowe to zdjęcia RGB (PNG) oraz obrazy multispektralne (GeoTIFF) zawierające kanały czerwony i bliskiej podczerwieni (NIR).

## Struktura projektu
```
deforestation-analysis/
├── deforestation.py   # główny skrypt analizy
├── functions.py       # funkcje pomocnicze
├── images/            # zdjęcia RGB (.png)
└── images_geotiff/    # zdjęcia multispektralne (.tif)
```

## Wymagania
```
pip install opencv-python numpy matplotlib rasterio
```

## Uruchomienie
```
python deforestation.py
```

## Wskaźniki

| Wskaźnik | Opis | Dane wejściowe |
|----------|------|----------------|
| VARI | Visible Atmospherically Resistant Index | RGB |
| GLI | Green Leaf Index | RGB |
| VIGREEN | Vegetation Index Green | RGB |
| NDVI | Normalized Difference Vegetation Index | NIR + Red (GeoTIFF) |