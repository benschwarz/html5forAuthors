SVN=svn
CURL=curl
PYTHON=python
CVS=cvs
CVSFLAGS=
GREP=egrep
GREPFLAGS=
TEE=tee
TEEFLAGS=
PERL=perl
PERLFLAGS=
PATCH=patch
PATCHFLAG=
PARSE=xmllint
PARSEFLAGS=--html --xmlout
XSLTPROC=xsltproc
XSLTPROCFLAGS=--novalid

HTML5=../spec
SPLITTER=html5-tools/spec-splitter/spec-splitter.py
#SPLITTERFLAGS=--w3c --html5lib-serialiser
SPLITTERFLAGS=--w3c --html5lib-serialiser --make-index-of-terms
WHATWGSTYLE = whatwg.css

# http://mercurial.selenic.com/wiki/
HG=hg

REVISION=$(shell $(GREP) $(GREPFLAGS) 'This is .+Revision: ' $(HTML5)/Overview.html | $(PERL) $(PERLFLAGS) -pe 's/.*This is .+Revision: (1\.[0-9]+) \$$\./$$1/')

Overview.html: spec.html $(SPLITTER) MANIFEST FILECHECK

spec.preprocessed.html: $(HTML5)/Overview.html anolis/anolis tools/preprocess.xsl fragment-links.xhtml
	$(XSLTPROC) $(XSLTPROCFLAGS) \
	  --html \
	  --stringparam RCSREVISION $(REVISION) \
	  tools/preprocess.xsl \
	  $(HTML5)/Overview.html > $@

spec.html: spec.preprocessed.html tools/postprocess.xsl
	$(PYTHON) anolis/anolis \
	  --parser=lxml.html \
	  --enable terms \
	  --filter=.impl \
	  --output-encoding="ascii" \
	  $< $@.tmp
	$(XSLTPROC) $(XSLTPROCFLAGS) \
	  --html \
	  tools/postprocess.xsl \
	  $@.tmp > $@
	$(PERL) $(PERLFLAGS) -pi -e "s/load\('styler.js'\);//" $@;

MANIFEST: spec.html
	$(PYTHON) $(PYTHONFLAGS) $(SPLITTER) $(SPLITTERFLAGS) $< . \
	  | $(TEE) $(TEEFLAGS) SPLITTERLOG \
	  | $(GREP) $(GREPFLAGS) '<h2>|<h3>|<h4>|<h5>|<h6>' \
	  | cut -c8- \
	  | cut -d " " -f1 \
	  | $(PERL) $(PERLFLAGS) -pe "s/(^[^ ]+)\s*\n/\1.html\n/" > $@
	 cp html5-tools/spec-splitter/link-fixup.js .

fragment-links-full.js:
	$(CURL) $(CURLFLAGS) -o $@ http://dev.w3.org/html5/spec/fragment-links.js

fragment-links.xhtml: fragment-links-full.js
	$(GREP) $(GREPFLAGS) "var fragment_links" $< \
	  | perl -pe "s|var fragment_links = \{ '|<div xmlns='http://www.w3.org/1999/xhtml'>\n<ul>\n<li>#|" \
	  | perl -pe "s|':'|</li>\n<li>|g" \
	  | perl -pe "s|','|</li>\n</ul>\n<ul>\n<li>#|g" \
	  | perl -pe "s|' };|</li>\n</ul>\n\</div>|g" \
	  > $@

FILECHECK:
	-$(CVS) $(CVSFLAGS) add *.html 2>&1 | grep -v already
	-$(CVS) $(CVSFLAGS) add index-of-terms/*.html 2>&1 | grep -v already
	touch $@

clean:
	$(RM) spec.preprocessed.html
	$(RM) spec.html.tmp
	$(RM) spec.html
	$(RM) CHANGEDESC
	$(RM) SPLITTERLOG
	$(RM) FILECHECK
	$(RM) MANIFEST

distclean: clean
	$(RM) -r anolis
	$(RM) -r html5-tools
	$(RM) fragment-links-full.js
	$(RM) fragment-links.xhtml

CHANGEDESC: $(HTML5)/Overview.html
	$(CVS) $(CVSFLAGS) log -r$(REVISION) $< \
	  | $(GREP) $(GREPFLAGS) -v \
	  "^$$|^RCS file: |^Working file: |^head:|^branch:|^locks:|^access list:|^symbolic names:|^keyword substitution:|^total revisions:|^description:|^revision |^-----|^date: |^=====" \
	  > $@
	@echo >> $@
	@echo "[updated by splitter]" >> $@

# below are some historical targets and comments from DanC when he
# first set up the build

# This was DanC 1st approach; hixie suggested the above technique instead
html5-author2.html: webapps/source anolis/anolis
	anolis/anolis --parser=lxml.html \
		--output-encoding=ascii --w3c-compat-xref-a-placement \
		--filter=.impl webapps/source $@

webapps/source:
	$(SVN) co http://svn.whatwg.org/webapps/


# Another source of clues...
#<rubys> We should use what Hixie provides, but FYI, I've genned a document before using this: http://intertwingly.net/tmp/html5spec

#####
# some dependencies

# this also relies on html5lib and lxml
anolis/anolis:
	$(HG) clone http://hg.hoppipolla.co.uk/anolis/
	$(PATCH) $(PATCHFLAGS) -p1 -d anolis < patch.anolis

# tested with r169 2009-07-22 08:37:15 -0500
# Repository UUID: fac1fef6-d828-0410-b4ea-9384b9858573
$(SPLITTER):
	$(SVN) checkout http://html5.googlecode.com/svn/trunk/ html5-tools
	$(PATCH) $(PATCHFLAGS) -p0 < patch.spec-splitter.1

$(WHATWGSTYLE):
	$(CURL) http://www.whatwg.org/style/specification > $@
