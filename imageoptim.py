# Uses ImageOptim API, for which you need an account
# https://imageoptim.com/api
# This converts local image files to the chosen sizes using the API
import requests
import yaml
import os

# Load in the config variables
with open('config.yaml') as c:
    # use safe_load instead load
    configs = yaml.safe_load(c)

# Vars
api_url = configs['api_url']
source_dir = configs['source_dir']
# img_base_url = configs['img_base_url']

# Directories to save the various sizes
# 'orig' holds the exported, full size images for processing
# Pixel sizes:
# xl = 3072px (3x medium)
# l = 2048px (2x medium)
# m = 1024px (1x medium)
# s = 1200px (3x xs)
# xs = 800px (2x xs)
# xs = 400px (1x xs)
orig_dir = 'orig'

# Sizing options to be passed to API
opts = dict(
    xl='1024x1024,3x',
    l='1024x1024,2x',
    m='1024x1024',
    s='400x400,3x',
    xs='400x400,2x',
    xxs='400x400'
)

orig_dir = os.path.join(source_dir, orig_dir)


# pass one original image in and convert to all sizes
# loop over opts
def convert_image(f_name):

    for k, v in opts.items():
        print("Writing size {0}".format(k))
        url = "{0}/{1}/".format(api_url, v)
        in_file = os.path.join(orig_dir, f_name)
        out_file = os.path.join(source_dir, k, f_name)
        file = {'file': open(in_file, 'rb')}  # fix path source_dir/orig/f_name

        r = requests.post(url, files=file)
        r.content

        with open(out_file, 'wb') as f:
            f.write(r.content)


# Loop through files in orig, calling convert_image() on each
for filename in os.listdir(orig_dir):
    if filename.endswith(".jpg"):
        print("Converting image {0}".format(filename))
        convert_image(f_name=filename)
    else:
        continue

print("All convertions complete.")
