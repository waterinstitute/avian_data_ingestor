**Disclaimer: This document and the content of the repository is in draft state.  File structure and documentation can change in any moment.** 
# Gulfwide Avian Colony Monitoring Survey Photos


[Colibri Ecological Consulting Inc](https://colibri-ecology.com/), as a [The Water Insitute of the Gulf](https://thewaterinstitute.org/) subcontractor, under a [Coastal Protection and Restoration Authority (CPRA)](https://coastal.la.gov/) contract, has taken high-resolution aerial photos in zones that extend from southern Texas to the Big Bend of Florida along the northern coast of the Gulf of Mexico. 
Photos have been annotated(dotted) with bird nests analysis data (including species, quantity, and date). These photos will be used to assess changes in colonial waterbird populations. 
Initially, the dataset contains photos taken in 2018 and it will grow with photos being taken in 2021. 

## Data formats 

High resolution(5184 x 3456) images are provided in jpg format (compression quality level 98%). A sample image can be found at  [doc/examples/20May2018 Camera2-3817.jpg](doc/examples/20May2018%20Camera2-3817.jpg). 2018 dataset has 26899 images. 
Metadata will be provided in json format in a schema similar to the example found in [doc/examples/20May2018 Camera2-3817.json](doc/examples/20May2018%20Camera2-3817.json). 
Low resolution, png, thumbnails will also be provided.

![thumbnail](doc/examples/20May2018%20Camera2-3817.png)

Metadata schema may change but the documentation in this repository will reflect those changes. Metadata information includes data about birds species' colonies location.
Each dataset will also contain an static site using the metadata and the thumbnails.  
The folder structure will contain: 
```
<dataset name>/
├─ metadata/
│  ├─ <filename1>.json
│  ├─ <filename2>.json
│  ├─ all.json
├─ thumbnails/
│  ├─ <filename1>.png
│  ├─ <filename2>.png
├─ <filename2>.jpg
├─ <filename1>.jpg
├─ index.html
├─ README.md
```
### How metadata is created
The [metadata_generation](doc/metadata_generation.ipynb) jupyter notebook describe the metadata creation process. 

## The ingestor
This repository contains the code for the ingestor component of the photo discoverability tool. At this early stage it is used to generate the metadata files.

## Licence

The datasets are relased with a Creative Commons BY-SA, license. 
The software and documentation in this repository has an Apache License. 
