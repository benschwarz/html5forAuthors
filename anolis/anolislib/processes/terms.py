# coding=UTF-8
# Copyright (c) 2010 Michael(tm) Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re

from lxml import etree
from copy import deepcopy

from anolislib import utils

class terms(object):
    """Build and add an index of terms."""

    terms = None

    def __init__(self, ElementTree, **kwargs):
        self.terms = etree.Element(u"div",{u"class": "index-of-terms"})
        self.buildTerms(ElementTree, **kwargs)
        self.addTerms(ElementTree, **kwargs)

    def buildTerms(self, ElementTree, w3c_compat=False, **kwargs):
        self.terms.text = "\n"
        # make a list of all the defining instances of "terms" in the document
        # -- <dfn> elements
        dfnList = ElementTree.findall("//dfn")
        if dfnList:
            indexNavTop = etree.Element(u"div",{u"class": "index-nav", u"id": "index-terms_top"})
            indexNavTop.text = "\n"
            indexNavTop.tail = "\n"
            indexNavHelpers = {"top": indexNavTop}
            self.terms.append(indexNavHelpers["top"])
            termFirstLetter = None
            prevTermFirstLetter = None
            firstLetters = ["top"]
            # sort the list of <dfn> terms by the lowercase value of the DOM
            # textContent of the <dfn> element (concantentation of the <dfn>
            # text nodes and that of any of its descendant elements)
            dfnList.sort(key=lambda dfn: dfn.text_content().lower())
            for dfn in dfnList:
                # we don't need the tail, so copy the <dfn> and drop the tail
                term = deepcopy(dfn)
                term.tail = None
                termID = None
                dfnHasID = False
                if dfn.get("id"):
                    # if this <dfn> itself has an id, we'll use it as part of the
                    # id on the index entry for this term
                    termID = dfn.get("id")
                    dfnHasID = True
                elif dfn.getparent().get("id"):
                    # if this <dfn> itself has no id, use the id of its parent
                    # node as the id on the index entry for this term, with or
                    termID = dfn.getparent().get("id")
                # if we found an id, then create an index entry for this <dfn>
                # term; otherwise, do nothing further
                if termID:
                    indexEntry = etree.Element(u"dl")
                    # we want to give this index entry an id attribute based on
                    # the <dfn> or parent of a <dfn> we got the id-attribute
                    # value from earlier; but, if this <dfn> has no id attribute
                    # and has any sibling <dfn>s that also lack id attributes,
                    # we need to further qualify the id attribute here to make
                    # it unique
                    dfnSiblings = int(dfn.xpath("count(preceding-sibling::dfn[not(@id)])"))
                    if not dfnHasID and dfnSiblings > 0:
                        indexEntry = etree.Element(u"dl",{u"id": termID+"_"+str(dfnSiblings)+"_index"})
                    else:
                        indexEntry = etree.Element(u"dl",{u"id": termID+"_index"})
                    indexEntry.text = "\n"
                    # termName is container of the name of the term as it appears in the index
                    termName = etree.Element(u"dt")
                    if "id" in term.attrib:
                        del term.attrib["id"]
                    term.tag = "span"
                    term.tail = "\n"
                    termName.append(term);
                    termName.tail= "\n"
                    indexEntry.append(termName)
                    # normalize the text content of each <dfn> in the document
                    # and then normalize the text content of this <dfn>, then
                    # do a case-insensitive comparison of them and count how
                    # many matches we have
                    expr = "count(//dfn\
                            [normalize-space(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'))\
                            =normalize-space(translate($content,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'))])"
                    if ElementTree.xpath(expr, content = term.text_content()) > 1:
                        # we have more than one <dfn> in the document whose
                        # content is a case-insensitive match for the
                        # textContent of this <dfn>; so, we attempt to
                        # disambiguate them by copying the parent node of the
                        # <dfn> and including that in our output as an excerpt,
                        # to provide the context for the term
                        dfnContext = etree.Element(u"dd",{u"class": u"dfn-excerpt"})
                        dfnContext.text = "\n"
                        dfnContext.tail = "\n"
                        dfnParentNode = deepcopy(dfn.getparent())
                        # if length of the parent node isn't greater than 1,
                        # then the <dfn> is the only child node of its parent,
                        # and so there is no useful context we can provide, so
                        # we do nothing. Also, if the parent node is an h1-h6
                        # heading, we are already listing it in the entry, to
                        # it'd be redundant to be it here too, so we don't
                        if len(dfnParentNode) > 1 and not re.match("^[hH][1-6]$",dfnParentNode.tag):
                            # we just drop all of the text in this parent up to
                            # the first child element, because it's often just
                            # part of phrase like "The foo attribute" or
                            # something, and we don't need that. But, after we
                            # drop it, we don't want the node to end up starting
                            # with no next at all (because it looks odd in our
                            # output), so we replace it with some characters to
                            # indicate that there's something been ellided
                            if not dfnParentNode[0].tag == "dfn":
                                dfnParentNode.text = "*** "
                            # ...except for the case where we know our current
                            # dfn is the first child element, and then we deal
                            # with handling of that a little further down
                            else:
                                dfnParentNode.text = ""
                            dfnParentNode.tag = "span"
                            # remove ID so that we don't duplicate it
                            if "id" in dfnParentNode.attrib:
                                del dfnParentNode.attrib["id"]
                            descendants = dfnParentNode.xpath(".//*[self::dfn or @id]")
                            for descendant in descendants:
                                if descendant.tag == "dfn":
                                    descendant.tag = "span"
                                if "id" in descendant.attrib:
                                    del descendant.attrib["id"]
                                # if the text content of this descendant is the
                                # same as the text content of the term, then we
                                # don't want to repeat it, so instead we
                                # replace it with ellipses
                                if descendant.text_content().lower() == term.text_content().lower():
                                    tail = ""
                                    if descendant.tail is not None:
                                        tail = descendant.tail
                                    # drop any children this element might have,
                                    # and just put ellipsis in place of it
                                    descendant.clear()
                                    descendant.text = "..."+tail
                                elif descendant == descendants[0]:
                                    # if we get here it means that the first dfn
                                    # child of this parent node is _not_ our
                                    # current dfn, so we use some alternative
                                    # characters (other than ellipses) to
                                    # indicate that we've ellided something
                                    dfnParentNode.text = "*** "
                            dfnContext.append(dfnParentNode)
                            indexEntry.append(dfnContext)
                    # we need a first letter so that we can build navigational
                    # links for the alphabetic nav bars injected into the index
                    termFirstLetter = term.text_content()[0].upper()
                    if termFirstLetter != prevTermFirstLetter and termFirstLetter.isalpha():
                        firstLetters.append(termFirstLetter)
                        indexNavHelpers[termFirstLetter] = etree.Element(u"div",{u"class": "index-nav", u"id": "index-terms_"+termFirstLetter})
                        prevTermFirstLetter = termFirstLetter
                        self.terms.append(indexNavHelpers[termFirstLetter])
                    # #########################################################
                    # make a list of all the instances of terms in the document
                    # that are hyperlinked references back to the <dfn> term
                    # that is the defining instance of this term, as well as
                    # the <dfn> defining instance itself
                    # #########################################################
                    instanceList = ElementTree.xpath("//a[substring-after(@href,'#')=$targetID]|//*[@id=$targetID]", targetID = termID)
                    if instanceList:
                        instanceItem = None
                        lastLinkToHeading = None
                        lastInstanceItem = None
                        for instance in instanceList:
                            # each of these term instances is an <a> hyperlink
                            # without an id attribute, but we need each to have
                            # an id attribute so that we can link back to it
                            # from the index of terms; so, create an id for each
                            instanceID = utils.generateID(instance, **kwargs)
                            instance.set(u"id",instanceID)
                            # make a link that's a copy of the node of the h1-h6
                            # heading for the section that contains this
                            # instance hyperlink
                            linkToHeading = self.getAncestorHeadingLink(instance, instanceID)
                            if not instance.tag == u"a":
                                linkToHeading.set(u"class","dfn-ref")
                            # if this heading is not the same as one that we've
                            # already added to the index entry for this term,
                            # then process the heading
                            if lastLinkToHeading is None or linkToHeading.text_content() != lastLinkToHeading.text_content():
                                instanceItem = etree.Element(u"dd")
                                instanceItem.text = "\n"
                                lastLinkToHeading = linkToHeading
                                n = 1
                                # we wait to add the item for the previous
                                # instance at this point because we need to
                                # delay adding in order to see if for this
                                # instance there are multiple references to the
                                # same ancestor heading (if there are, we append
                                # link numbers to them, instead of repeating the
                                # heading; see below)
                                if lastInstanceItem is not None:
                                    #print(etree.tostring(lastInstanceItem,method="text"))
                                    indexEntry.append(lastInstanceItem)
                                lastInstanceItem = instanceItem
                                linkToHeading.tail = "\n"
                                instanceItem.append(linkToHeading)
                                instanceItem.tail = "\n"
                            # otherwise, this heading is the same as one that
                            # we've already added to the index entry for this
                            # term; so instead of reprocessing the heading, we
                            # just append one or more link numbers to it
                            else:
                                n += 1
                                counterLink = etree.Element(u"a",{u"href": "#"+instanceID, u"class": "index-counter"})
                                if not instance.tag == u"a":
                                    counterLink.set(u"class","dfn-ref")
                                else:
                                    counterLink.set(u"class","index-counter")
                                counterLink.text = "("+str(n)+")"
                                counterLink.tail = "\n"
                                instanceItem.append(counterLink)
                            # if the value of our n counter is still at 1 at
                            # this point, it means the document contains only
                            # one instance of a reference this term, so we need
                            # to add that instance now
                            if n == 1:
                                indexEntry.append(instanceItem)
                    if not len(instanceList) > 1:
                        # if we don't have more than one item in this list, it
                        # means the <dfn> defining instance is the only item in
                        # the list, and the document contains no hyperlinked
                        # references back to that defining instance at all, so
                        # we need to set a flag to indicate that
                        indexEntry.set(u"class","has-norefs")
                    self.terms.append(indexEntry)
                    indexEntry.tail = "\n"
            # ######################################################################
            # inject some alphabetic nav hyperlink bars into the index, strictly
            # for convenience purposes
            # ######################################################################
            navLetters = etree.Element(u"p")
            navLetters.text = "\n"
            navLetters.tail = "\n"
            navLettersClones = {}
            # reverse the letters list so that we can just pop off it
            firstLetters.append("end")
            firstLetters.reverse()
            while(firstLetters):
                letter = firstLetters.pop()
                navLetter = etree.Element(u"a",{u"href": "#index-terms_"+letter})
                navLetter.text = letter
                navLetter.tail = "\n"
                navLetters.append(navLetter)
            for key, navNode in indexNavHelpers.items():
                # this seems really hacky... but we need some way to manage multiple
                # copies of the sets of nav hyperlink letters we inject into the
                # index; otherwise, how to do it without just moving a single node
                # around instead of copying it...
                navLettersClones[key] = deepcopy(navLetters)
                navNode.text = "\n"
                navNode.append(navLettersClones[key])
                navNode.tail = "\n"
            navLettersEnd = deepcopy(navLetters)
            indexNavEnd = etree.Element(u"div",{u"class": "index-nav", u"id": "index-terms_end"})
            indexNavEnd.text = "\n"
            indexNavEnd.tail = "\n"
            indexNavEnd.append(navLettersEnd)
            indexNavHelpers = {"end": indexNavEnd}
            self.terms.append(indexNavHelpers["end"])
        self.terms.tail = "\n"

    def getAncestorHeadingLink(self, descendantNode, id):
        """ Given a node, return a link to the heading for the section that contains it."""
        node = descendantNode
        while (node is not None):
            if isinstance(node.tag,str) and re.match("^[hH][1-6]$",node.tag):
                # we need a copy of this heading rather than the original node
                headingLink = deepcopy(node)
                # turn this h1-h6 heading copy into <a> hyperlink back to the
                # location of the target node
                headingLink.tag = "a"
                headingLink.set(u"href","#"+id)
                # this is a copy of an h1-h6 heading that may have had an id
                # attribute; we don't want to duplicate the id, so drop it
                if "id" in headingLink.attrib:
                    del headingLink.attrib["id"]
                # some headings may contain descendants that are <a> links or
                # <dfn>s, and/or that have id attributeds
                embeddedLinks = headingLink.xpath(".//*[self::dfn or @href or @id]")
                # we have taken a copy of what was a heading and transformed it
                # into a hyperlink, and because it is a hyperlink, we now do not
                # want it to itself contain descendant <a> links, nor any <dfn>s, 
                # so we transform those descendants into <span>s
                for descendant in embeddedLinks:
                  if descendant.tag == "a" or descendant.tag == "dfn":
                      descendant.tag = "span"
                  # we need to remove any @href attributes left over in any
                  # descendants that we were <a> links
                  if "href" in descendant.attrib:
                      del descendant.attrib["href"]
                  # this descendant might be an <a> element that we added an
                  # id attribute to earlier and/or some other element with an ia
                  # attribute ; but we don't want to duplicate the id attributes
                  # here, so drop any id attribute we find
                  if "id" in descendant.attrib:
                      del descendant.attrib["id"]
                return headingLink
            elif node.getprevious() == None:
                node = node.getparent()
            else:
                node = node.getprevious()
                # note from MikeSmith: dunno the purpose of the following; just
                # ported it over as-is from Hixie's dfn.js because it's there
                if isinstance(node.tag,str) and node.get("class") == "impl":
                    node = xpath("node()[last()]")
        return None

    def addTerms(self, ElementTree, **kwargs):
        to_remove = set()
        in_terms = False
        for node in ElementTree.iter():
            if in_terms:
                if node.tag is etree.Comment and \
                   node.text.strip(utils.spaceCharacters) == u"end-index-terms":
                    if node.getparent() is not terms_parent:
                        raise DifferentParentException(u"begin-index-terms and end-index-terms have different parents")
                    in_terms = False
                else:
                    to_remove.add(node)
            elif node.tag is etree.Comment:
                if node.text.strip(utils.spaceCharacters) == u"begin-index-terms":
                    terms_parent = node.getparent()
                    in_terms = True
                    node.tail = None
                    node.addnext(deepcopy(self.terms))
                    self.indentNode(node.getnext(), 0, **kwargs)
                elif node.text.strip(utils.spaceCharacters) == u"index-terms":
                    node.addprevious(etree.Comment(u"begin-index-terms"))
                    self.indentNode(node.getprevious(), 0, **kwargs)
                    node.addprevious(deepcopy(self.terms))
                    self.indentNode(node.getprevious(), 0, **kwargs)
                    node.addprevious(etree.Comment(u"end-index-terms"))
                    self.indentNode(node.getprevious(), 0, **kwargs)
                    node.getprevious().tail = node.tail
                    to_remove.add(node)
        for node in to_remove:
            node.getparent().remove(node)

    def indentNode(self, node, indent=0, newline_char=u"\n", indent_char=u" ",
                   **kwargs):
        whitespace = newline_char + indent_char * indent
        if node.getprevious() is not None:
            if node.getprevious().tail is None:
                node.getprevious().tail = whitespace
            else:
                node.getprevious().tail += whitespace
        else:
            if node.getparent().text is None:
                node.getparent().text = whitespace
            else:
                node.getparent().text += whitespace

class DifferentParentException(utils.AnolisException):
    """begin-index-terms and end-index-terms do not have the same parent."""
    pass
