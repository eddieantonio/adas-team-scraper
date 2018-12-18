CURLOPTIONS = --silent --show-error --location


# We need the sitemap to find all the posts to download.
sitemap.xml:
	curl --fail $(CURLOPTIONS) -o $@ https://adasteam.wordpress.com/sitemap.xm
