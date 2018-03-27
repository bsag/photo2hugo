"""Format metadata to YAML block for Hugo post"""
import subprocess
import re
import json
from datetime import datetime, date, time
from glob import glob


def get_basename(fstring, content_file_extension):
    """Return the basename of the image file with a Markdown
    file extension (specified in config.yaml)"""
    fbasename = re.match(r'(.*)\.jpg', fstring).group(1)
    fname = ".".join((fbasename, content_file_extension))
    return(fname)


def format_hugo_date(dt):
    """Generate a Hugo formatted datestring from a
        datetime object"""
    d = dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    return(d)


def conv_exif_to_hugo_date(date_string):
    """Convert EXIF date to Hugo format date"""
    # "2017:12:11 12:34:19"
    dt = datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
    d = format_hugo_date(dt)
    return(d)


def check_key(metadata, key, default_val):
    v = metadata.get(key, default_val)
    return(v)


def build_content(metadata, img_base_url):
    """Create image link and description for body of content file"""
    img = "![{0}]({1}/s/{3})".format(metadata['XMP:Title'],
                                     img_base_url, metadata['File:Filename'])
    description = check_key(metadata, 'XMP:Description', "Image information")
    content = "{0}\n\n{1}\n".format(img, description)

    return(content)


def process_exif_keys(metadata, album, img_base_url):
    """Pulls in EXIF data for one image and processes the
        relevant keys to make a string to write to YAML block"""

    img_tags = check_key(metadata, 'XMP:Subject', "[]")

    # Fix so that if there is only one tag (so a simple string),
    # it is saved in the right format as a YAML array
    if isinstance(img_tags, str):
        img_tags = "[\"{0}\"]".format(img_tags)

    description = check_key(metadata, 'XMP:Description', "Image information")

    if description == "":
        description == "Image information"

    meta = dict(
        title=metadata['XMP:Title'],
        date=format_hugo_date(datetime.now()),
        description=description,
        taken_on=conv_exif_to_hugo_date(metadata['EXIF:DateTimeOriginal']),
        aperture="f/{0}".format(metadata['EXIF:FNumber']),
        speed="{0}s".format(metadata['Composite:ShutterSpeed']),
        iso="ISO {0}".format(metadata['EXIF:ISO']),
        expcomp="{0} ev".format(metadata['EXIF:ExposureCompensation']),
        camera="{0!s} {1}".format(metadata['EXIF:Make'].capitalize(),
                                  metadata['EXIF:Model']),
        tags=img_tags,
        albums=album,
        imageurl=metadata['File:FileName']
    )

    out_list = []
    out_list.append("---\n")

    for k, v in meta.items():
        if (k == "tags"):
            out_list.append("{0}: {1}\n".format(k, v))
        else:
            out_list.append("{0}: \"{1}\"\n".format(k, v))

    out_list.append("---\n\n")
    out_list.append(build_content(metadata, img_base_url))

    return("".join(out_list))
