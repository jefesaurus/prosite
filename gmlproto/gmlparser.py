

'''
filename="test.gml"

file=open(filename,"r")
if file:
  line=file.readline()
while line:

  for char in line:
    if char  

  if line[0] and line[0] == "`":
    print "TRUE"
  line=file.readline()
'''
class AutoExtendReqs(type):
  def __new__(cls, name, bases, attrs):

    required_attr=[]
    possible_attr=[]
    default_attr={}

    for base in bases:
      try:
        required_attr.extend(getattr(base, 'required_attr'))
        possible_attr.extend(getattr(base, 'possible_attr'))
        default_attr=dict(default_attr.items() + getattr(base, 'default_attr').items())
      except AttributeError:
        pass
    try:
      required_attr.extend(attrs.pop('reqs'))
      possible_attr.extend(attrs.pop('possibles'))
      default_attr=dict(default_attr.items() + attrs.pop('defaults').items())

    except KeyError:
      pass
    attrs['required_attr'] = required_attr 
    attrs['possible_attr'] = possible_attr 
    attrs['default_attr'] = default_attr 
    return type.__new__(cls, name, bases, attrs) 



class treeNode(list):
  required_attr=[]
  possible_attr=[]
  default_attr={}

 # __metaclass__ = AutoExtendReqs

  def __init__(self, iterable=(), **attributes):
    self.attr=attributes
    list.__init__(self,iterable)
    self.setDefaults()


  def __repr__(self):
    return '%s(%s, %r)' % (type(self).__name__, list.__repr__(self), self.attr)



#======= main output methods to extended
  def toHTML(self):
    return self.finalProcessor(self.start() + self.middle() + self.end())

#======= try to stick to these if possible
  def start(self):
    return "" 

  def middle(self):
    out=""
    for child in self:
      print child
      out+=str(child.toHTML())
    return out

  def end(self):
    return ""

#===========================================

#slaps some center tags around provided text
  def center(self, text):
    return "<p class=\"centeredImage\">" + text + "</p>"

#intended for extension by subclasses that wish to add some stuff(condiditonally) before returning
  def finalProcessor(self,inp):
    #loopback by default
    return inp


  def isLeaf(self):
    return len(self)==0

#intended to determine whether the necessary args are supplied or not
  def validate(self):
    for req in self.required_attr:
      if req not in self.attr.keys():

        return (False, "Missing required args")
    for attr in self.attr.keys():
      if attr not in self.possible_attr:
        return (True, "Extraneous args")
    return (True, "All good")

  def setDefaults(self):
    for attrName, val in self.default_attr.iteritems():
      if attrName not in self.attr: self.attr[attrName]=val



#=========================================================================
#     HTML IMPLEMENTATIONS
#=========================================================================

#==================  SINGLE NODES ==================

class plainText(treeNode):
  reqs=["text"]
  def middle(self):
    return self.attr["text"]

class link(treeNode):
  reqs=["url","text"]
  def middle(self):
    return "<a href=\"" + self.attr["url"] + "\">" + self.attr["text"] + "</a>"

class blankLine(treeNode):
  def middle(self):
    return "<p>&nbsp;</p>"

class image(treeNode):
  reqs=["src"]
  possibles=["width","height"]
  defaults={'center':True,'width':700,'height':467}

  def finalProcessor(self,inp):
    outp=inp
    if self.attr['center']: outp = self.center(outp)
    return outp

  def middle(self):
    return "<img src=\"" + self.attr["src"] + "\" width=\""+ str(self.attr['width']) + "\" height=\"" + str(self.attr['height']) + "\" />"


class youtube(treeNode):
  reqs=["src"]
  possibles=["center"]
  defaults={'center':True}
  def finalProcessor(self, inp):
    outp=inp
    if self.attr['center']: outp = self.center(outp)
    return outp
  def middle(self):
    return "<object width=\"480\" height=\"385\"><param name=\"wmode\" value=\"transparent\" /><param name=\"movie\" value=\"" + self.attr["src"]  + "\"></param><param name=\"allowFullScreen\" value=\"true\"></param><param name=\"allowscriptaccess\" value=\"always\"></param><embed src=\""+ self.attr["src"] +"\" type=\"application/x-shockwave-flash\" allowscriptaccess=\"always\" allowfullscreen=\"true\" width=\"480\" height=\"385\" wmode=\"transparent\"></embed></object>"




#=================  SANDWICH NODES =================

class header1(treeNode):
  possibles=["center"]
  defaults={'center':False}

  def finalProcessor(self,inp):
    outp=inp
    if self.attr['center']: outp = self.center(outp)
    return outp

  def start(self):
    return "<h1>"
  def end(self):
    return "</h1>"

class innerBody(treeNode):
  def start(self):
    return "<div style=\"width:750px; font-family: Arial, Helvetica, sans-serif; font-size: 16px;\">"
  def end(self):
    return "</div>"







refer=link(url="www.google.com",text="google yo")

main=innerBody()
img1=image(src="dog")
text1=plainText("This is the dog. it jumps over a lazy brown fox.")
space1=blankLine()
text2=plainText("This is the dog. it jumps over a crazy brown fox.")

main.extend([img1,text1,space1,text2])
print main.toHTML()
