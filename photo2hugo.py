import subprocess
import os
import yaml
from glob import glob
import exiftool
import metadata

# Get input from user for album name
album = input("Enter album name (or leave blank):")

# Load in the config variables
with open('config.yaml') as c:
    # use safe_load instead load
    configs = yaml.safe_load(c)

# Read in the files list from source directory in config file
source_folder = os.path.join(configs['source_dir'], 'orig')
dest_folder = configs['content_dir']
content_file_extension = configs['content_file_extension']
img_base_url = configs['img_base_url']
files_list = glob(os.path.join(source_folder, '*.jpg'))

# Use ExifTool to read in metadata
with exiftool.ExifTool() as e:
    meta = e.get_metadata(*files_list)
    # Extract basename to use as Hugo content filename
    # For each item in metadata:
    # - create file using filename
    # - process the EXIF keys in the right format
    # - write the YAML structure plus the formatted keys
    # - write the content (filename)
    # - save file
    # - report back on how many files created
num_files = 0

for m in meta:
    fname = metadata.get_basename(m['File:FileName'], content_file_extension)
    fpath = os.path.join(dest_folder, fname)
    num_files += 1

    with open(fpath, 'w') as f:
        f.write(metadata.process_exif_keys(metadata=m,
                                           album=album,
                                           img_base_url=img_base_url))
        msg = "Image \"{0}\" written to {1}".format(m['XMP:Title'], fpath)
        print(msg)

print("{0} files processed.".format(num_files))
