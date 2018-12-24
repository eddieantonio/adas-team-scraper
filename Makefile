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

# Remove generated content
clean:
	$(RM) $(HTML:.html=.d)
	$(RM) $(POSTS)
	$(RM) $(ASSETS)

# These are not real targets -- always remake them.
.PHONY: all clean convert-posts download-images
