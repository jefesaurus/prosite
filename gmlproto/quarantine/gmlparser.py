
static_url="/home/geoff/workspace/gmlproto/quarantine/testbed/"

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

  __metaclass__ = AutoExtendReqs

  def __init__(self, iterable=(), **attributes):
    self.attr=attributes
    list.__init__(self,iterable)
    self.setDefaults()


  def __repr__(self):
    return '%s(%r)' % (type(self).__name__,  self.attr)

  def printTree(self, pre):
    print pre + str(self.validate()) + self.__repr__()
    for child in self:
      child.printTree(pre + "|   ")
    print pre + "|___"



#======= main output methods to extended
  def toHTML(self):
    return self.finalProcessor(self.start() + self.middle() + self.end())

#======= try to stick to these if possible
  def start(self):
    return "" 


#======= Pretty much should only be messing with middle if this is a leaf node, i.e. something you can guarantee will not be containing more elements
  def middle(self):
    out=""
    for child in self:
      out+=str(child.toHTML())
    return out

  def end(self):
    return ""

#===========================================


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
      if attr not in self.possible_attr and attr not in self.required_attr:
        return (True, "Extraneous args")
    return (True, "All good")

  def setDefaults(self):
    for attrName, val in self.default_attr.iteritems():
      if attrName not in self.attr: self.attr[attrName]=val

#=========================================================================
#     HTML IMPLEMENTATIONS
#=========================================================================

#==================  SINGLE NODES ==================


class link(treeNode):
  reqs=["url"]
  possibles=["text"]

  def middle(self):
    if 'text' in self.attr: display=self.attr['text']
    else: display = self.attr['url']
    return "<a href=\"" + self.attr["url"] + "\">" + display + "</a>"

class plainText(treeNode):
  reqs=["text"]
  def middle(self):
    return self.attr["text"]

class image(treeNode):
  reqs=['src']
  possibles=['width','height','center']
  defaults={'center':True,'width':700,'height':467}

  def middle(self):
    return "<img " + ('class=\"center\"' if self.attr['center'] else '') + "src=\""  + static_url + self.attr['src'] + "\" width=\""+ str(self.attr['width']) + "\" height=\"" + str(self.attr['height']) + "\" />"

class blankLine(treeNode):
  def middle(self):
    return "<p>&nbsp;</p>"

class youtube(treeNode):
  reqs=["src"]
  possibles=["center"]
  defaults={'center':True}
  def middle(self):
    return "<object class=\"center\" width=\"560\" height=\"315\"><iframe width=\"560\" height=\"315\" src=\"" + self.attr['src'] + "\" frameborder=\"0\" allowfullscreen></iframe></object>"

#=================  SANDWICH NODES =================

class genericDouble(treeNode):
  def __init__(self, name, **attributes):
    self.name = name
    treeNode.__init__(self,**attributes)

  def start(self):
    argstring= ' '
    for arg, val in self.attr.iteritems():
      argstring += arg + '=' + '\"' + str(val) + '\"' + ' '
    return '<' + self.name + argstring[:-1] + '>'
  def end(self):
    return '</' + self.name + '>'

class genericSingle(treeNode):
  def __init__(self, name, **attributes):
    self.name = name
    treeNode.__init__(self,**attributes)

  def middle(self):
    argstring= ' '
    for arg, val in self.attr.iteritems():
      argstring += arg + '=' + '\"' + str(val) + '\"' + ' '
    
    return '<' + self.name + argstring[:-1] + '/>'


class innerBody(treeNode):
  def start(self):
    return "<div style=\"width:750px; font-family: Arial, Helvetica, sans-serif; font-size: 16px;\">"
  def end(self):
    return "</div>"






def make(node,filename):
  output=node.toHTML()
  file = open(filename,"w+")
  file.writelines(output)
  file.close()

html=genericDouble('html', work="2000")
head=genericDouble('head')
body=genericDouble('body')
css=genericSingle('link',href=static_url+"styles.css",rel="stylesheet",type="text/css")


main=innerBody()
sub=innerBody()
ln1=link(url="https://www.google.com",text="yay link1")
img1=image(src="dawg",width="200")
bl1=blankLine()
text1=plainText(text="Nice work, son")
yt1=youtube(src="http://www.youtube.com/embed/oefI_XgCkLg")

sub.append(ln1)
sub.append(bl1)
sub.append(img1)
main.append(text1)
main.append(sub)
main.append(yt1)

body.append(main)
head.append(css)
html.append(head)
html.append(body)


html.printTree('')
print html.toHTML()
filename="/home/geoff/workspace/gmlproto/quarantine/testbed/index.html"
make(html,filename)
