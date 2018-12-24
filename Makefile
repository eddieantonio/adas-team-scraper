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

# Usage:
# 	make -j && make -j download-images
#
# To remove EVERY downloaded/generated file:
# 	make clean

CURLOPTIONS = --silent --show-error --location

all: convert-posts download-images

# html-download-rules.mk, once generated, will contain a
# `download-html` PHONY target that downloads all of the post HTML.
# It will also create a variable called
# $(HTML) that enumerates each HTML that should be downloaded.
include html-download-rules.mk

ASSETS =
POSTS = $(patsubst _src/%.html,_posts/%.md,$(HTML))

# html2post.py creates .d files for downloading images.
# It will also append filenames to $(ASSETS).
-include $(HTML:.html=.d)

# Generate posts by running them through html2post
# Note: $(HTML) variable is generated in html-download-rules.mk.
convert-posts: $(POSTS)
_posts/%.md: _src/%.html html2post.py
	./html2post.py -o $@ $<

download-images: $(ASSETS)

# Parse links to blog posts from the sitemap.
html-download-rules.mk: create-html-download-rules-from-sitemap.py sitemap.xml
	./$< $@

# We use the sitemap to find all the posts to download.
sitemap.xml:
	curl --fail $(CURLOPTIONS) -o $@ https://adasteam.wordpress.com/sitemap.xml

# Remove generated/downloaded files.
clean:
	$(RM) sitemap.xml
	$(RM) html-download-rules.mk
	$(RM) $(HTML:.html=.d)
	$(RM) $(POSTS)
	$(RM) $(ASSETS)

# These are not real targets -- always remake them.
.PHONY: all clean convert-posts download-images
