#import ply.lex as lex
import parser
import sys
import re
import copy
from collections import deque
from pprint import pprint as pp
import sys

#from enum import Enum

class Type():  # This could also be done with individual classes
    leftparentheses = 0
    rightparentheses = 1
    operator = 2
    empty = 3
    operand = 4

OPERATORS = {  # get your data out of your code...
    "=": "=>",
    "|": "or",
    "&": "and",
    "~": "not",
    #"/": "divide",
}

def textOperator(string):
    if string not in OPERATORS:
        sys.exit("Unknown operator: " + string)
    return OPERATORS[string]

def typeof(string):
    if string == '(':
        return Type.leftparentheses
    elif string == ')':
        return Type.rightparentheses
    elif string in OPERATORS:
        #print string,'str'
        return Type.operator
    elif string == ' ':
        return Type.empty
    else:
        return Type.operand

def process(tokens):

    stack = []
    lower=[]
    tok=[]
    #print tokens,'tokens'
    while tokens:
       # print tokens,'TOKENS$$'
        token = tokens.pop()
        #print token,'token initia'
        tok.append(token)
        #print tok,'token initia'
        category = typeof(token)
        #print 'category:',category
        #print("token = ", token, " (" + str(category) + ")")

        if category == Type.operand:
            #print token,'operand'
            stack.append(token)
            #print stack,'stack'
        elif category == Type.operator:
            #print category,'***',token,'***',stack
            stack.append((textOperator(token), stack.pop(), process(tokens)))
        elif category == Type.leftparentheses:
            #print token,'('
            stack.append(process(tokens))
        elif category == Type.rightparentheses:
            #print token,')'
            return stack.pop()
        elif category == Type.empty:
            continue

        #print("stack = ", stack)
       
    return stack.pop()

##INFIX = "((B&C)=>A)"

# pop/append work from right, so reverse, and require a real list
#postfix = process(list(INFIX[::-1]))

#print(postfix)

f=open('input14.txt','r')
nq=int(f.readline())
is_a = isinstance
queries=[]
qs=''
for i in range(nq):
    qs=f.readline().strip()
    queries.append(qs)
##print queries
nk=int(f.readline())
total=nq+nk
kb=[]
s=''
for i in range(nq+1,total+1):
    s=f.readline().strip()
    kb.append(s)
##print kb,'kb'
def priority(c):
    if c=='~':
        return 1
    elif c=='&':
        return 2
    elif c=='|':
        return 3
    elif c=='=>':
        return 4
def getop(c):
    op=[]
    if '=>' in c:
        op.append('=>')
    if '=' in c:
        op.append('=')
##    if '~' in c:
##        op.append('~')
    if '|' in c:
        op.append('|')
    if '&' in c:
        op.append('&')
    #print op
    return op

d=[]
e=[]
o=[]
p=[]
op=["|","&","~","=>","="]
c=[]

def predicate(cl):
    predicate=[]
    #g=''
    pred=[]
    x=[]
    for i in range(len(cl)):
        if cl[i].isupper():
            x.append(cl[i:].split('(')[0])
    for i in range(len(x)):
        if ',' not in x[i] and ')' not in x[i]:
            pred.append(x[i])

    return pred

def getvariable(cl):
    variable=[]
    for i in range(len(cl)):
        if cl[i].islower() and (cl[i-1]=='(' or cl[i-1]==','):
            variable.append(cl[i])
    return variable

def constants(cl):
    const=[]
    j=0
    d=''
    x=[]
    c=[]
    p=predicate(cl)
   # print x,'xxxx'
    #x=[]
    for i in range(len(cl)):
        if cl[i].isupper():
            j=i
            x.append(cl[i:].split('(')[0])
    #print x,'xxxxxxxxxxxxxx'
    for i in range(len(x)):
        if x[i] not in p:
            c.append(x[i].replace(')',''))
    #print c,'const'
    if c !=[]:
        o=c[0]
        t=o.split(',')
        for i in range(len(t)):
       # if ','  in x[i] or '('  in x[i]:
           # p=x[i].split(',')
            const.append(t[i])
    
       

    return const
def tsplit(string, delimiters):
    """Behaves str.split but supports multiple delimiters."""
    
    delimiters = tuple(delimiters)
    stack = [string,]
    
    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i+j, _substring)
            
    return stack

def build(cl):
    c=cl.replace('(',' ')
    d=c.replace(')','')
    u=predicate(cl)
    #p={}
    y=tsplit(d,getop(cl))
    p={u[i]:[] for i in range(len(u))}

    #print y
    for i in range(len(y)):
        if u[i] in y[i]:
            #print i,'iiii'
            p[u[i]].append(y[i].replace(',',' '))
    return p
def con(u,p):
    s={}
    #print u,'pred'
    s={u[i]:[] for i in range(len(u))}
    for i in range(len(u)):
       # for j in range(len(p[u[i]])):
        s[u[i]]=p[u[i]]
    return s
def getterm(cl):
    s=cl
    term=''
    t=[]
    u=predicate(cl)
    f=getop(cl)
    if f==[]:
        t.append(s)
    for i in range(len(s)):
        if s[i] in u and f!=[]:
            j=i
            while s[j]!= ')':
                term=term+(s[j])
                j+=1
            t.append(term+')')
            term=''
    return t

def get(cl):
    s=cl
    t=[]
    term=''
    u=predicate(cl)
    #print u,'predicate'
    f=getop(cl)
    if f==[]:
        t.append(s)
        return t
    j=0
    y=0
    i=0
    while i < len(s)-1 :
 
        term=term+u[j]
##        print term,'term'
        q=s.find(term)
##        print q,'pos'
        j+=1
##        print j,'jjj'
        y=q+len(term)
        #print y,'len'
        while s[y]!=')':
            term=term+s[y]
##            print term,'inside'
            y+=1
        t.append(term+')')
        s=s.replace(term+')',(len(term)+1)*'*')

        i=s.find('*')+1
        #if s[i]!=')':
        i=y+1
        if i<len(s)-1:
            while s[i]==')' and i<len(s)-1:
                i+=1
            
            
            #print i,'iyiy'
        term=''
        #print term,'ttt'
    return t
    
def convert(cl):
##    print cl,'cll'
    c=cl
    #print type(c)
    v=[]
    x=predicate(cl)
    w=get(cl)

    j=0
    for i in range(len(w)):

        c=(c.replace(w[i],x[i]))
        #v.append(c)
    i=0
    c=c.replace(' ','')

    while i<(len(c)):
       # print len(c),'length'
        if c[i].isupper():
            y=len(x[j])
##            print y,'yyy',i
            j+=1

            v.append(c[i:i+y])
            i=i+y
##            print v,'****',i
        elif c[i]=='(' or c[i]==')' or c[i]==',' or c[i]==' ' or c[i]=='|' or c[i]=='&' or c[i]=='=' or c[i]=='~':
            v.append(c[i])
            i+=1
            

    return v
def getnegate(cl):
    i=0
    j=0
    t=''
    if '~' not in cl:
        return cl
    elif '~' in cl:
        while i < len(cl):
            if cl[i] =='~' and cl[i-1]=='(':
                j=i+1
                #print i,'((())',j
                while cl[j]!=')' or cl[j-1]!=')':
                    t=t+cl[j]
                    j+=1
                i=i+j+1
            else: i=i+1
        return t
def pred(s):
    e=[]
    for i in range(len(s)):
        if s[i].isupper():
            j=i
            while s[j]!="'":
                j+=1
            e.append(s[i:j])
    return e
    
                
def replicate(st,di,q):
    e=(st)
##    print e
    e="'"+e+"'"
    p=0
    g=copy.deepcopy(di)
    u=pred(st)
    i=0
    st=st.replace('( ','')
    while i<(len(st)):
        #print t[i]
        if st[i].isupper() and st[i:i+len(u[p])] in u :
            e=e.replace("'"+st[i:i+len(u[p])]+"'",'('+g[q][st[i:i+len(u[p])]][0]+')',1)

##            print e,'eeeeeeeee'
            del g[q][st[i:i+len(u[p])]][0]
            #print o,'ooooooo'
            i=i+len(u[p])
            #print i
            p+=1
        else: i+=1
    #x=e.replace("'",'').replace(',','').replace('( ','(')
    return e
                
        
def require(cl,t,q):
    e=(t)
##    print e
    e="'"+e+"'"
    p=0
    g=copy.deepcopy(di)
    u=predicate(cl)
    i=0
    t=t.replace('( ','')
    while i<(len(t)):
        #print t[i]
        if t[i].isupper() and t[i:i+len(u[p])] in u :
            e=e.replace("'"+t[i:i+len(u[p])]+"'",'('+g[q][t[i:i+len(u[p])]][0]+')',1)

            del g[q][t[i:i+len(u[p])]][0]
            #print o,'ooooooo'
            i=i+len(u[p])
            #print i
            p+=1
        else: i+=1
    i=0
    u=0
    e=e.replace("'",'')
    e="'"+str(e)+"'"
    k=e

    if '~' in e:
                c=getnegate(cl)

                for i in range(len(e)):
                    if e[i]=='~':
                       
                        r=(convert(c.replace("=>","=").replace("~","")))
                        r.reverse()
                        st=process(r)
                        st=str(st)
                        #######st=replicate(st,di,q)
                        st="'"+st+"'"

                        up=pred(st)
##                        print up,'preds'
                        for i in range(len(up)):
##                            print up[i],'upupup',di[q][up[i]][0]
                            st=st.replace(up[i],'('+di[q][up[i]][0]+')')
                            st.replace('~','')
                        st=st.replace("'","")
                        
                        
##                        u=i+1
                        if st in e:

                            st=st.replace("~","")
                            k=k.replace('~','')
                            k=k.replace(st,'('+'not'+st+')')
                            
##                        i=u+1
                
##        else:
##            e=e
##                
    x=k.replace("'",'').replace(',','').replace('( ','(')
                 
    return x
    
di=[]  

for i in range(len(kb)):
    di.append(con(predicate(kb[i]),build(kb[i].replace(' ',''))))
##    print "cotncate ",con(predicate(kb[i]),build(kb[i].replace(' ','')))
que=[]
##print '********************QUERIES***************************************************'
for i in range(len(queries)):
    que.append(con(predicate(queries[i]),build(queries[i].replace(' ',''))))
##    print "cotncate ",con(predicate(queries[i]),build(queries[i].replace(' ','')))



inf=[]
#infix=[]
for i in range(len(kb)):
    #infix=deque()
    x=kb[i]
    #z=predicate(kb[i])
    infix=(convert(kb[i].replace("=>","=").replace("~","")))
    infix.reverse()
##    print infix,'infix acrual'
    #print (infix[::-1]),'infix'
    rii=(process(((infix))))
    o=str(rii)
##    print o.replace("'",'')
    inf.append(o)


t=()
##print '********************************************************************************'
for i in range(len(inf)):

    t=t+(require(kb[i],str(inf[i]),i),)
##    print "Final ",require(kb[i],str(inf[i]),i)

qt=()
##print '*************************************************************************'
for i in range(len(que)):
    qt=qt+(que[i][predicate(queries[i])[0]][0],)
        
        
is_a = isinstance

class lisp_reader:

    def __init__ (self, file):
        self.file = file
        self.char = None
        self.line = 1

    def peek (self):
        if self.char is None:
            self.char = self.file.read (1)
        return self.char

    def next (self):
        result, self.char = self.char, self.file.read (1)
        if result == '\n':
            self.line += 1
        return result

    def skip_whitespace (self):
        while 1:
            ch = self.peek()
            if not ch:
                break
            elif ch not in ' \t\r\n':
                if ch == ';':
                    while self.next() not in '\r\n':
                        pass
                else:
                    break
            else:
                self.next()

    def read (self):
        self.skip_whitespace()
        ch = self.peek()
        if ch == '':
            raise EOFError, "Unexpected end of file"
        elif ch == '(':
            return self.read_list()
        elif ch in '0123456789':
            a = self.read_atom()
            all_digits = 1
            for ch in a:
                if ch not in '0123456789':
                    all_digits = 0
                    break
            if all_digits:
                return int (a)
            else:
                return a
        else:
            return self.read_atom()

    def read_atom (self):
        # read at least one character
        line = self.line
        result = self.next()
        while 1:
            ch = self.peek()
            if ch in ' \t\r\n' or ch in '()':
                return result
            else:
                result = result + self.next()

    def read_list (self):
        result = []
        # throw away the paren
        paren = self.next()
        while 1:
            self.skip_whitespace()
            p = self.peek()
            if p == ')':
                # throw away the paren
                ch = self.next()
                return tuple (result)
            else:
                exp = self.read()
                result.append (exp)

def read_string (s):
    import cStringIO
    r = lisp_reader (cStringIO.StringIO (s))
    return r.read()

def map_args (op, fun, exp):
    return (op,) + tuple ([fun(x) for x in exp[1:]])

def negate (e):
    #print e,'negate e'
    if e[0]=='not':
        return e[1]
    return ('not', e)

class counter:
    def __init__ (self, init=0):
        self.val = init
    def next (self):
        result, self.val = self.val, self.val + 1
        return result

class UnboundVariableError (Exception):
    pass

# I think we want these globally unique
alpha_counter = counter()
skolem_counter = counter()

def to_cnf (e):
    print e

    def unimply (e):
        if is_a (e, tuple):
            op = e[0]
            if op == '=>':
                #print e,'unimply e'
                _, ant, con = e
                return ('or', unimply (('not', ant)), unimply (con))
            
            else:
                return map_args (op, unimply, e)
        else:
            return e

    def move_not_inward (e):
        if is_a (e, tuple):
            op = e[0]
            if op == 'not':
                _, e = e
                if is_a (e, tuple):
                    op = e[0]
                    if op == 'not':
                        _, e = e
                        #print e,'eeeeeeeeeeeeeeee'
                        return move_not_inward (e)
                    elif op == 'or':
                        _, a, b = e
                        return ('and', move_not_inward (('not', a)), move_not_inward (('not', b)))
                    elif op == 'and':
                        _, a, b = e
                        return ('or', move_not_inward (('not', a)), move_not_inward (('not', b)))
                    else:
                        # XXX ground term - we need to verify no more ops below here!
                        return ('not', map_args (op, move_not_inward, e))
                else:
                    return ('not', e)
            else:
                return map_args (op, move_not_inward, e)
        else:
            return e

    def lookup (name, lenv):
        while lenv is not None:
            (var, val), lenv = lenv
            if name == var:
                return val
        raise UnboundVariableError (name)

    def standardize_apart (e, lenv=None):
        # alpha renaming
        if is_a (e, tuple):
            op = e[0]
           
            return map_args (op, lambda x: standardize_apart (x, lenv), e)
        elif is_a (e, str) and e[0] == e[0].lower():
            # symbols starting with lower-case letter are variables
            # XXX think about doing this in the parser and making a class for vars
            return lookup (e, lenv)
        else:
            return e

   

    def distribute_and_over_or (e):
        def F (e):
            # let's try it simply first
            if is_op (e, 'or'):
                _, e0, e1 = e
                e0, e1 = F(e0), F(e1)
                if is_op (e0, 'and'):
                    # ((f0 & f1) | e1) => (f0|e1) & (f1|e1)
                    _, f0, f1 = e0
                    return ('and', F (('or', f0, e1)), F (('or', f1, e1)))
                elif is_op (e1, 'and'):
                    # (e0 | (f0 & f1)) => (f0|e0) & (f1|e0)
                    _, f0, f1 = e1
                    return ('and', F (('or', f0, e0)), F (('or', f1, e0)))
                else:
                    return ('or', e0, e1)
            elif is_a (e, tuple):
                return map_args (e[0], F, e)
            else:
                return e
        return F (e)

    def flatten (e):
        if is_a (e, tuple):
            if e[0] in ('and', 'or'):
                op, e0, e1 = e
                e0, e1 = flatten (e0), flatten (e1)
                if is_op (e0, op):
                    r = e0[1:]
                else:
                    r = (e0,)
                if is_op (e1, op):
                    r += e1[1:]
                else:
                    r += (e1,)
                return (op,) + r
            else:
                return map_args (e[0], flatten, e)
        else:
            return e

    e = unimply (e)
    e = move_not_inward (e)
    # this is done in the solver
    #e = standardize_apart (e)
    e = distribute_and_over_or (e)
    e = flatten (e)

    return e

def is_op (e, op):
    return is_a (e, tuple) and e[0] == op

def parse (s):
    return read_string (s)

def unparse (e):
    if is_a (e, tuple):
        return ('(%s ' % e[0]) + ' '.join ([unparse(x) for x in e[1:]]) + ')'
    else:
        return '%s' % (e,)

def simplify (e):
    # 1) make and & or binary operators
    # 2) make quantifiers bind only one variable
    if is_a (e, tuple):
        op = e[0]
        if op in ('and', 'or'):
            if len (e) > 3:
                return (op, e[1], simplify ((op,) + e[2:]))
            else:
                return e
        else:
            return map_args (op, simplify, e)
    else:
        return e

def infix (e):
    if is_a (e, set):
        # special case to handle disjunct_sets
        return infix (('or',) + tuple (e))
    elif is_a (e, tuple):
        op = e[0]
        if op in ('and', 'or'):
            op = ' %s ' % ({'and':'&','or':'|'}[op],)
            return '(' + op.join ([infix (x) for x in e[1:]]) + ')'
        elif op == 'not':
            return '~%s' % (infix (e[1]),)
        else:
            return '%s(%s)' % (op, ', '.join ([infix(x) for x in e[1:]]))
    else:
        return '%s' % (e,)

def conjuncts (e):
    if is_op (e, 'and'):
        return e[1:]
    else:
        return [e]

def disjuncts (e):
    if is_op (e, 'or'):
        return e[1:]
    else:
        return [e]

def disjunct_set (e):
    if is_op (e, 'or'):
        return set (e[1:])
    else:
        return set ([e])

def size (x):
    if is_a (x, tuple):
        r = 0
        for y in x:
            r += size (y)
        return r
    else:
        return 1

class clause:
    def __init__ (self, lits):
        self.lits = set(lits)
        self.predicates = {}
        for lit in lits:
            pred = get_predicate (lit)
            if self.predicates.has_key (pred):
                self.predicates[pred].append (lit)
            else:
                self.predicates[pred] = [lit]
        self.size = self.compute_size()

    def __len__ (self):
        return len (self.lits)

    def compute_size (self):
        r = 0
        for l in self.lits:
            r += size (l)
        return r

    def __cmp__ (self, other):
        assert (is_a (other, clause))
        #diff = self.lits.symmetric_difference (other.lits)
        if self.lits == other.lits:
            return 0
        else:
            return -1

    def find_complements (self, other):
        # return all possible pairs of complements
        assert (is_a (other, clause))
        pla = self.predicates
        plb = other.predicates
        if len(pla) > len (plb):
            pla, plb = plb, pla
        r = []
        used = set()
        for key in pla.iterkeys():
            if plb.has_key (key):
                for lita in pla[key]:
                    for litb in plb[key]:
                        if is_not (lita) != is_not (litb):
                            if lita not in used and litb not in used:
                                r.append ((lita, litb))
                                used.add (lita)
                                used.add (litb)
        #print r,'find complement r'
        return r

    def resolve (self, other):
        complements = self.find_complements (other)
        #print complements,'complements'
        complements.reverse()
        for i in range(len(complements)):
            # second, try to unify each of the pairs
            #print len(complements),'len'
            eliminated = set()
            for x0, y0 in complements:
                if is_not (x0):
                    x1, y1 = x0[1], y0
                else:
                    x1, y1 = x0, y0[1]
                try:
                    # XXX fixme - don't pass subst down
                    subst = {}
                    unify (x1, y1, subst)
                except UnifyError:
                    pass
                else:
                    #while subst:
                    #print 'eliminated', infix(x0), infix(y0)
                    eliminated.add (x0)
                    #print 'x0',eliminated,'x00',x0
                    eliminated.add (y0)
                    #print 'y0',eliminated#,'clause',clause(eliminated)
            if len (eliminated):
                #print len(eliminated),'len',subst,'sub'
                return subst, clause (self.lits.union (other.lits) - eliminated)
            else:
                return False
        else:
            return False

    def apply_subst (self, subst):
        return clause (set ([apply_subst (x, subst) for x in self.lits]))

    def standardize_apart (self, suffix):
        map = {}
        def F (e):
            if is_a (e, tuple):
                return map_args (e[0], F, e)
            elif is_var (e):
                if map.has_key (e):
                    return map[e]
                else:
                    map[e] = add_suffix (e, suffix)
                    return map[e]
            else:
                return e
        return clause (set ([F(x) for x in self.lits]))

    def __repr__ (self):
        return infix (('or',) + tuple (self.lits))

def add_suffix (var, suffix):
    # add a suffix, replacing one if it's already there
    p = var.rfind ('_')
    if p == -1:
        return '%s_%s' % (var, suffix)
    else:
        return '%s_%s' % (var[:p], suffix)

class knowledge_base:

    def __init__ (self):
        self.clauses = []

    def tell (self, s):
        # store the clauses as sets of literals
        for c in conjuncts (to_cnf (simplify (parse (s)))):
            #print c,'ccc'
            self.clauses.append (clause (disjunct_set (c)))

    def dump (self):
        print 'KB {'
        for c in self.clauses:
            print '  %s,' % (infix (c),)
        print '}'

def is_var (e):
    return is_a (e, str) and len(e) and e[0] == e[0].lower()

def is_const (e):
    return is_a (e, str) and len(e) and e[0] == e[0].upper()

def is_predicate (e):
    return is_a (e, tuple) and is_const (e[0])

# base types that allow simple comparison.
# [we want to avoid using 'x == y', which will do deep comparisons]
simple = (int, str)

class UnifyError (Exception):
    pass

def unify (x, y, subst):
    if is_a (x, int) and is_a (y, int) and x == y:
        return subst
    elif is_const (x) and is_const (y) and x == y:
        return subst
    elif is_var (x):
        return unify_var (x, y, subst)
    elif is_var (y):
        return unify_var (y, x, subst)
    elif is_predicate (x) and is_predicate (y):
        if x[0] != y[0]:
            raise UnifyError (x, y, subst)
        else:
            return unify_sequence (x[1:], y[1:], subst)
    elif is_a (x, list) and is_a (y, list):
        return unify_sequence (x, y)
    else:
        raise UnifyError (x, y, subst)

def unify_var (v, x, subst):
    if subst.has_key (v):
        return unify (subst[v], x, subst)
    else:
        occurs_check (v, x)
        subst[v] = x
        return subst

def unify_sequence (x, y, subst):
    if len(x) != len(y):
        raise UnifyError (x, y, subst)
    else:
        for i in range (len (x)):
            subst = unify (x[i], y[i], subst)
        return subst

def occurs_check (v, x):
    if is_var (x):
        if v == x:
            raise UnifyError (v, x, "occurs check")
    elif is_a (x, tuple):
        for y in x[1:]:
            occurs_check (v, y)
    else:
        pass

def apply_subst (x, subst):
    if is_var (x):
        while subst.has_key (x):
            x = subst[x]
        return x
    elif is_a (x, tuple):
        return (x[0],) + tuple ([apply_subst(y, subst) for y in x[1:]])
    else:
        return x

def flatten_subst (substs):
    if substs is not None:
        subst, substs = substs

def U (x, y, subst):
    print '    unify', infix(x), infix(y)
    r = unify (x, y, subst)
    print '    =>', r
    return r

def is_not (e):
    return is_a (e, tuple) and e[0] == 'not'

def get_predicate (e):
    #print e,'predicate'
    #print (is_a (e, tuple))
    assert (is_a (e, tuple))
    if e[0] == 'not':
        e = e[1]
    assert is_a (e, tuple)
    #print e[0][0]
    assert (e[0][0] == e[0][0].upper())
    return e[0]

def get_variables (e):
    return ()

class Solved (Exception):
    pass

def print_answer (vars, vals):
    if vars:
        print 'answer:'
        for i in range (len (vars)):
            print '%s=%s' % (vars[i], infix (vals[i]))
        raw_input()
    else:
        raise Solved

# --- resolution ---
arr=[]
def linear_resolution (kb, question, success=print_answer, randomize=False, negate_query=True):
    clauses = kb.clauses
    # negate the goal
    question = parse (question)
    # pull out any variables the user is looking for
    vars = get_variables (question)
    goals = conjuncts (to_cnf (simplify (question)))
    # XXX until I understand how to handle it...
    assert (len (goals) == 1)
    if negate_query:
        goal = clause ([negate (goals[0])])
    else:
        goal = clause (disjunct_set (goals[0]))
##    print 'goal:', goal
    
    def search (clauses, goal, substs, depth=0):

        def I (s):
            pass
            #print '%s%s' % (depth * '  ', s)

        I ('search: [%d] %r' % (goal.size, goal,))
        if randomize:
            import random
            random.shuffle (clauses)
        else:
            # sort by size (i.e., unit preference)
            clauses.sort (lambda a,b: cmp (a.size, b.size))
            
        for c in clauses:
            I ('  trying: %r  %r' % (goal, c))
            # I don't like this, but it seems to be the only
            #   way to get a composable substitution.  Maybe
            #   I can build it into resolve()?
            c = c.standardize_apart (str (depth+1))
            probe = c.resolve (goal) # goal.resolve (c)
            if probe is not False:
                subst, resolvent = probe
                I ('  resolvent: %r' % (resolvent,))
                # did we get the empty clause?
                if len(resolvent) == 0:
                    # return the solution
                    I (' * subst : %r' % (subst,))
                    success (vars, [apply_subst (x, subst) for x in vars])
                else:
                    # apply <subst> to the resolvent
                    if subst:
                        I (' * subst : %r' % (subst,))
                        I (' * before: %r' % (resolvent,))
                        resolvent = resolvent.apply_subst (subst)
                        I (' * after : %r' % (resolvent,))
                        if resolvent in clauses:
                            # a loop, get out
                            I ('LOOP, BACKTRACKING...')
                            continue
                    # make the resolvent the new goal
                    # add the previous resolvent to the set of clauses (makes this 'linear resolution')
                    # THIS IS THE ONE I REMOVED: raw_input()
                    search (clauses + [goal], resolvent, (subst, substs), depth+1)
                    # do *not* add it (makes this 'input resolution')
                    #search (clauses, resolvent, (subst, substs), depth+1)
                    I ('BACKTRACKING...')

    try:
        search (clauses, goal, None)
        #print 'YES'
    except Solved:
        #f.write('TRUE')
        arr.append('TRUE')
        print 'TRUE'
        pass
    else:
        arr.append('FALSE')
        #f.write('FALSE')
        print 'FALSE'
        

class horn_knowledge_base:

    def __init__ (self):
        self.rules = {}

    def tell (self, s):
        for c in conjuncts (to_cnf (simplify (parse (s)))):
            lits = disjuncts (c)
            #print lits
            body = []
            head = None
            for lit in lits:
                if is_not (lit):
                    body.append (lit[1])
                elif head is not None:
                    raise ValueError ("non-Horn clause: %r" % (s,))
                else:
                    head = lit
            head_pred = get_predicate (head)
            # store each rule as follows:
            # rules[PRED] = [[head0, body0_0, body0_1, ...], [head1, body1_0, body_1_1, ...]]
            if self.rules.has_key (head_pred):
                self.rules[head_pred].append ([head] + body)
            else:
                self.rules[head_pred] = [[head] + body]

    def dump (self):
        print 'HornKB {'
        for pred in self.rules.keys():
            for rule in self.rules[pred]:
                head, body = rule[0], rule[1:]
                if len(body):
                    print '  %s :- %s.' % (infix(head), ', '.join ([infix(x) for x in body]))
                else:
                    print '  %s.' % (infix(head),)
        print '}'

    def apply_subst (self, exp, subst):
        def F (exp):
            if is_var (exp) and subst.has_key (exp):
                return F (subst[exp])
            elif is_a (exp, tuple):
                return map_args (exp[0], F, exp)
            else:
                return exp
        return F (exp)

    def standardize_apart (self, e, suffix):
        def F (e):
            if is_a (e, tuple):
                return map_args (e[0], F, e)
            elif is_var (e):
                return add_suffix (e, suffix)
            else:
                return e
        return F (e)

    def sld_resolution (self, query, success=print_answer):
        # negate the goal
        query = parse (query)
        #print 'query=', infix(query)
        # pull out any variables the user is looking for
        vars = get_variables (query)
        goals = conjuncts (to_cnf (simplify (query)))
        #print goals,'goooaaals'
        
        def search (goals, vals, depth):
            goal = goals[0]
            goal_pred = get_predicate (goal)
            #print '%sgoal:%s' % ('  ' * depth, infix (goal))
            #print goal_pred,'goal'
            for rule in self.rules[goal_pred]:
                # can we unify this head with our goal?
                subst = {}
                #print '%stry %s :- %s' % ('  ' * depth, infix(head), ', '.join ([infix(x) for x in body]))
                rule = [self.standardize_apart (x, str(depth)) for x in rule]
                head = rule[0]
                body = rule[1:]
                try:
                    unify (head, goal, subst)
                except UnifyError:
                    pass
                else:
                    goals = body + goals[1:]
                    #print '%s[%d] goals: %s' % ('  ' * depth, len(goals), [infix(x) for x in goals])
                    #print '%ssubst:%r' % ('  ' * depth, subst)
                    if len(goals) == 0:
                        success (vars, [self.apply_subst (v, subst) for v in vals])
                    else:
                        search (
                            [self.apply_subst (x, subst) for x in goals],
                            [self.apply_subst (v, subst) for v in vals],
                            depth + 1
                            )
        try:
            search (goals, vars, 0)
        except Solved:
            arr.append("TRUE")
            print 'YES'
        else:
            arr.append("FALSE")
            print 'NO'

    def ask (self, query):
        self.sld_resolution (query)   
            
def test():
    c=0
    for i in range(len(t)):
        #print t,'ttt'
##        kbase.tell(t[i])
        if '=>' in t[i]:
            c+=1
   # kbase.dump()
    if c>=1:
        kbase = knowledge_base()
        for i in range(len(t)):
        #print t,'ttt'
            kbase.tell(t[i])
        for i in range(len(qt)):
            b=qt[i]
            b=str(b)
            if '~' in qt[i]:
                b=b.replace('~','')
                b='('+'not'+'('+b+')'+')'
            else:
                b='('+b+')'
            linear_resolution(kbase,b)
    elif c==0:
        kbase=horn_knowledge_base()
        for i in range(len(t)):
        #print t,'ttt'
            kbase.tell(t[i])        
        for i in range(len(qt)):
            b=qt[i]
            b=str(b)
            if '~' in qt[i]:
                b=b.replace('~','')
                b='('+'not'+'('+b+')'+')'
            else:
                b='('+b+')'
            kbase.sld_resolution(b)
 

if __name__ == '__main__':
    out=open('output.txt','w')
    test()
    for i in range(len(arr)):
        out.write(arr[i])
        out.write('\n')
    out.close()

