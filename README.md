photo_processor
===============

History
-------

Just a custom tool to fix some issues with my photos.

I have a small collection of pictures that combined with other image files that I have in my hard drive used to take up to 4.6GB of disk space, also the different photos taken with a variety of devices ended up having different file extentions like (JPG, jpg, JPEG or jpeg) and after some years I knew that I needed some way to normalize all those file names.

Few months ago I read out about jpegoptim a JPEG Image Optimization / Compress Command in this [post](http://www.cyberciti.biz/faq/linux-jpegoptim-jpeg-jfif-image-optimize-compress-tool/) created by Nix Craft and decided to create this tool to normalize my photo names and also save some space in my disk.

After running photo_processor my image folder now uses 4.3GB of space, so I've saved 3GB

Features
------------
* cli interface (docopt)
* option to change file names to lower case
* option to optimize pictures files using jpegoptim, check [jpegoptim page](http://freecode.com/projects/jpegoptim)  for more details
* option to scan a directory recursively
* an log file is generated with the results of processing image files
* only JPEG image files are supported for now

Planned features
------------------------
* add optiomization options for other image files http://www.cyberciti.biz/faq/linux-unix-optimize-lossless-png-images-with-optipng-command/
* add some unit tests
