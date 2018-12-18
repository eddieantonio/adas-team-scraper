CURLOPTIONS = --silent --show-error --location

all: download-html

include html-download-rules.mk

html-download-rules.mk: link-dowloader.py sitemap.xml
	./$< $@

# We need the sitemap to find all the posts to download.
sitemap.xml:
	curl --fail $(CURLOPTIONS) -o $@ https://adasteam.wordpress.com/sitemap.xm
