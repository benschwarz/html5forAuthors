<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:h="http://www.w3.org/1999/xhtml"
  exclude-result-prefixes="h"
  version='1.0'>
  <xsl:output method="html" indent="no" encoding="ascii"
    doctype-public="-//W3C//DTD HTML 4.01//EN"
    />
  <xsl:key name="local-frags" match="." use="concat('#',@id)"/>
  <xsl:key name="filename-map" match="." use="h:li"/>
  <xsl:template match="node() | @*">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="a[@href[starts-with(.,'#')]]">
    <xsl:variable name="ref" select="@href"/>
    <xsl:choose>
      <xsl:when test="not(key('local-frags',$ref))">
        <!-- * <xsl:message> -->
          <!-- * <xsl:value-of select="$ref"/> -->
        <!-- * </xsl:message> -->
        <xsl:variable name="filename">
          <xsl:call-template name="get-filename">
            <xsl:with-param name="ref" select="$ref"/>
          </xsl:call-template>
        </xsl:variable>
        <a>
          <xsl:copy-of select="@*"/>
          <xsl:attribute name="href">
            <xsl:value-of select="concat('http://dev.w3.org/html5/spec/',$filename,'.html',$ref)"/>
          </xsl:attribute>
          <xsl:attribute name="class">full-spec-link</xsl:attribute>
          <xsl:attribute name="title">
            <xsl:text>Read about this "</xsl:text>
            <xsl:value-of select="normalize-space(.)"/>
            <xsl:text>" reference in the full HTML5 spec.</xsl:text>
          </xsl:attribute>
          <xsl:apply-templates/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  <xsl:template name="get-filename">
    <xsl:param name="ref"/>
    <xsl:for-each select="document('../fragment-links.xhtml')">
      <xsl:value-of select="key('filename-map',$ref)/*[2]"/>
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>
