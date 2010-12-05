<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:h="http://www.w3.org/1999/xhtml"
  exclude-result-prefixes="h"
  version='1.0'>
  <xsl:param name="RCSREVISION"/>
  <xsl:output method="html" indent="no" encoding="ascii"
    doctype-public="-//W3C//DTD HTML 4.01//EN"
    />
  <xsl:template match="node() | @*">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="style[1]">
    <xsl:text>&#10;</xsl:text>
    <link href="whatwg.css" rel="stylesheet"/>
    <xsl:text>&#10;</xsl:text>
    <xsl:copy-of select="."/>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>
  <xsl:template match="style[contains(.,'.domintro:before')]"/>
  <xsl:template match="link[starts-with(@href,'http://www.w3.org/StyleSheets/TR/')][last()]">
    <xsl:copy-of select="."/>
    <xsl:text>&#10;</xsl:text>
    <link href="style.css" rel="stylesheet"/>
    <xsl:text>&#10;</xsl:text>
    <script src="link-fixup.js"></script>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>
  <xsl:template match="h1">
    <h1>
      <xsl:text>HTML5</xsl:text>
      <xsl:text> </xsl:text>
      <span class="edition">Edition for Web Authors</span>
      <xsl:text> </xsl:text>
      <span class="rcsrevision">
        <xsl:value-of select="concat('revision ',$RCSREVISION)"/>
      </span>
    </h1>
  </xsl:template>
  <xsl:template match="title">
    <title>HTML5 (Edition for Web Authors)</title>
    <xsl:text>&#10;</xsl:text>
    <meta name="viewport" content="width=device-width;"/>
    <xsl:text>&#10;</xsl:text>
    <meta content='IE=edge,chrome=1' http-equiv='X-UA-Compatible'/>
  </xsl:template>
  <xsl:template match="a[normalize-space(.)='http://www.w3.org/TR/html5/']">
    <a href="http://www.w3.org/TR/html5/author/">http://www.w3.org/TR/html5/author/</a>
  </xsl:template>
  <xsl:template match="a[normalize-space(.)='http://dev.w3.org/html5/spec/Overview.html']">
    <a
      href="http://dev.w3.org/html5/spec-author-view/">http://dev.w3.org/html5/spec-author-view/</a>
  </xsl:template>
  <xsl:template match="a[starts-with(normalize-space(.),'http://www.w3.org/TR/2010/WD-html5-201')]
    [not(normalize-space(.)='http://www.w3.org/TR/2010/WD-html5-20100304/')]
    ">
    <xsl:variable name="href">
      <xsl:value-of select="concat(.,'author/')"/>
    </xsl:variable>
    <a href="{$href}"><xsl:value-of select="$href"/></a>
  </xsl:template>
  <xsl:template match="p[contains(normalize-space(.),'This specification is available in the following formats')]">
    <p>
      <xsl:text>This specification is available in the following formats: </xsl:text>
      <a href="spec.html">single page HTML</a>
      <xsl:text>, </xsl:text>
      <a href="Overview.html">multipage HTML</a>
      <xsl:text>, </xsl:text>
      <a href="http://dev.w3.org/html5/spec/">full specification</a>.
      <xsl:text>This is revision </xsl:text>
      <xsl:value-of select="$RCSREVISION"/>
      <xsl:text>.</xsl:text>
    </p>
  </xsl:template>
  <xsl:template match="h2[@id='abstract']">
    <xsl:copy-of select="."/>
    <xsl:text>&#10;</xsl:text>
    <p class="strong-note">This is a strict subset of the
      <a href="http://dev.w3.org/html5/spec/">HTML5 specification</a>
      that omits user-agent (UA) implementation details. It is
      targeted toward Web authors and others who are not UA
      implementors and who want a view of the HTML specification
      that focuses more precisely on details relevant to using the
      HTML language to create Web documents and Web applications.
      Because this document does not provide implementation
      conformance criteria, UA implementors should not rely on it,
      but should instead refer to the full specification.</p>
  </xsl:template>
  <xsl:template match="p[@id='wip']"/>
  <xsl:template match="*[@id='references']" name="insert-index-of-terms">
    <xsl:text>&#10;</xsl:text>
    <h2 id="index-of-terms" class="no-num">Index of terms</h2>
    <xsl:text>&#10;</xsl:text>
    <xsl:comment>index-terms</xsl:comment>
    <xsl:text>&#10;</xsl:text>
    <xsl:copy-of select="."/>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>
  <xsl:template match="//script[1]">
    <xsl:text>&#10;</xsl:text>
    <xsl:copy-of select="document('../script.xml')"/>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>
</xsl:stylesheet>
