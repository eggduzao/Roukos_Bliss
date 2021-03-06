"""
Util
===================
The Util classes contains many utilities needed by other classes such as the paths to input files.

Authors: Eduardo Gade Gusmao.
"""

# Python
from __future__ import print_function
import os
import sys
import shutil
import ConfigParser
import traceback
from optparse import OptionParser,BadOptionError,AmbiguousOptionError

def npath(filename):
    """Returns a normalised, absolute version of the path, with expanded user directory."""
    return os.path.abspath(os.path.expanduser(filename))

class HelpfulOptionParser(OptionParser):
    """An OptionParser that prints full help on errors. Inherits OptionParser."""
    def error(self, msg):
        self.print_help(sys.stderr)
        self.exit(2, "\n%s: error: %s\n" % (self.get_prog_name(), msg))

class PassThroughOptionParser(HelpfulOptionParser):
    """When unknown arguments are encountered, bundle with largs and try again, until rargs is depleted. sys.exit(status) will still be called if a known argument is passed incorrectly (e.g. missing arguments or bad argument types, etc.). Inherits HelpfulOptionParser."""
    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                HelpfulOptionParser._process_args(self,largs,rargs,values)
            except (BadOptionError,AmbiguousOptionError), e:
                pass
                #largs.append(e.opt_str)

class Html:
    """Represent an HTML file.

    *Keyword arguments:*

        - name -- Name of the HTML document.
        - links_dict -- Dictionary with the upper links.
        - fig_dir -- Figure directory (default = None).
        - fig_rpath -- Relative figure path (default = '../fig').
        - cluster_path_fix -- deprecated.
        - RGT_header -- Whether to print RGT header (default = True).
        - other_logo -- Other tool logos (default = None).
        - homepage -- Homepage link (default = None).

    .. warning:: cluster_path_fix is going to be deprecated soon. Do not use it.
    """

    def __init__(self, name, links_dict, fig_dir=None, fig_rpath="../fig", cluster_path_fix="", 
                 RGT_header=True, other_logo=None, homepage=None):

        # Variable initializations
        self.name = name
        self.links_dict = links_dict
        self.cluster_path_fix = cluster_path_fix
        self.document = []
        self.image_data = ImageData()
        self.other_logo = other_logo
        self.homepage = homepage
        
        # Initialize document
        if fig_dir:
            self.copy_relevent_files(fig_dir)
            self.create_header(relative_dir=fig_rpath, RGT_name=RGT_header, other_logo=other_logo)
        else:
            self.create_header(relative_dir=fig_rpath, RGT_name=RGT_header, other_logo=other_logo)
        
        self.add_links()

    def copy_relevent_files(self, target_dir):
        """Copies relevant files to relative paths.

        *Keyword arguments:*

            - target_dir -- Target directory to copy files.
        """

        try:
            os.stat(target_dir)
        except:
            os.mkdir(target_dir)
        shutil.copyfile(src=self.cluster_path_fix+self.image_data.get_rgt_logo(), dst=os.path.join(target_dir,"rgt_logo.gif"))
        shutil.copyfile(src=self.cluster_path_fix+self.image_data.get_css_file(), dst=os.path.join(target_dir,"style.css"))
        #shutil.copyfile(src=self.cluster_path_fix+self.image_data.get_jquery(), dst=os.path.join(target_dir,"jquery-1.11.1.js"))
        shutil.copyfile(src=self.cluster_path_fix+self.image_data.get_tablesorter(), dst=os.path.join(target_dir,"jquery.tablesorter.min.js"))
        #shutil.copyfile(src=self.cluster_path_fix+self.image_data.get_jquery_metadata(), dst=os.path.join(target_dir,"jquery.metadata.js"))
        #shutil.copyfile(src=self.cluster_path_fix+self.image_data.get_tablesorter(), dst=os.path.join(target_dir,"jquery.metadata.js"))
        if self.other_logo:
            if self.other_logo == "TDF":
                shutil.copyfile(src=self.cluster_path_fix+self.image_data.get_tdf_logo(), dst=os.path.join(target_dir,"tdf_logo.png"))
            if self.other_logo == "viz":
                shutil.copyfile(src=self.cluster_path_fix+self.image_data.get_viz_logo(), dst=os.path.join(target_dir,"viz_logo.png"))
          
    def create_header(self, relative_dir=None, RGT_name=True, other_logo=None):
        """Creates default document header.

        *Keyword arguments:*

            - relative_dir -- Define the directory to store CSS file and RGT logo so that the html code can read from it (default = None).
            - RGT_name -- Whether to print RGT name (default = True).
            - other_logo -- Other tool logos (default = None)
        """

        self.document.append('<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>') 
            
        if relative_dir:
            #self.document.append('<script type="text/javascript" src="'+relative_dir+'/jquery-1.11.1.js"></script>')
            self.document.append('<script type="text/javascript" src="'+relative_dir+'/jquery.tablesorter.min.js"></script>')
            #self.document.append('<script type="text/javascript" src="'+relative_dir+'/jquery.metadata.js"></script>')
        else:
            #self.document.append('<script type="text/javascript" src="'+self.cluster_path_fix+self.image_data.get_jquery()+'"></script>')
            self.document.append('<script type="text/javascript" src="'+self.cluster_path_fix+self.image_data.get_tablesorter()+'"></script>')
            #self.document.append('<script type="text/javascript" src="'+self.cluster_path_fix+self.image_data.get_jquery_metadata()+'"></script>')
        
        self.document.append("<html>")
        self.document.append("<head><meta http-equiv=\"Content-Type\" content=\"text/html\"><title>RGT "+self.name+"</title>")

        self.document.append("<style type=\"text/css\">")
        self.document.append("<!--")
        
        if relative_dir:
            self.document.append("@import url(\""+relative_dir+"/style.css\");")
        else:
            self.document.append("@import url(\""+self.cluster_path_fix+self.image_data.get_css_file()+"\");")
        
        self.document.append("-->")
        self.document.append("</style></head>")
        self.document.append("<body topmargin=\"0\" leftmargin=\"0\" rightmargin=\"0\" bottommargin=\"0\" marginheight=\"0\" marginwidth=\"0\" bgcolor=\"#FFFFFF\">")        
        
        self.document.append("<h3 style=\"background-color:white; border-top:3px solid gray; border-bottom:3px solid gray;\">")
        self.document.append("<table border=\"0\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">")
        self.document.append("  <tr>")

        # Logo
        if relative_dir:            
            self.document.append("    <td width=\"5%\">")
            if self.homepage: self.document.append("<a href=\""+self.homepage+"\">")
            if other_logo == "TDF":
                self.document.append("    <img border=\"0\" src=\""+relative_dir+"/tdf_logo.png"+"\" width=\"130\" height=\"100\">")
            elif other_logo == "viz":
                self.document.append("    <img border=\"0\" src=\""+relative_dir+"/viz_logo.png"+"\" width=\"130\" height=\"100\">")
            else:
                self.document.append("    <img border=\"0\" src=\""+relative_dir+"/rgt_logo.gif\" width=\"130\" height=\"100\">")
            if self.homepage: self.document.append("</a>")
            self.document.append("    </td>")
            
        else:
            self.document.append("    <td width=\"5%\"><img border=\"0\" src=\""+self.cluster_path_fix+self.image_data.get_rgt_logo()+"\" width=\"130\" height=\"100\"></td>")

        # Gap
        self.document.append("     <td width=\"5%\"></td>")
        # Title
        if RGT_name:
            self.document.append("    <td width=\"90%\"><p align=\"left\"><font color=\"black\" size=\"5\">Regulatory Genomics Toolbox - "+self.name+"</font></td>")
        else:
            self.document.append("    <td width=\"90%\"><p align=\"left\"><font color=\"black\" size=\"5\">"+self.name+"</font></td>")
        
        self.document.append("  </tr>")
        self.document.append("</table>")
        self.document.append("</h3>")

    def add_links(self):
        """Adds all the links."""
        for k in self.links_dict.keys():

            self.document.append("<a class=\"pure-button\" href=\""+\
                                 os.path.join(self.cluster_path_fix,self.links_dict[k])+\
                                 "\">"+\
                                 "<font size='1'>"+k+"</font>"+"</a>")

        #self.document.append("<table border=\"0\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">")
        #self.document.append("  <tr>")
        #self.document.append("    <td width=\"100%\"><font color=\"black\" face=\"Arial\" size=\"4\"><b>&nbsp;&nbsp;")
        #link_str = "    "+" &nbsp;&nbsp; |&nbsp;&nbsp; ".join(["<a href=\""+os.path.join(self.cluster_path_fix,self.links_dict[k])+"\">"+k+"</a>" for k in self.links_dict.keys()])
        #self.document.append(link_str)
        #self.document.append("    </b></font></td>")
        #self.document.append("  </tr>")
        #self.document.append("</table>")

    def create_footer(self):
        """Adds footer."""
        self.document.append("<br><br>")
        self.document.append("<p align=\"center\"><font face=\"Arial\" color=\"#000000\" size=\"2\">")
        self.document.append("For more details please visit the <a href=\"http://www.regulatory-genomics.org/\"> RGT Website </a>")
        self.document.append("</font></p>")
        self.document.append("<h3 style=\"background-color:white; border-top:3px solid gray;\"></h3>")
        self.document.append("</body>")
        self.document.append("</html>")

    def add_heading(self, heading, align = 50, color = "black", face = "Arial", size = 5, bold = True, idtag=None):
        """Creates a heading.
        
        *Keyword arguments:*

            - heading -- The heading title.
            - align -- Alignment of the heading. Can be either an integer (interpreted as left margin) or string (interpreted as HTML positional argument (default = 50).
            - color -- Color of the heading (default = "black").
            - face -- Font of the heading (default = "Arial").
            - size -- Size of the heading (HTML units [1,7]) (default = 5).
            - bold -- Whether the heading is bold (default = True).
            - idtag -- Add ID tag in the heading element (default = None).
        """

        if idtag:
            idstr = ' id="'+idtag+'"'
        else:
            idstr = ""

        # Creating header
        content_str = ""
        if(isinstance(align,int)): content_str += "<p style=\"margin-left: "+str(align)+"\""+idstr+">"
        elif(isinstance(align,str)): content_str += "<p align=\""+align+"\""+idstr+">"
        else: pass # ERROR
        content_str += "<font color=\""+color+"\" face=\""+face+"\" size=\""+str(size)+"\""+idstr+">"
        if(bold): content_str += "<b>"
        self.document.append(content_str)

        # Printing heading name
        self.document.append(heading)

        # Creating footing
        end_str = ""
        if(bold): end_str += "</b>"
        end_str += "</font></p>"
        self.document.append(end_str)

    def add_zebra_table(self, header_list, col_size_list, type_list, data_table, align = 50, 
                        cell_align = 'center', auto_width=False, colorcode=None, header_titles=None,
                        border_list=None, sortable=False):
        """Creates a zebra table.

        *Keyword arguments:*

            - header_list -- A list with the table headers in correct order.
            - col_size_list -- A list with the column sizes (integers).
            - type_list -- A string in which each character represents the type of each row.
                  - s = string (regular word or number)
                  - i = image
                  - l = link 
            - data_table -- A table containing the data to be input according to each data type defined.
                  - s = string
                  - i = tuple containing: ("file name", width) width = an integer
                  - l = tuple containing: ("Name","Link")
            - align -- Alignment of the heading. Can be either an integer (interpreted as left margin) or string (interpreted as HTML positional argument) (default = 50).
            - cell_align -- Alignment of each cell in the table (default = center).
            - auto_width -- Adjust the column width by the content automatically regardless of defined col size (default = False).
            - colorcode -- Color code (default = None)
            - header_titles -- Given a list corresponding to the header_list, which defines all the explanation in hint windows (default = None).
            - border_list -- Table borders (default = None).
            - sortable -- Whether it is a sortable table (default = False).
        """
        #if header_notes: self.document.append("<style> .ami div {display:none} .ami:hover div {display:block} </style>")
        
        if not border_list:
            border_list = [""] * len(data_table[0])
        if auto_width: auto= " table-layout: auto"
        else: auto=""


        # Starting table
        type_list = type_list.lower()
        if(isinstance(align,int)): self.document.append("<p style=\"margin-left: "+str(align)+"\">")
        elif(isinstance(align,str)): self.document.append("<p align=\""+align+"\">") 
        else: pass # TODO ERROR
        
        # Table header
        #self.document.append("<table id=\"myTable\" class=\"tablesorter\">")
        
        if sortable: 
            sortableclass=" class=\"tablesorter\""
            tableid="sortable"
        else:
            sortableclass=""
            tableid="hor-zebra"

        self.document.append("<table id=\""+tableid+"\""+sortableclass+auto+">")

        if colorcode:
            for line in colorcode:
                self.document.append(line)

        #############################
        ##### Header ################
        self.document.append("  <thead>")
        if (isinstance(header_list[0], list)):
        # For headers more than one row
            for r, row_list in enumerate(header_list):
                self.document.append("    <tr>")
                header_str = []

                merge_num = [1] * len(row_list)
                for i, value in enumerate(row_list):
                    if value == None:
                        merge_num[last_true] += 1
                        merge_num[i] -= 1
                    else:
                        last_true = i

                for i in range(0,len(row_list)):
                    if merge_num[i] > 1:
                        if header_titles:
                            header_str.append("<th scope=\"col\" width=\""+str(col_size_list[i])+
                                              "\" align=\""+'center'+"\""+" colspan=\""+str(merge_num[i])+"\" "+
                                              "title=\""+header_titles[r][i]+"\""+border_list[i+merge_num[i]-1]+auto+" >"+
                                              row_list[i]+"</th>")
                        else:
                            header_str.append("<th scope=\"col\" width=\""+str(col_size_list[i])+
                                              "\" align=\""+'center'+"\""+" colspan=\""+str(merge_num[i])+"\""+
                                              border_list[i+merge_num[i]-1]+auto+">"+row_list[i]+"</th>")
                        
                    elif merge_num[i] == 0:
                        continue
                    else:
                        if header_titles:
                            header_str.append("<th scope=\"col\" width=\""+str(col_size_list[i])+
                                              "\" align=\""+cell_align+"\" "+
                                              "title=\""+header_titles[r][i]+"\""+border_list[i]+auto+">"+
                                              row_list[i]+"</th>")
                        else:
                            header_str.append("<th scope=\"col\" width=\""+str(col_size_list[i])+
                                              "\" align=\""+cell_align+"\""+border_list[i]+auto+">"+
                                              row_list[i]+"</th>")

                header_str = "    "+"\n    ".join(header_str)
                self.document.append(header_str)
                self.document.append("    </tr>")

        else:
            self.document.append("    <tr>")
            header_str = []
            for i in range(0,len(header_list)):
                if header_titles:
                    header_str.append("<th scope=\"col\" width=\""+str(col_size_list[i])+"\" align=\""+cell_align+"\" "+
                                      "title=\""+header_titles[i]+"\" >"+header_list[i]+"</th>")
                else:
                    header_str.append("<th scope=\"col\" width=\""+str(col_size_list[i])+"\" align=\""+cell_align+"\">"+
                                      header_list[i]+"</th>")
                
            header_str = "    "+"\n    ".join(header_str)
            self.document.append(header_str)
            self.document.append("    </tr>")
        self.document.append("  </thead>")

        
        #############################
        ##### Table body ############
        self.document.append("  <tbody>")
        for i in range(0,len(data_table)):

            # Row type
            if(i%2==0) and not sortable: self.document.append("    <tr class=\"odd\">")
            else: self.document.append("    <tr>")

            # Body data
            for j in range(0,len(data_table[i])):
                if(type_list[j] == "s"):
                    self.document.append("      <td align=\""+cell_align+"\" "+border_list[j]+">"+data_table[i][j]+"</td>")
                elif(type_list[j] == "i"): 
                    self.document.append("      <td align=\""+cell_align+"\"><img src=\""+self.cluster_path_fix+
                                         data_table[i][j][0]+"\" width="+str(data_table[i][j][1])+" ></td>")
                elif(type_list[j] == "l"):
                    self.document.append("      <td align=\""+cell_align+"\"><a href=\""+data_table[i][j][1]+"\">"+
                                         data_table[i][j][0]+"</a></td>")
                else: pass # TODO ERROR

            # Row ending
            self.document.append("    </tr>")
        
        # Finishing table
        self.document.append("</tbody></table></p>")

    def add_fixed_rank_sortable(self):
        """Add jquery for fixing the first column of the sortable table"""
        scripts = ["<script>",
                   "// add custom numbering widget",
                   "$.tablesorter.addWidget({",
                   "    id: 'numbering',",
                   "    format: function(table) {",
                   "        var c = table.config;",
                   "        $('tr:visible', table.tBodies[0]).each(function(i) {",
                   "            $(this).find('td').eq(0).text(i + 1);",
                   "        });",
                   "    }",
                   "});",
                   "$('.tablesorter').tablesorter({",
                   "    // prevent first column from being sortable",
                   "    headers: {",
                   "        0: { sorter: false }",
                   "    },",
                   "    // apply custom widget",
                   "    widgets: ['numbering']",
                   "});",
                   "</script>"]
        for s in scripts:
            self.document.append(s)

    def add_figure(self, figure_path, notes=None, align=50, color="black", face="Arial", size=3, 
                   bold=False, width="800", more_images=None):
        """Add a figure with notes underneath.
        
        *Keyword arguments:*

            - figure_path -- The path to the figure.
            - notes -- A list of strings for further explanation
            - align -- Alignment of the heading. Can be either an integer (interpreted as left margin) or string (interpreted as HTML positional argument) (default = 50).
            - color -- Color (default = 'black').
            - face -- Font (default = 'Arial').
            - size -- Size (default = 3).
            - bold -- Whether it is bold (default = False).
            - width -- Width (default = 800).
            - more_images -- Add more images (default = None).
        """        
        if(isinstance(align,int)): img_str = "<p style=\"margin-left: "+str(align)+"\">"
        elif(isinstance(align,str)): img_str = "<p align=\""+str(align)+"\">"
        else: pass # TODO ERROR
        
        img_str += '<a href="'+figure_path+'"><img src="'+ figure_path +'" width='+width+'></a>'
        
        if more_images:
            for im in more_images:
                img_str += '<a href="'+im+'"><img src="'+ im +'" width='+width+'></a>'
        
        img_str += '</p>'

        self.document.append(img_str)
        if notes:
            if(isinstance(align,int)): 
                note_str = "<p style=\"margin-left: "+str(align)+"\"><font color=\""+color+"\" face=\""+face+"\" size=\""+str(size)+"\ align=\""+ str(align) + "\">"
            elif(isinstance(align,str)):
                note_str = "<p align=\""+str(align)+"\"><font color=\""+color+"\" face=\""+face+"\" size=\""+str(size)+"\ align=\""+ str(align) + "\">"            
            else: pass # TODO ERROR
            
            if(bold): note_str += "<b>"
            for line in notes:
                note_str += line + "<br>" 
            if(bold): note_str += "</b>"
            note_str += "</font></p>"
            self.document.append(note_str)

    def add_free_content(self, content_list):
        """Adds free HTML to the document.

        *Keyword arguments:*

            - content_list -- List of strings. Each string is interpreted as a line in the HTML document.
        """
        for e in content_list: self.document.append(e)

    def add_list(self, list_of_items, ordered=False):
        """Add a list to the document

        *Keyword arguments:*

            - list_of_items -- List of items to add.
            - ordered -- Whether the list is odered (default = False).
        """
        codes = ""

        if ordered: codes += "<ol>"
        else: codes += "<ul>"
        
        for item in list_of_items:
            codes += "<li style=\"margin-left: 50\">"+item+"</li>"
        
        if ordered: codes += "</ol>"
        else: codes += "</ul>"

        self.document.append(codes)
        
    def write(self, file_name):
        """Write HTML document to file name.

        *Keyword arguments:*

            - file_name -- Complete file name to write this HTML document.
        """

        # Add footer - finalize document
        self.create_footer()

        # Writing document to file
        f = open(file_name,"w")
        for e in self.document:
            if e: f.write(e+"\n")
        f.close()

class AuxiliaryFunctions:
    """Class of auxiliary static functions."""

    @staticmethod
    def string_is_int(s):
        """Verifies if a string is a numeric integer.

        *Keyword arguments:*

            - s -- String to verify.
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def string_is_float(s):
        """Verifies if a string is a numeric float.

        *Keyword arguments:*

            - s -- String to verify.
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def correct_standard_bed_score(score):
        """Standardize scores between 0 and 1000.

        *Keyword arguments:*

            - score -- Score.
        """
        return min(max(score,0),1000)

    @staticmethod
    def overlap(t1, t2, strand_specific=False):
        """Checks if one interval contains any overlap with another interval.

        *Keyword arguments:*

            - t1 -- First tuple.
            - t2 -- Second tuple.
  
        *Return:*
            - -1 -- if i1 is before i2.
            - 1 -- if i1 is after i2.
            - 0 -- if there is any overlap.
        """
        if strand_specific:
            if (t1[1] <= t2[0]): return -1  # interval1 is before interval2
            if (t2[1] <= t1[0]): return 1  # interval1 is after interval2
            if t1[4] == t2[2]:
                return 0  # interval1 overlaps interval2
            else:
                return 2  # interval1 overlaps interval2 on the opposite strand
        else:
            if(t1[1] <= t2[0]): return -1 # interval1 is before interval2
            if(t2[1] <= t1[0]): return 1 # interval1 is after interval2
            return 0 # interval1 overlaps interval2

    @staticmethod
    def revcomp(s):
        """Revert complement string.

        *Keyword arguments:*

            - s -- String.
        """
        revDict = dict([("A","T"),("T","A"),("C","G"),("G","C"),("N","N")])
        return "".join([revDict[e] for e in s[::-1]])

        
def which(program):
    """Return path of program or None, see
    http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python"""
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None