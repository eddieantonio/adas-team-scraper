#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

"""
Usage:
    html2post -o MARKDOWN HTML

Options:
    -o MARKDOWN, --output=MARKDOWN   The filename of the output Markdown file.

"""

import shlex
import sys
from contextlib import redirect_stdout
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from docopt import docopt
from html2text import html2text


# Parse arugments using the docstring 👆 as a template.
arguments = docopt(__doc__)
html_filename = Path(arguments['HTML'])
post_filename = Path(arguments['--output'])

# Parse the HTML!
with open(html_filename, 'r', encoding='UTF-8') as fp:
    soup = BeautifulSoup(fp, 'lxml')

# The title is not in <title> but in <meta content="..." property="og:title">
title = soup.find('meta', attrs={'property': 'og:title'})['content']

# Parse out the blog post, the author, and the content.
# <div class="type-post">
#   <a class="author">Author Name</a>
#   <div class="entry-content">
#      Here is the blog post...
#   </div>
# </div>
blog_post = soup.article
assert 'type-post' in blog_post['class']
author = blog_post.find(class_='author').string
assert len(author) > 0
post_content = blog_post.find(class_='entry-content')

# Find all of the hosted images, and download them to assets/
# images is a mapping from: Local image path → remote URI
images = {}
for img_tag in post_content.find_all('img'):
    img_uri = urlparse(img_tag['src'])

    # Skip any NON hosted images.
    if img_uri.netloc != 'adasteam.files.wordpress.com':
        print("Skipping image:", img_uri.geturl(), file=sys.stderr)
        continue

    # Figure out where to put the file.
    # It will be save to assets/POST_FILENAME/IMAGENAME.ext
    *_, img_name = img_uri.path.split('/')
    save_path = PurePosixPath('assets') / post_filename.stem / img_name
    # Let the URI be determined by Jekyll.
    jekyll_uri = '{{ site.baseurl }}' / save_path

    # So Wordpress resizes the original to MANY sizes and uses a srcset=""
    # to choose the correct image. For now, we'll just choose the original
    # size.
    original_uri = img_tag.attrs.get('data-orig-file') or img_uri.geturl()
    alt_text = img_tag['alt']

    # Now, throw out the original <img> tag, and redo the attributes
    img_tag.attrs.clear()
    img_tag['src'] = jekyll_uri
    img_tag['alt'] = alt_text

    # Finally, keep track of it!
    images[save_path] = original_uri

# Get rid of ads, sharing buttons, and other junk.
post_content.find(class_='wpcnt').decompose()
post_content.find(class_='sharedaddy').decompose()
# Get rid of atatags' <div> and <script> tags.
for item in post_content:
    if isinstance(item, str):
        continue
    elif item.tag == 'script' or item.attrs.get('id', '').startswith('atatags-'):
        item.decompose()


# Finally, we can prepare the Jekyll post!
front_matter = {
    'title': title,
    'author': author,
}
yaml_front_matter = '\n'.join(f'{key}: {value!r}'
                              for key, value in front_matter.items())

markdown = html2text(str(post_content))

# Buffer the ENTIRE output,
output = f"""---
layout: post
{yaml_front_matter}
---

{markdown}
"""

# Finally, let's write that file!
# Ensure the parent directory(ies) exist.
post_filename.parent.mkdir(parents=True, exist_ok=True)
post_filename.write_text(output, encoding='UTF-8')

# Create the make(1) dependencies file beside the .html file.
if len(images) > 0:
    post_dependency_file = html_filename.with_suffix('.d')
    with open(post_dependency_file, 'w', encoding='UTF-8') as fp,\
         redirect_stdout(fp):
        print('ASSETS +=', *images.keys())
        print(f'{post_filename}: {html_filename}', *images.keys())
        for path, uri in images.items():
            print(f'{path}:')
            # Create the parent directory first!
            print(f'\tmkdir -p', path.parent)
            print(f'\tcurl --fail $(CURLOPTIONS) -o $@', shlex.quote(uri))

# TODO: create <meta content="..." property="og:title">
# TODO: create permalink <meta content="" property="og:url">
# TODO: summarize <meta content="..." property="og:description">
# TODO: <meta content="..." property="og:published_time">
# TODO: <meta content="..." property="og:modified_time">
# TODO: Place this in template  <meta content="..." property="og:site_name">
# TODO: <meta content="..." property="og:image">
# TODO: <meta content="..." property="og:image:secure_url">
# TODO: Use <meta content="en_CA" property="og:locale">
# TODO: <meta content="en_CA" property="og:video">
# TODO: Use <meta content="@Adas_team" name="twitter:creator">
# TODO: Use <meta content="@Adas_team" name="twitter:site">
# TODO: <meta content="summary_large_image" name="twitter:card"/>
# TODO: Use <meta content="249643311490" property="fb:app_id"/>?
# TODO: <meta content="Promoting Diversity in Computing, Games, and Tech" name="msapplication-tooltip"/>
# TODO: <meta content="http://www.youtube.com/watch?v=ifNK08mJgOs Ada's Team is back from the 2013 Grace Hopper Celebration of Women in Computing (GHC 2013). We're running a series of posts written by the women who attended GHC 2013 about their impressions of the conference - a speaker who really inspired them, a career path they learned about, companies they interviewed with at…" name="description"/>
# TODO: RSS feed!
# TODO: Auto sitemap!
