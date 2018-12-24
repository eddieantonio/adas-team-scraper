‘Steam Scraper
==============

Downloads all of the blog posts on [Ada's Team's WordPress
site][adasteam-blog] and converts them to [Jekyll][] blog posts.

The output will be folders called `_posts/` and `assets/`.

[adasteam-blog]: https://adasteam.wordpress.com/
[Jekyll]: https://jekyllrb.com/


How to do the thing
-------------------

### Install system requirements

 - `make`: you probably have this already
 - `pipenv`:  you might have this. Install it like this if you don't: `brew install pipenv`
 - Python 3.7: `pipenv` will probably install this?

Next, install all the things with `pipenv`:

```sh
pipenv install
```

### Running

Activate the `pipenv` environment:

```sh
pipenv shell
```

Within the environment, start `make`!

```sh
make -j 8 && make -j 8 download-images
```

(`-j 8`  starts up to 8 jobs simultaneously; adjust it as you see fit).

If all went well, you should now have Markdown posts, ready for
publication in `_posts/` and images in `assets/`! You can just copy
over `_posts/` and `assets/` to your Jekyll blog.


It all didn't go well
---------------------

Oh, that's a bummer! Send me an issue report!


How does it work?
-----------------

Simple! It's a Makefile that calls a Python script to create another
Makefile, which is included in the original Makefile, which calls
another Python script, but this time way more than once, and that Python
script also creates several Makefiles, however, that's about as many
embedded Makefiles as we're going to take so then you invoke `make`
again to embed the other Makefiles and by then end of this process,
you'll have all of the Markdown posts and images!

<iframe src="https://giphy.com/embed/l0IykOsxLECVejOzm" width="480" height="304" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/fx-charlie-always-sunny-l0IykOsxLECVejOzm">via GIPHY</a></p>

### Okay, but seriously

We want to create all corresponding `*.md` files from `*.html` files.
This would be done with a pattern rule:

```make
%.md: %.html
	./html2post -o $@ $<
```

This means, to make a `foo.md` from a `foo.html`, run `./html2post`,
which will output to `$@` (the _target_), by supplying the first
dependency (`$<`) as input.

**However**, we don't have all the HTML files! We have to download them
all. So, the `Makefile` is instructed to figure those out first. It
realizes it needs `html-download-rules.mk `, but that doesn't exist
yet. If an include doesn't exist, Make tries to create it by some rule.
The existing rule tells it to invoke
`./create-html-download-rules-from-sitemap.py` which consequently
requires `sitemap.xml`. So Make downloads `sitemap.xml` and runs
`./create-html-download-rules-from-sitemap.py`.

`sitemap.xml` lists all of the blog posts online.
`./html-download-rules.mk` will list all of the URIs to download HTML
pages. Thus, when Make finally is able to include this file (generated
by `./create-html-download-rules-from-sitemap.py`), it now knows how to:

### But that's not all!

We still need to download images. Along with the Markdown post, the
`html2post` creates `*.d` Makefile "dependency" files. These files are
generated such that, in order for the Markdown post to exist, they
require not only the original HTML, but also all of the images,
downloaded in `assets/`. Just as before, each `*.d` file instructs Make
how to download each image. Then, these rules are included in the main
Makefile, but _only on the second invocation of make_! (I could have had
it all in one go, but this was already getting a bit out of hand, so
I opted for a slightly simpler two-stage process instead).

I probably should have stopped at first stage, or downloaded images in
`html2post`, but... aw well. ¯\_(ツ)_/¯

License
-------

This code is distributed under the terms of the Unlicense, reproduced
below:

> This is free and unencumbered software released into the public domain.
>
> Anyone is free to copy, modify, publish, use, compile, sell, or
> distribute this software, either in source code form or as a compiled
> binary, for any purpose, commercial or non-commercial, and by any
> means.
>
> In jurisdictions that recognize copyright laws, the author or authors
> of this software dedicate any and all copyright interest in the
> software to the public domain. We make this dedication for the benefit
> of the public at large and to the detriment of our heirs and
> successors. We intend this dedication to be an overt act of
> relinquishment in perpetuity of all present and future rights to this
> software under copyright law.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
> EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
> MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
> IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
> OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
> ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
> OTHER DEALINGS IN THE SOFTWARE.
>
> For more information, please refer to <http://unlicense.org/>
