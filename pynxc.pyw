#!/usr/bin/env python
from __future__ import with_statement

__author__  = 'Brian Blais <bblais@bryant.edu>'
__version__ = (0,1,6)


import ast_template
import sys
from compiler import parse, walk
from compiler.consts import *
from waxy import *
import os
import subprocess
from optparse import OptionParser
import re
import yaml


pynxc_root,junk=os.path.split(sys.argv[0])
#pynxc_root=os.getcwd()


class MyObject(object):
    
    def __init__(self,name,type='default'):
        
        self.name=name
        self.type=type
        self.datatype=None
        self.value=None


        self.variables=[]

    def __repr__(self):
        return self.type+" "+self.name+" of datatype "+self.datatype.__repr__()+" with value "+self.value.__repr__()


class Variable(MyObject):
    
    def __init__(self,name,datatype='default'):
        
        
        super(Variable,self).__init__(name,'variable')
        self.datatype=datatype
    
        
class Function(MyObject):

    def __init__(self,name,variables=[]):
        
        
        super(Function,self).__init__(name,'function')
        self.variables=variables
        
    
    
    
file_lines=[]

class SecondPassVisitor(ast_template.Visitor):
    """This object goes through and output the code"""

    def __init__(self,fv,stream=sys.stdout,debug=False):

        ast_template.Visitor.__init__(self,stream,debug)
    
        
        self.fv=fv  # first-pass visitor
        self.stream=stream
        self.erase_assign=False
        self.buffer=[]
        self.semicolon=True

        self.writef('#include "NXCDefs.h"\n')
        self.writef(open(os.path.join(pynxc_root,"MyDefs.h"),'rt').read())
            
        
        for d in fv.defines:
            self.writef('#define %s %s\n' % (d[0],d[1]))
        
        self.print_structure_definitions(fv.struct_types)
        
        self.print_typedefs(fv.typedefs)

        if self.debug:
            print "Module Variables Printing "
        
        self.print_variable_definitions(fv.functions['module'].variables)
        self.scope=['module']
        
        
    def type2str(self,datatype):
        if datatype=='Integer':
            return 'int'
        elif datatype=='IntegerPtr':
            return 'int&'
        elif datatype=='Word':
            return 'word'
        elif datatype=='Long':
            return 'long'
        elif datatype=='Byte':
            return 'byte'
        elif datatype=='Short':
            return 'short'
        elif datatype=='String':
            return 'string'
        elif datatype=='Mutex':
            return 'mutex'
        elif datatype in self.fv.struct_types:
            return datatype
        else:
            return 'int'

    def print_typedefs(self,typedefs):
        
        for types in typedefs:
            self.write('typedef %s %s;' % (typedefs[types],types))
            self.NEWLINE()
            self.flush()
            
    def print_structure_definitions(self,struct_types):
        
        for key in struct_types:
            self.write('struct %s ' % key)
            self.INDENT()
            variables=struct_types[key]
            for var in variables:
                self.write(self.type2str(variables[var].datatype))
                self.write(' %s' % variables[var].name)
                self.write(';')
                self.NEWLINE()
            self.DEDENT()
            self.write(';')
            self.NEWLINE()
        
        
    def print_variable_definitions(self,variables):
        for var in variables:
            
            
            if self.debug:
                print "  Variable ",variables[var]
            
            self.write(self.type2str(variables[var].datatype))

            self.write(' %s' % variables[var].name)
                
            if not variables[var].value is None:
                if isinstance(variables[var].value,list):
                    self.write('[]')
                    if not variables[var].value==[]:
                        self.write('={')
                        for v in variables[var].value:
                            self.write(v.__repr__())
                            if not v == variables[var].value[-1]:
                                self.write(',')
                        self.write('}')
                                
                            
                        
                else:
                    val=variables[var].value.__repr__()
                    self.write('= %s' % val.replace("'",'"'))
            self.write(';')
            self.NEWLINE()
            
            if variables[var].datatype in self.fv.struct_types:
                variables2=self.fv.struct_types[variables[var].datatype]
                for var2 in variables2:
                    if variables2[var2].value:
                        val2=variables2[var2].value.__repr__()
                        
                        self.write('%s.%s' % (var,variables2[var2].name))
                        self.write('= %s' % val2.replace("'",'"'))
                        self.write(';')
                        self.NEWLINE()
                
            
            
        self.flush()
        
        
    def flush(self):
        
        if self.buffer:
            for s in self.buffer:
                s=s.replace("'",'"')
                self.stream.write(s)
        
        self.buffer=[]
            
    def DEDENT(self,with_semicolon=False):
        self.indents -=1
        self.NEWLINE()
        self.write('}')
        if with_semicolon:
            self.write(';')
        self.NEWLINE()

    def INDENT(self):
        self.indents += 1
        self.write(' {')
        self.NEWLINE()

    def NEWLINE(self):
        self.write('\n')
        self.write(' ' * 4 * self.indents )
        
    def write(self, data):
        self.buffer.append(data)
            

    def writef(self, data):
        self.write(data)
        self.flush()

        
    def visitBlock(self, block):
        self.INDENT()
        self.v(block)
        self.DEDENT()

    def visitAdd(self, node):
        self.write("(")
        self.v(node.left)
        self.write(" + ")
        self.v(node.right)
        self.write(")")

    def visitAnd(self, node):
        self.write("(")
        for i in range(len(node.nodes)):
            self.write("(")
            self.v(node.nodes[i])
            self.write(")")
            if i < (len(node.nodes) - 1):
                self.write(" && ")
        self.write(")")

    def visitAssAttr(self, node):
        if self.debug:
            print 'visitSecondVisitorAssAttr'
        self.v(node.expr, self)
        self.write(".%s" % node.attrname)

    def visitAssName(self, node):
        self.write(node.name)

    def visitAssign(self, node):
        self.flush()
        self.erase_assign=False
        n=node.nodes[0]


        if self.scope[-1]=='module':
            return

#        try:
#            if (n.name == n.name.upper()) and (len(n.name)>2):  # a definition
#                return
#        except AttributeError:
#            pass   # probably a subscript?
            
        for i in range(len(node.nodes)):
            n = node.nodes[i]
            self.v(n)
            if i < len(node.nodes):
                self.write(" = ")
        self.v(node.expr)
        
        self.write("; ")
        self.NEWLINE()

        
        if self.erase_assign:
            self.buffer=[]

        self.flush()
        
        
    def visitAugAssign(self, node):
        self.v(node.node)
        self.write(" %s " % node.op)
        self.v(node.expr)
        self.write("; ")
        self.NEWLINE()


    def visitBitand(self, node):
        for i in range(len(node.nodes)):
            self.v(node.nodes[i])
            if i < (len(node.nodes) - 1):
                self.write(" & ")

    def visitBitor(self, node):
        for i in range(len(node.nodes)):
            self.v(node.nodes[i])
            if i < (len(node.nodes) - 1):
                self.write(" | ")

    def visitBitxor(self, node):
        for i in range(len(node.nodes)):
            self.v(node.nodes[i])
            if i < (len(node.nodes) - 1):
                self.write(" ^ ")        

    def visitBreak(self, node):
        self.write("break; ")
        self.NEWLINE()
        
    def visitFunction(self, node):
        self.scope.append('function')
    
        hasvar = haskw = hasone = hasboth = False

        ndefaults = len(node.defaults)

        if node.flags & CO_VARARGS:
            hasone = hasvar = True
        if node.flags & CO_VARKEYWORDS:
            hasone = haskw = True
        hasboth = hasvar and haskw

        kwarg = None
        vararg = None
        defargs = []
        newargs = node.argnames[:]

        if ndefaults:
            for i in range(ndefaults):
                defargs.append((newargs.pop(), node.defaults.pop()))
            defargs.reverse()

        func_type=self.fv.functions[node.name].datatype
        if not func_type:
            func_type='void'
            
        if func_type=='default':
            func_type='int'
            
        if node.name=='main':
            self.write("task %s(" % node.name)
        elif node.name.find('task_')==0:
            self.write("task %s(" % node.name)
        elif node.name.find('sub_')==0:
            self.write("sub %s(" % node.name)
        elif node.name.find('inline_')==0:
            self.write("inline %s %s(" % (func_type,node.name.replace('inline_','')))
        else: 
            self.write("%s %s(" % (func_type,node.name))
        

        for i in range(len(newargs)):
            if isinstance(newargs[i], tuple):
                self.write("(%s, %s)" % newargs[i])
            else:
                self.write("int "+newargs[i])
            if i < len(newargs) - 1:
                self.write(", ")
        if defargs and len(newargs):
            self.write(", ")

        for i in range(len(defargs)):
            name, default = defargs[i]
            typename=default.node.name
            
            
            
            self.write("%s %s" % (self.type2str(typename),name))
            #self.v(default)
            if i < len(defargs) - 1:
                self.write(", ")
        
        if vararg:
            if (newargs or defargs):
                self.write(", ")
            self.write(vararg)
        if kwarg:
            if (newargs or defargs or vararg):
                self.write(", ")
            self.write(kwarg)

        self.write(") ")
        self.INDENT()
        
        self.print_variable_definitions(self.fv.functions[node.name].variables)
        
        self.v(node.code)
        self.DEDENT()
        
        self.flush()
        self.scope.pop()
            
        
    def visitCallFunc(self, node):
        
        name=node.node.name
        
        if name=="ASM":  # raw ASM
            s=node.args[0].value
            
            self.write("asm{%s}" % s)
            
            return
        
        if name=="NXC":
            s=node.args[0].value
            
            self.write("%s" % s)
            
            return
        
        if name=="DEFINE":
            s=node.args[1].value
            d=node.args[0].value

            self.write("#define %s %s" %(d,s))
            self.NEWLINE()
            self.semicolon=False
            return
        
        self.v(node.node)
        self.write("(")
        for i in range(len(node.args)):
            self.v(node.args[i])
            if i < (len(node.args) - 1):
                self.write(", ")
        if node.star_args:
            if len(node.args):
                self.write(", ")
            self.write("*")
            self.v(node.star_args)
        if node.dstar_args:
            if node.args or node.star_args:
                self.write(", ")
            self.write("**")
            self.v(node.dstar_args)
        self.write(")")

        if name in self.fv.types:
            self.erase_assign=True
        
        
    def visitClass(self, node):
        self.scope.append('class')

        self.flush()
        for i in range(len(node.bases)):
            self.v(node.bases[i])
        self.INDENT()
        self.v(node.code)
        self.DEDENT()
        
        self.buffer=[]  # get rid of all of the stuff in a class def
        self.scope.pop()
        
        
    def visitCompare(self, node):
        self.write("(")
        self.v(node.expr)
        
        for operator, operand in node.ops:
            self.write(" %s " % operator)
            self.v(operand)
        self.write(")")

    def visitConst(self, node):
        self.write(repr(node.value))

    def visitContinue(self, node):
        self.write("continue; ")

    def visitDiscard(self, node):
        self.semicolon=True

        # deal with empty statements, so it doesn't print None
        try:
            if node.expr.value is None:
                pass
            else:
                self.v(node.expr)
                if self.semicolon:
                    self.write(";")
                self.NEWLINE()
        except AttributeError:
            self.v(node.expr)
            if self.semicolon:
                self.write(";")
            self.NEWLINE()

    def visitDiv(self, node):
        self.v(node.left)
        self.write(" / ")
        self.v(node.right)


    def visitFor(self, node):
        
        
        children=node.list.getChildNodes()
        start='0'
        end='1'
        step='1'
        
        if self.debug:
            print node.assign.name
            print dir(node.assign)
            
            print node.list
            print dir(node.list)
    
            print node.list.getChildren()

            print children
            
        if children[0].name=='range':
            vals=[v.asList()[0] for v in children[1:]]
            if node.assign.name=='repeat':  # keyword repeat
                if len(vals)==1:
                    end=vals[0]
                else:
                    raise ValueError,"Bad for-loop construction"
                
                self.write("repeat(%s) " % (end))
                
            else:
                if len(vals)==1:
                    end=vals[0]
                elif len(vals)==2:
                    start=vals[0]
                    end=vals[1]
                elif len(vals)==3:
                    start=vals[0]
                    end=vals[1]
                    step=vals[2]
                else:
                    raise ValueError,"Bad for-loop construction"
                
                varname=node.assign.name
                self.write("for (%s=%s; %s<%s; %s+=%s) " % (varname,start,
                                                            varname,end,
                                                            varname,step))

            self.INDENT()
            self.v(node.body)
            self.DEDENT()
        else:
            raise ValueError,"For-loop construction not implemented"
            
        
        
        
    def visitGenExpr(self, node):
        self.write("(")
        self.v(node.code)
        self.write(")")

    def visitGetattr(self, node):
        self.v(node.expr)
        self.write(".%s" % node.attrname)

    def visitIf(self, node):
        flag=False
        for c, b in node.tests:
            if not flag:
                self.write("if (")
            else:
                self.write("else if (")
            self.v(c)
            self.write(') ')
            self.INDENT()
            self.v(b)
            self.DEDENT()
            flag=True
        if node.else_:
            self.write("else ")
            self.INDENT()
            self.v(node.else_)
            self.DEDENT()
            
    def visitKeyword(self, node):
        self.write(node.name)
        self.write("=")
        self.v(node.expr)


    def visitInvert(self, node):
        self.write("~")
        self.v(node.expr)

    def visitLeftShift(self, node):
        self.v(node.left)
        self.write(" << ")
        self.v(node.right)

    def visitMod(self, node):
        self.v(node.left)
        self.write(" % ")
        self.v(node.right)

    def visitMul(self, node):
        self.v(node.left)
        self.write(" * ")
        self.v(node.right)

    def visitName(self, node):
        
        if node.name=='False':
            self.write("false")
        elif node.name=='True':
            self.write("true")
        else:
            self.write(node.name.replace('inline_',''))

    def visitNot(self, node):
        self.write(" !(")
        self.v(node.expr)
        self.write(")")
        
    def visitOr(self, node):
        self.write("(")
        for i in range(len(node.nodes)):
            self.write("(")
            self.v(node.nodes[i])
            self.write(")")
            if i < len(node.nodes) - 1:
                self.write(" || ")
        self.write(")")

                
    def visitPass(self, node):
        self.write("// pass ")

    def visitReturn(self, node):
        try:
            if node.value.value is None:
                self.write('return;')
            else:
                self.write('return(%s);' % node.value.value.__repr__())
                
        except TypeError:
            pass
        except AttributeError:
                
            self.write("return(")
            self.v(node.value)
            self.write(");")

    def visitRightShift(self, node):
        self.v(node.left)
        self.write(" >> ")
        self.v(node.right)

    def visitSubscript(self, node):
        isdel = False
        if node.flags == OP_DELETE: isdel = True
        isdel and self.write("del ")
        self.v(node.expr)
        self.write("[")
        for i in range(len(node.subs)):
            self.v(node.subs[i])
            if i == len(node.subs) - 1:
                self.write("]")
        node.flags == OP_DELETE and self.NEWLINE()

    def visitSub(self, node):
        self.write("(")
        self.v(node.left)
        self.write(" - ")
        self.v(node.right)
        self.write(")")

    def visitUnaryAdd(self, node):
        self.write("+")
        self.v(node.expr)

    def visitUnarySub(self, node):
        self.write("-")
        self.v(node.expr)

    def visitWhile(self, node):
        self.write("while (")
        self.v(node.test)
        self.write(") ")
        self.INDENT()
        self.v(node.body)
        if node.else_:
            self.DEDENT()
            self.write("else:")
            self.INDENT()
            self.v(node.else_)
        self.DEDENT()
        
        
        
        
        
        
class FirstPassVisitor(ast_template.Visitor):
    """This object goes through and gets all of the variables.  
    The second pass will output the code"""
    
    def __init__(self,stream=sys.stdout,debug=False):

        ast_template.Visitor.__init__(self,stream,debug)
        self.variables={}

        self.return_datatype=None
        self.types=['Byte','Short','Word','String','Mutex','Integer','Long','Struct']
        self.struct_types={}
        self.functions={}
        self.functions['module']=Function('module',self.variables)
        
        self.variables_assign=[]
        self.kwassign=[]
        self.use_kwassign=False
        
        self.typedefs={}
        
        self.scope=['module']
        
        self.use_typedef=False
        
    def visitClass(self, node):
        self.scope.append('class')
        
        variables={}
        old_self_variables=self.variables
        self.variables=variables
        
        if self.debug:
            print "myvisitClass"
            print node.name
        
        basename=node.bases[0].name
        for i in range(len(node.bases)):
            self.v(node.bases[i])
            
            
        self.use_typedef=False
        self.v(node.code)

        if self.use_typedef:
            self.typedefs[node.name]=basename
            self.types.append(node.name)
        else:
            self.struct_types[node.name]=variables
            self.types.append(node.name)
            self.variables=old_self_variables
        self.scope.pop()
        
        
        
    def visitPass(self, node):
        if self.scope[-1]=='class':
            self.use_typedef=True
        
    def visitBlock(self, block):
        if self.debug:
            print "myvisitBlock"
        self.v(block)

    def visitAssName(self, node):
        if self.debug:
            print 'visitAssName'
            if node.flags == OP_DELETE:
                print "del ",
            print node.name
        
        n=node
        
        self.variables_assign.append(n.name)
        
        if n.name not in self.variables:
            self.variables[n.name]=Variable(n.name)
            if self.debug:
                print "MyAddVar",n.name
        
    def visitReturn(self, node):
        #self.write("return ")
        #self.v(node.value)
        try:
            if node.value.value is None:
                self.return_datatype='void'
            else:
                if isinstance(node.value.value,int):
                    self.return_datatype='int'
                else:
                    raise TypeError,"Unknown type for "+str(node.value.value)
                
        except TypeError:
            pass
        except AttributeError:  # a name?
            name=node.value.name
            if name in self.variables:
                self.return_datatype=self.variables[name].datatype
            else:
                raise NameError, "Name"+name+"not found"
            
    def visitFor(self, node):
        if self.debug:
            print 'myvisitFor'

        if node.assign.name!='repeat':  # keyword repeat
            self.v(node.assign)
            
        self.v(node.body)
        
        
    
    def visitAssign(self, node):
        if self.debug:
            print 'MyvisitAssign'
            
        self.variables_assign=[]
        for i in range(len(node.nodes)):
            n = node.nodes[i]
            if self.debug:
                print "  Node ",n
            self.v(n)
            
        if self.debug:
            print "varassign ",self.variables_assign
            a=node.expr.asList()[0]
            print "varassign expr",node.expr,node.expr.asList()[0],type(a)
        
        if self.scope[-1]=='module':
            if self.debug:
                print "Module Variables"
            for name in self.variables_assign:
                val=node.expr.asList()[0]
                self.variables[name].value=val
                if isinstance(val,str):
                    self.variables[name].datatype='String'
                if self.debug:
                    print "  ",self.variables[name]
                
                
        self.v(node.expr)

        
    def visitKeyword(self, node):
        if self.debug:
            print 'myvisitKeyword'

        if not self.use_kwassign:
            self.v(node.expr)
            return
        
        
        
    def visitCallFunc(self, node):
        if self.debug:
            print 'myvisitCallFunc'
            print 'funcname: ',node.node.name
            
        name=node.node.name
        
        
        if not name in self.types:
            self.v(node.node)
            for i in range(len(node.args)):
                self.v(node.args[i])

            return
            
        for v in self.variables_assign:
            if (name=='Byte' or name=='Word' or name=='Short' or 
                name=='String' or name=='Integer' or name=='Long' or
                name=='Mutex'):
                    
                self.variables[v].datatype=name
                try:
                    self.variables[v].value=node.args[0].value
                except IndexError:
                    self.variables[v].value=None # to fix the mutex problem
                    # was:  pass  # use the default value
                except AttributeError:  # list? or mutex
                    nodelist=node.args[0].asList()
                    vallist=[]
                    for l in nodelist:
                        vallist.append(l.value)
                    
                    self.variables[v].value=vallist
            elif name=='Struct':
                    
                
                self.use_kwassign=True

                
                struct_name=node.args[0].value
                
                if not struct_name in self.struct_types:
                    self.struct_types.append(struct_name)
                    
                    for i in range(1,len(node.args)):
                        if self.debug:
                            print node.args[i]
                            print dir(node.args[i])
                        fun=node.args[i].name
                        #self.v(node.args[i])
                        if self.debug:
                            print "  fun",fun
            elif name in self.types:
                self.variables[v].datatype=name
                try:
                    self.variables[v].value=node.args[0].value
                except IndexError:
                    pass  # use the default value
                except AttributeError:  # list?
                    self.variables[v].value=[]
                
            
    def visitFunction(self, node):
        self.scope.append('function')
        self.return_datatype=None
        
        variables={}
        old_self_variables=self.variables
        self.variables=variables
        
        if self.debug:
            print "myvisitFunction"
            print node.name
        hasvar = haskw = hasone = hasboth = False

        ndefaults = len(node.defaults)

        if node.flags & CO_VARARGS:
            hasone = hasvar = True
        if node.flags & CO_VARKEYWORDS:
            hasone = haskw = True
        hasboth = hasvar and haskw

        kwarg = None
        vararg = None
        defargs = []
        newargs = node.argnames[:]


        self.v(node.code)
                
        self.functions[node.name]=Function(node.name,variables)
        self.functions[node.name].datatype=self.return_datatype
        self.variables=old_self_variables
        self.scope.pop()
                    
        
        # remove those variables that are global
        remove_var=[]
        for var in self.functions[node.name].variables:
            if (var in self.variables and 
                self.functions[node.name].variables[var].datatype=='default'):
                
                remove_var.append(var)
                    
        for r in remove_var:
            self.functions[node.name].variables.pop(r)
        
 
def python_to_nxc(pyfile,nxcfile=None,debug=False):
    global file_lines
    
    filename = pyfile
    
    f = open(filename, 'U')
    codestring = f.read()
    f.close()
    if codestring and codestring[-1] != '\n':
        codestring = codestring + '\n'
        
    file_lines=open(filename).readlines()
    filestr=codestring
    
    
    defines=re.findall('\s*DEFINE (.*?)=(.*)',filestr)
    filestr=re.sub('\s*DEFINE (.*?)=(.*)',"",filestr)
    
    
    if debug:
        print "Filestr"
        print filestr
    
    ast = parse(filestr)
    v = FirstPassVisitor(debug=debug)
    v.v(ast)
    
    v.defines=defines
    
    if nxcfile:
        fid=open(nxcfile,'wt')
    else:
        fid=sys.stdout
        
    v2 = SecondPassVisitor(v,debug=debug,stream=fid)
    v2.v(ast)
    v2.flush()
    
    if not fid==sys.stdout:
        fid.close()
    
def readconfig(fname):
    config={'firmware':'105'}
    
    if os.path.exists(fname):
        data=yaml.load(open(fname))        
        config.update(data)
    
    return config
    
def main():

    config=readconfig('pynxc.yaml')
    nxc=os.path.join("nxc",sys.platform,'nbc')
    if not os.path.exists(nxc):
        nxc = 'nbc' # expect 'nbc' in the binary PATH

    usage="usage: %prog [options] [filename]"
    parser = OptionParser(usage=usage)

    parser.add_option('-c', '--compile', dest="compile",
                      help='compile to nxc code only',default=False,
                      action="store_true")
    parser.add_option('--debug', dest="debug",
                      help='show debug messages',default=False,
                      action="store_true")
    parser.add_option('--show_nxc', dest="show_nxc",
                      help='show the nxc code',default=False,
                      action="store_true")
    parser.add_option('-d', '--download', dest="download",
                      help='download program',default=False,
                      action="store_true")
    parser.add_option('-B', '--bluetooth', dest="bluetooth",
                    help='enable bluetooth',default=False,
                    action="store_true")
    parser.add_option('--firmware', dest="firmware",
                      help='firmware version (105, 107, or 128)',default=config['firmware'])
    parser.add_option('--command',  dest="nxc",
                      help='what is the nxc/nqc command',default=nxc,
                      metavar="<command>")
                      
                      
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        raise SystemExit
    
    options.firmware=config['firmware']

    # sanity check on the options
    
    if (options.download) and (options.compile):
        print "conflicting options"
        parser.print_help()
        raise SystemExit
        
    
    nxc_root,nxc=os.path.split(options.nxc)
    s=nxc.lower()

    filename = args[0]

    for filename in args:

        root,ext=os.path.splitext(filename)
        
        nxc_filename=root+".nxc"
        rxe_filename=root+".rxe"
        
        python_to_nxc(filename,nxc_filename,debug=options.debug)
        print "Wrote %s." % (nxc_filename)

        if options.show_nxc:
            fid=open(nxc_filename)
            print fid.read()
            fid.close()
            
        if not options.compile:
        
            cmd=options.nxc+" "
            if options.bluetooth:
                cmd+=' -BT '
                
            cmd=cmd+ "'%s'" % nxc_filename+ " -I='%s' -I=%s/ -v=%s -O='%s'" % (nxc_root,
                                                           pynxc_root,
                                                           options.firmware,
                                                           rxe_filename)
            print cmd
            a=os.system(cmd)
    
            if options.download:
                print "Downloading...",
                cmd=options.nxc+" "
                cmd=cmd+ nxc_filename+ " -I='%s/' -I='%s/' v=%s -d" % (nxc_root,
                                                          pynxc_root,
                                                          options.firmware)
                a=os.system(cmd)
                nxtcom=os.path.join(nxc_root,'nxtcom')
                print nxtcom
                if os.path.exists(nxtcom):
                    cmd='%s %s' % (nxtcom,rxe_filename)
                    a=os.system(cmd)

                print "done."
        
            
    return


class MainFrame(Frame):

    def Body(self):
        self.ReadConfig()
    
        self.nxc=os.path.join("nxc",sys.platform,'nbc')
        if not os.path.exists(self.nxc):
            nxc = 'nbc' # expect 'nbc' in the binary PATH

        self.prog=None

        self.CreateMenu()
        
        self.textbox = TextBox(self, multiline=1, readonly=1,
                       Font=Font("Courier New", 10), Size=(650,500),
                       Value='PyNXC Version '+str(__version__)+"\n" + 
                       "Firmware Version "+self.firmware_version+"\n")
        self.AddComponent(self.textbox, expand='both')

        self.Pack()
        self.CenterOnScreen()
        
        cmdlist=[self.nxc]
        self.DoCmd(cmdlist)
        
        self.ResetTitle()
        
    def ReadConfig(self):
    
        config=readconfig('pynxc.yaml')
        self.firmware_version=str(config['firmware'])
            
    def UpdateConfig(self):
    
        config={'firmware':self.firmware_version}
        with open("pynxc.yaml",'w') as fid:
            yaml.dump(config,fid,default_flow_style=False)
    
    def CreateMenu(self):
    
        
        menubar = MenuBar()
        
        menu1 = Menu(self)
        menu1.Append("L&oad Program File", self.Load, "Load a .py file",hotkey="Ctrl+O")
        menu1.Append("&Quit", self.Quit, "Quit",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        menu1 = Menu(self)
        menu1.Append("Con&vert", self.OnlyConvert)
        menu1.Append("&Compile", self.Compile,hotkey="Ctrl+C")
        menu1.Append("Compile and &Download", self.Download,hotkey="Ctrl+D")
        menubar.Append(menu1, "&Program")
        self.menubar=menubar

        self.nxt_menu = Menu(self)
        self.nxt_menu.Append("&Info", self.NXT_Info)
        self.bluetooth_menu=self.nxt_menu.Append("Enable &Bluetooth", type='check')
        
        submenu=Menu(self)
        self.firmware_menus=[
            submenu.Append("Version 105",type='radio',event=self.FirmwareVersion),
            submenu.Append("Version 107",type='radio',event=self.FirmwareVersion),
            submenu.Append("Version 128",type='radio',event=self.FirmwareVersion),
        ]
        if self.firmware_version=='107':
            self.firmware_menus[1].Check(True)
        elif self.firmware_version=='128':
            self.firmware_menus[2].Check(True)
        else:
            self.firmware_menus[0].Check(True)
            self.firmware_version='105'
            self.UpdateConfig()
            
        self.nxt_menu.AppendMenu("Firmware",submenu)
        
        self.menubar.Append(self.nxt_menu, "&NXT")
            
            
        self.SetMenuBar(menubar)

        
    def FirmwareVersion(self,event):
        versions={'Version 105':'105',
        'Version 107':'107',
        'Version 128':'128',
        }
    
        for menu in self.firmware_menus:
            if menu.IsChecked():
                self.firmware_version=versions[menu.Label]
                self.UpdateConfig()
                
        
        
    def Load(self,event=None):
        dlg = FileDialog(self, 'Select a Program File',default_dir=os.getcwd(),wildcard='*.py',open=1)
        try:
            result = dlg.ShowModal()
            if result == 'ok':
                self.prog = dlg.GetPaths()[0]
                self.ResetTitle()
        finally:
            dlg.Destroy()
    
    def ResetTitle(self,event=None):
        if self.prog:
            junk,fname=os.path.split(self.prog)
            s='PyNXC: %s' % fname
        else:
            s='PyNXC'
            
        self.SetTitle(s)
        
            
    def NXT_Info(self,event=None):
        pass
    
    def Quit(self,event=None):
        self.Close()

    def DoCmd(self,cmdlist):
        
        S=self.textbox.GetValue()
        S=S+"#-> "+" ".join(cmdlist)+"\n"
        self.textbox.SetValue(S)
        
        try:

            if sys.platform=='win32':
                output=subprocess.Popen(
                    cmdlist,stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            else:
                output=subprocess.Popen(
                    cmdlist,stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)

            try: # there might be non-ASCII chars in the output
                S += output.stdout.read() + output.stderr.read()
            except UnicodeDecodeError:
                S += (output.stdout.read() + output.stderr.read()
                     ).decode('utf-8', 'replace')
            
            self.textbox.SetValue(S)
                
        except OSError:
            
            s=sys.exc_info()
            S=S+"Error with NXC Executable: "+str(s[1])
            self.textbox.SetValue(S)
            return
                
                
            
    def Convert(self):
        filename=self.prog

#        path,fname=os.path.split(filename)
        root,ext=os.path.splitext(filename)
        
        nxc_filename=root+".nxc"
        
        S=self.textbox.GetValue()
        
        S=S+"Writing %s..." % (nxc_filename)
        self.textbox.SetValue(S)
        
        python_to_nxc(filename,nxc_filename)
        
        
        S=S+".done\n"
        self.textbox.SetValue(S)
        
        return nxc_filename

    
    def OnlyConvert(self,event=None):
        self.textbox.SetValue("")
        
        if not self.prog:
            self.Load()
            
        if not self.prog:
            dlg = MessageDialog(self, "Error","No Program File Selected")
            dlg.ShowModal()
            dlg.Destroy()
            return
            
        try:
            nxc_filename=self.Convert()
        except:
            s=sys.exc_info()
            str1="Error in "+self.prog +": "+str(s[1])
            self.textbox.SetValue(str1)
            return

    def Compile(self,event=None):
        self.textbox.SetValue("")
        
        if not self.prog:
            self.Load()
            
        if not self.prog:
            dlg = MessageDialog(self, "Error","No Program File Selected")
            dlg.ShowModal()
            dlg.Destroy()
            return
            
        try:
            nxc_filename=self.Convert()
        except:
            s=sys.exc_info()
            str1="Error in "+self.prog +": "+str(s[1])
            self.textbox.SetValue(str1)
            return


        root,ext=os.path.splitext(nxc_filename)
        rxe_filename=root+".rxe"
        
        
        
        cmdlist=[self.nxc,nxc_filename," -v=%s" % self.firmware_version," -O=%s" % rxe_filename]
        
        self.DoCmd(cmdlist)
            

   
    def Download(self,event=None):
        
        self.textbox.SetValue("")
        
        if not self.prog:
            self.Load()
            
        if not self.prog:
            dlg = MessageDialog(self, "Error","No Program File Selected")
            dlg.ShowModal()
            dlg.Destroy()
            return
            
        try:
            nxc_filename=self.Convert()
        except:
            s=sys.exc_info()
            str1="Error in "+self.prog +": "+str(s[1])
            self.textbox.SetValue(str1)
            return

        flags=['-d','-S=usb','-v=%s' % self.firmware_version]
        if self.bluetooth_menu.IsChecked():
            flags.append('-BT')
            
        root,ext=os.path.splitext(nxc_filename)
        rxe_filename=root+".rxe"
        cmdlist=[self.nxc]
        cmdlist.extend(flags)
        cmdlist.append(nxc_filename)
        
        self.DoCmd(cmdlist)

        root,ext=os.path.split(self.nxc)
        nxtcom=os.path.join(root,'nxtcom_scripts/nxtcom')
        print nxtcom
        if os.path.exists(nxtcom):
            print "Downloading...",
            cmd='%s %s' % (nxtcom,rxe_filename)
            a=os.system(cmd)
            print "done."
        
        
if __name__ == "__main__":

    
    if len(sys.argv)<2:  # no args given, launch gui
        app = Application(MainFrame, title="PyNXC")
        app.Run()
    else:
        sys.exit(main())
    
