<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fn="http://www.w3.org/2005/02/xpath-functions" xmlns:odml="http://www.g-node.org/odml">
   <!-- ************************************************  -->
   <!--                   root template                   -->
   <xsl:template match="odML">
      <xsl:variable name="repository" select="repository"/>
      <html>
         <style type="text/css">
            body { margin-left:2%; margin-top:10px; padding:0;} div { border:0px solid #888; }

            #navigationContainer { left:10%; width:95%;}

            #contentContainer { left:10%; width:95%;}
         </style>

         <body>
            <a name="top" style="color:#336699"><h1>odML - Metadata</h1></a>
            <div id="navigationContainer">
               <p>
                  <hr style="color:yellow; background-color:#336699; height:4px; margin-right:0; text-align:right; border:1px dashed black;"/>
                  <h2>Document info</h2>
                  <b>Author: </b><xsl:if test="author"><xsl:value-of select="author"/></xsl:if><br/>
                  <b>Date: </b><xsl:if test="date"><xsl:value-of select="date"/></xsl:if><br/>
                  <b>Version: </b><xsl:if test="version"><xsl:value-of select="version"/></xsl:if><br/>
                  <b>Repository: </b><xsl:if test="repository"><xsl:value-of select="repository"/></xsl:if><br/>
               </p>

               <hr style="color:yellow; background-color:#336699; height:4px; margin-right:0; text-align:right; border:1px dashed black;"/>

               <h2>Structure</h2>
               <font  size ="-1" >
                  <xsl:if test="section">
                     <xsl:for-each select="section">
                        <li>
                           <xsl:call-template name="sectionTemplate">
                              <xsl:with-param name="navigation">1</xsl:with-param>
                              <xsl:with-param name="anchorBase">Sec</xsl:with-param>
                              <xsl:with-param name="url" select="$repository"/>
                           </xsl:call-template>
                        </li>
                     </xsl:for-each>
                  </xsl:if></font>
            </div>

            <div id="contentContainer">
               <hr style="color:yellow; background-color:#336699; height:4px; margin-right:0; text-align:right; border:1px dashed black;"/>
               <h2>Content</h2>

               <xsl:if test="section">
                  <xsl:for-each select="section">
                     <xsl:call-template name="sectionTemplate">
                        <xsl:with-param name="navigation">0</xsl:with-param>
                        <xsl:with-param name="anchorBase">Sec</xsl:with-param>
                        <xsl:with-param name="url" select="$repository"/>
                     </xsl:call-template>
                  </xsl:for-each>
               </xsl:if>
            </div>
         </body>
      </html>
   </xsl:template>

   <!-- ************************************************  -->
   <!--              section template.                    -->
   <xsl:template name="sectionTemplate" match="section">
      <xsl:param name="navigation"/>
      <xsl:param name="anchorBase"/>
      <xsl:param name="url"/>
      <!-- create the anchor for the navigation menu-->
      <xsl:variable name="anchorName" select="concat($anchorBase,position())"/>
      <!-- set new baseurl if specified within this section otherwise use the old one -->
      <xsl:variable name="repository">
         <xsl:choose>
            <xsl:when test="repository">
               <xsl:value-of select ="repository"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select ="$url"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!-- print out the content -->
      <xsl:choose>
         <!--  fill the navigation container if this is the task (navigation param = 1)  -->
         <xsl:when test="$navigation = 1">
            <!-- create a link to the anchor in the content container  -->
            <ol style="compact">
               <font size="normal"><a href="#{$anchorName}">
                  <xsl:value-of select="name"/> (type: <xsl:value-of select="type"/>)
               </a></font>
               <!--  recursive call if there are subsections  -->
               <xsl:if test="section">
                  <xsl:for-each select="section">
                     <xsl:call-template name="sectionTemplate">
                        <xsl:with-param name="navigation" select="$navigation"/>
                        <xsl:with-param name="anchorBase" select="concat($anchorName,'SubSec')"/>
                        <xsl:with-param name="url" select="$repository"/>
                     </xsl:call-template>
                  </xsl:for-each>
               </xsl:if>
            </ol>
         </xsl:when>
         <!--  otherwise use template to display the content (navigation !=1) -->
         <xsl:otherwise>
            <a name="{$anchorName}"><h3>Section: <xsl:value-of select="name"/> </h3></a>
            <p>
               <b>Type: </b><xsl:value-of select="type"/><br/>
               <xsl:choose>
                  <xsl:when test ="repository">
                     <b>Repository: </b><xsl:value-of select="repository"/><br/>
                  </xsl:when>
                  <xsl:otherwise>
                     <b>Repository: </b><xsl:value-of select="$repository"/><br/>
                  </xsl:otherwise>
               </xsl:choose>
               <b>Link: </b><xsl:if test="link"><xsl:value-of select="link"/></xsl:if><br/>
               <b>Include:</b> <xsl:if test="include"><font color="red"><xsl:value-of select="include"/></font></xsl:if><br/>
               <b>Definition:</b> <xsl:if test="definition"><xsl:value-of select="definition"/></xsl:if><br/>
            </p>

            <!--  Check if there are any properties  -->
            <xsl:if test="property">
               <table border="1" rules="rows" width="100%"><font size ="-1">
                  <tr bgcolor="#336699" valign="middle" align="left">
                     <th><font size="+1" color="white"><b>Name</b></font></th>
                     <th><font size="+1" color="white"><b>Value</b></font></th>
                     <th><font size="+1" color="white"><b>Uncertainty</b></font></th>
                     <th><font size="+1" color="white"><b>Unit</b></font></th>
                     <th><font size="+1" color="white"><b>Type</b></font></th>
                     <th><font size="+1" color="white"><b>Reference</b></font></th>
                     <th><font size="+1" color="white"><b>Definition</b></font></th>
                     <th><font size="+1" color="white"><b>Value origin</b></font></th>
                     <!--
                       <th><font size="+1" color="white"><b>Dependency</b></font></th>
                       <th><font size="+1" color="white"><b>Dependency Value</b></font></th>
                     -->
                  </tr>
                  <xsl:for-each select="property">
                     <xsl:variable name="anchor">
                        <xsl:value-of select ="name"/>
                     </xsl:variable>
                     <tr>
                        <td width="15%"><a name="{$anchor}"/>
                           <p><xsl:value-of select="name"/></p>
                        </td>
                        <td width="10%"><p><xsl:value-of select="value"/></p></td>
                        <td width="5%"><p><xsl:value-of select="uncertainty"/></p></td>
                        <td width="5%"><p><xsl:value-of select="unit"/></p></td>
                        <td width="5%"><p><xsl:value-of select="type"/></p></td>
                        <td width="5%"><p><xsl:value-of select="reference"/></p></td>
                        <td width="22.5%"><p><xsl:value-of select="definition"/></p></td>
                        <td width="7.5%%"><p><xsl:value-of select="value_origin"/></p></td>
                        <!--
                          <td width="5%"><p><xsl:value-of select="dependency"/></p></td>
                          <td width="5%"><p><xsl:value-of select="dependencyValue"/></p></td>
                        -->
                     </tr>
                  </xsl:for-each></font>
               </table>
            </xsl:if>
            <a href="#top"><tiny>top</tiny></a>
            <hr style="background-color:#336699; height:1px; margin-right:0; text-align:right;"/>
            <!--  recursive call if there are subsections  -->
            <xsl:if test="section">
               <xsl:for-each select="section">
                  <xsl:call-template name="sectionTemplate">
                     <xsl:with-param name="navigation" select="$navigation"/>
                     <xsl:with-param name="anchorBase" select="concat($anchorName,'SubSec')"/>
                     <xsl:with-param name="url" select="$repository"/>
                  </xsl:call-template>
               </xsl:for-each>
            </xsl:if>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:template>

</xsl:stylesheet>
