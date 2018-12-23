‘Steam Scraper
==============

Downloads all of the blog posts on [Ada's Team's WordPress
site][adasteam-blog] and converts them to [Jekyll][] blog posts.

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

Within the environment, type `make`!

```sh
make -j 8
```

(`-j 8`  starts up to 8 jobs simultaneously; adjust it as you see fit).

If all went well, you should now have Markdown posts, ready for
publication in `_posts/`!


It all didn't go well
---------------------

Oh, that's a bummer! Send me an issue report!


How does it work?
-----------------

Very carefully.

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
