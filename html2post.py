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

    html2post -o post.md post.html
"""

import sys

from html2text import html2text
from bs4 import BeautifulSoup


# Using exit codes defined in sysexits.h:
# https://www.freebsd.org/cgi/man.cgi?query=sysexits&apropos=0&sektion=0&manpath=FreeBSD+4.3-RELEASE&format=html
EXIT_USAGE = 64

try:
    _exec, _o, post_filename, html_filename = sys.argv
except ValueError:
    print(f"Invalid arguments: {sys.argv[1:]}",
          file=sys.stdout)
    sys.exit(EXIT_USAGE)

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

# TODO: Find all of the hosted images, and download them to assets/

# Get rid of ads, sharing buttons, and other junk.
post_content.find(class_='wpcnt').decompose()
post_content.find(class_='sharedaddy').decompose()

front_matter = {
        'title': title,
        'author': author,
}
markdown = html2text(str(post_content))

yaml_front_matter = '\n'.join(f'{key}: {value!r}'
                              for key, value in front_matter.items())

output = f"""---
layout: post
{yaml_front_matter}
---

{markdown}
"""

with open(post_filename, 'w', encoding='UTF-8') as fp:
    fp.write(output)

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
# TODO: auto sitemap!
