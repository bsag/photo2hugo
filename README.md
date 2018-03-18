# photo2hugo

This set of scripts is something I put together to use with my [Hugo-driven photoblog](https://github.com/bsag/wow). It is rough and ready, but works well for me. Feel free to clone and adapt it to your own needs.

The basic idea is as follows:

1. You export your photos (with embedded EXIF info) to a local folder on your own computer, sizing and naming the images as you wish.
2. You run `photo2hugo.py`, which asks for an album name (optional), then works through each image in the folder, extracting the EXIF information (using [ExifTool](https://sno.phy.queensu.ca/~phil/exiftool/)) and using this to create a Hugo content file for each image, with the information written to YAML metadata.
3. Once the Hugo files are written, you move the images wherever you will host them from (I use an AWS S3 bucket), and deploy your Hugo site. In my Hugo site config file, I set the base URL for the images, which is then inserted into the templates so that the image URLs are correct. This means that you can change your mind about where you host the images, as you just need to change the config file and rebuild the site.

## Requirements/Set up

* Python 3
* Install the Python dependencies: `pip3 install -r /path/to/requirements.txt` (you only have to do this once)
* Install [ExifTool](https://sno.phy.queensu.ca/~phil/exiftool/). Make sure the path to `exiftool` is correct in `exiftool.py`.
* Copy `config.template.yaml` to `config.yaml` and edit the paths to suit your setup

## Running the script

Run `python3 photo2hugo.py`. The script will ask for an album name to apply to all the files in the export folder. You can always leave this blank and add the metadata to the YAML header of each photo's file later. **NOTE**: The script will overwrite Hugo content files if you re-run the script -- use with care!

You can see the end result of combining these scripts with my [Hugo-driven photoblog](https://github.com/bsag/wow) [here](https://www.wingsopenwide.org.uk/). It is a work in progress :-).

