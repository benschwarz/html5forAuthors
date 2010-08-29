# About this repo

The contents of this repo are build tools for generating the document
[HTML5 (Edition for Web Authors)](http://dev.w3.org/html5/spec-author-view/),
a strict subset of the
[HTML5 spec](http://dev.w3.org/html5/spec-author-view/)
that omits UA implementation details and that is targeted toward Web
authors and others who are not UA implementors and who want a view
of the HTML specification that focuses more precisely on details
relevant to using the HTML language to create Web content.

This repo does not contain the generated HTML for the actual
document; instead it is just the actual build system you can use
to generate a copy of the document on your own (if you care to try).

It's not a particularly pleasant or easy-to-use build system, and
it's also quite slow. But I guarantee you it does actually work—
as long as you the right dependencies (and some time on your hands).

I'm also not planning to ever provide any actual documentation on
how to use it. If you try it and run into problems or have
questions, you'll find all the answers by reading the source of
the Makefile within.

Note that the versions of anolis and the spec splitter from the
html5lib project are included in this repo just for the sake of
convenience. If you make the "distclean" target, it will remove
the anolis and html5-tools subdirs, but then the build process
will subsequently re-download and patch them before using them.

Michael(tm) Smith <sideshowbarker@gmail.com>

![me](http://github.com/sideshowbarker/jsblog/raw/master/me.jpg)
