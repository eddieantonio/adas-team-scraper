#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

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

blog_post = soup.article
assert 'type-post' in blog_post['class']
author = blog_post.find(class_='author').string
assert len(author) > 0
post_content = blog_post.find(class_='entry-content')

# Get rid of ads, sharing buttons, and other junk.
post_content.find(class_='wpcnt').extract()
post_content.find(class_='sharedaddy').extract()

metadata = {
        'type': 'post',
        'title': title,
        'author': author,
}
markdown = html2text(str(post_content))

yaml_metadata = '\n'.join(f'{key}: {value!r}' for key, value in metadata.items())

output = f"""---
{yaml_metadata}
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
