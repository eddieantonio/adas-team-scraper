CURLOPTIONS = --silent --show-error --location

all: download-html

# html-download-rules.mk, once generated, will contain a
# `download-html` PHONY target that downloads all of the post HTML.
# It will also create a variable called
# $(HTML) that enumerates each HTML that should be downloaded.
include html-download-rules.mk
html-download-rules.mk: link-dowloader.py sitemap.xml
	./$< $@

# We use the sitemap to find all the posts to download.
sitemap.xml:
	curl --fail $(CURLOPTIONS) -o $@ https://adasteam.wordpress.com/sitemap.xm
