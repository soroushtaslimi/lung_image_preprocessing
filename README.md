# lung_image_preprocessing
This repository uses preprocessing technics such as image growing and erosion and dilation to crop the lungs from chest X-ray images

## Prerequisites

```
Python 3 +
numpy 1.18 +
opencv-python 4.x +
```


## Running the tests

run main.py located in code/ directory
```
python main.py
```

Lung images are read from data/ directory

<img src="https://github.com/soroushtaslimi/lung_image_preprocessing/blob/main/data/images_001/00000005_005.png" width=200></img>
<img src="https://github.com/soroushtaslimi/lung_image_preprocessing/blob/main/data/images_001/00000009_000.png" width=200></img>

After running the code the results are stored in Results/ directory. The green boundary shows a small part of the lung region after erosion. The blue rectangle is used to locate the lungs.

<img src="https://github.com/soroushtaslimi/lung_image_preprocessing/blob/main/Results/images_001/00000005_005.png" width=200></img>
<img src="https://github.com/soroushtaslimi/lung_image_preprocessing/blob/main/Results/images_001/00000009_000.png" width=200></img>

## Authors

* **Soroush Taslimi** - https://github.com/soroushtaslimi


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
