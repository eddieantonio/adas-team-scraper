CURLOPTIONS = --silent --show-error --location

all: convert-posts

# html-download-rules.mk, once generated, will contain a
# `download-html` PHONY target that downloads all of the post HTML.
# It will also create a variable called
# $(HTML) that enumerates each HTML that should be downloaded.
include html-download-rules.mk
html-download-rules.mk: create-html-download-rules-from-sitemap.py sitemap.xml
	./$< $@

# Generate posts by running them through html2post
# Note: $(HTML) variable is generated.
convert-posts: $(patsubst _src/%.html,_posts/%.md,$(HTML))
_posts/%.md: _src/%.html
	./html2post.py -o $@ $<

# We use the sitemap to find all the posts to download.
sitemap.xml:
	curl --fail $(CURLOPTIONS) -o $@ https://adasteam.wordpress.com/sitemap.xml
