# HowTo: Post-Processing Photos

This introduction to photography post-processing serves as a quick start for beginners. 
It focuses on enhancing on pre-made images for later publication via software.
It's not meant to be a complete guide. 
As there is plenty of software available and a constant evolution going on, this guide can only be a first start.
This introduction will only show open-source programs as they are available for free with the same / similar capabilities as commercial products. 
Please refer to named sources for more information, lookup device usage in their respective manuals or start your own research.

Feedback and error correction always welcome.

## General Overview

In order to understand how image processing software works one must know the basics of how they operate.

Data Compression
All images are stored in some form of compression. This is better known as file format like JPEG, GIF, PNG, BNP, and others. For illustration purposes there is the color space called RGB (red (R), green (G) and blue (B)) in which for each color a value is stored between 0 and 255. The reason for this crude number is that each color is represented by 8 binary numbers (aka bits) and kan therefore be stored as 1 Byte. That also allows representation in hex code in contrast to decimal numbers. 

Example:
base color | binary | decimal | hexadecimal
--- | --- | --- | ---
RED | 00000000 | 0 | #00
GREEN | 11111111 | 255 | #FF
BLUE | 01111111 | 127 | 7F
--- | --- | --- | ---
final color |  | RGB(0, 255, 127) | #00FF7F

As there are three base colors represented by one Byte each, there are a total 16.8 million colors in the RGB color space. For the human eye, that is – in most cases – good enough. In simple *raster images* like BMP this makes calculating the size of an image file pretty easy: Just multiply the dimensionen by 3 Byte and divide by 1024 to convert to KB and MB.

```
1920:1200
(1920 pixels width * 1200 pixels height) * 3 Byte
= 2,304,000 pixels * 3 Byte
= 6,912,000 Bytes
= 6,750 KiloBytes (KB)
~ 6.6 MegaByte (MB)
```


There are however, other color encodings running different schemes. Such are sRGB, ... 
In either way, compression is the art to find the most efficient way to store the information one needs for the purpose at hand. Therefore, storing color information per pixel has proven to be a too crude method and other formats have been conceived being more sophisticated for certain jobs.





When editing background algorithms tab into the numbers behind those colors and thereby calculate alteration to the image. This is especially relevant for changes in color space contrast white balance and other broad alterations of the image.

-------

There are a number of classes of software available for different purposes with overlapping capabilities. 
Main categories: 

* **Image Organisation**:
library tools to get an overview of your pictures; sort, filter and organize them; do minor tweaks. 

* **RAW-processors**:
picking up RAW files (more detailed data) and process them into flat-files (JPG, PNG, etc).

* **Image Editors**:
picking up flat image-files in order to edit them. 

* **Vector-Image processors**
Unlike photos, vector images largely consist of coordinates and shapes. 
They are usually used for abstract graphics like icons or visualisation. 

* **Publishing Tools and Channels**

A normal workflow therefore looks like this:
1. Shoot photos
1. Load into library (using an Image Organisation tool)
1. Select highlight and do RAW processing
1. Do final tweaks in a photo editor
1. Publish

## Image Organisation
Images can be organized in many ways. 
On the most basic level the usual file explorer is sufficient for that job. 
Provided one is used to structure pictures purposefully in folders and sub-folders, in a meaningful way.

If the stock gets bigger, using advanced methods gets more important. 
The ability to search files by tags, elements in the picture, camera or other criteria often require something more sophisticated. 

Often other programs bring basic image organization tools with them, as (other way around) image organization tools often provide simple editing features like cropping, turning or color filters, as well as features to directly publish to an online platform or print.

[open topic]

## RAW processors
RAW files act like negatives in analog photography: they require special techniques to handle them but output images for further editing or straight publication. 
Unlike negatives however, RAW files have the benefit of a much deeper level of data allowing to enhance the look of a picture. 
Therefore RAW processors and photo editors share a lot of features, but RAW processors are specifically chosen for RAW files and to edit the *overall appearance of the picture* (like colors, contrast, sharpness, etc.).

Admittedly, RAW processors share a steep learning curve. 
However, the results can be much more advanced then the out-of-the-box directly out of camera.

### RawTherapee

##### Collection of tutorials on YouTube
* [RawTherapee in JUST 12 Minutes! | Complete Tutorial](https://www.youtube.com/watch?v=QOzPg1HwmkE) by [Jason Polak Photography](https://www.youtube.com/@JasonPolakPhotography)

### Darktable

##### Collection of tutorials on YouTube
* [10 Step Darktable Workflow (Start to Finish)](https://youtu.be/0RLv8NeJc2Q?si=_BULpqL3hlTvu5HU) by [Tony Photo Pilot](https://www.youtube.com/@TonyPhotoPilot) (incl. Free Darktable Workflow Guide)
* [Darktable Beginner Workflow (2026 Update)](https://www.youtube.com/watch?v=EN2JnWCPiBA) by [Kyle Axley](https://www.youtube.com/@KyleAxley)
* Playlist: [Darktable Tutorial](https://www.youtube.com/watch?v=NMcA6MIhg0Q&list=PLqazFFzUAPc6ZUGNzA0cHEm0M06SsMYx7) by [TJ FREE](https://www.youtube.com/@TJFREE)
* [Darktable für Einsteiger: Bildbearbeitung & Verwaltung kostenlos!](https://www.youtube.com/watch?v=eprxpq2xZIQ) by [Schulung Für Dich](https://www.youtube.com/@schulungfurdich)

## Photo Editors
Photo editors  share a lot of features with RAW processors, but photo editors are usually only able to edit flat files (like JPG, PNG, etc) and specialize in editing specifics such as adding/subtracting/replacing elements in the picture, or combining elements of several pictures. 

### GIMP