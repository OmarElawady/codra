from .parser import parser
from .symboltable import SymbolTable
from functools import reduce

def strip(string):
    if len(string) and string[0] == '\n':
        string = string[1:]
    if len(string) and string[-1] == '\n':
        string = string[:-1]
    return string

class Annotator:
    def evaluate(self, node, symbol_table):
        self.symbol_table = symbol_table
        self.annotate(node)
    
    def annotate(self, node):
        try:
            getattr(self, node.get_name().replace('-', '_'))(node)
        except Exception as e:
            print("Error at line " + str(node.get_line()) + ": " + str(e))

    def annotate_children(self, node):
        chs = node.get_children()
        for ch in chs:
            self.annotate(ch)
    
    def combine_children(self, node):
        return reduce(lambda x, y: x + y, list(map(lambda x: str(x.get_value()), node.get_children())), '')
    
    def program_data(self, node):
        self.annotate_children(node)
        node.set_value(self.combine_children(node))

    def program_construct(self, node):
        self.annotate_children(node)
        node.set_value(self.combine_children(node))

    def program_empty(self, node):
        node.set_value('')
    
    def construct_expression(self, node):
        self.annotate_children(node)
        node.set_value(self.combine_children(node))

    def construct_if(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        if chs[0].get_value():
            node.set_value(chs[1].get_value())
        else:
            node.set_value('')

    def construct_for(self, node):
        chs = node.get_children()
        self.annotate(chs[0])
        self.annotate(chs[1])
        s = chs[1].get_value()
        result = ""
        for i in s:
            self.symbol_table.add(chs[0].get_value(), i)
            self.annotate(chs[2])
            result += chs[2].get_value()
            self.symbol_table.pop(chs[0].get_value())
        node.set_value(result)
   
    def construct_for_pack(self, node):
        chs = node.get_children()
        self.annotate(chs[0])
        self.annotate(chs[1])
        self.annotate(chs[2])
        s = chs[2].get_value()
        result = ""
        for tup in s:
            self.symbol_table.add(chs[0].get_value(), tup[0])
            for i, var in enumerate(chs[1].get_value()):
                self.symbol_table.add(var, tup[i + 1])
            self.annotate(chs[3])
            result += chs[3].get_value()
            self.symbol_table.pop(chs[0].get_value())
            for var in chs[1].get_value():
                self.symbol_table.pop(var)
        node.set_value(result)

    def expression_id(self, node):
        self.annotate_children(node)
        id_name = node.get_children()[0].get_value()
        node.set_value(self.symbol_table.get_value(id_name))
    
    def ids_one(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value([chs[0].get_value()])
    
    def ids_many(self, node):
        self.annotate_children(node)
        self.set_value([chs[0].get_value()] + chs[1].get_value())
        
    def expression_dot(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        ch0 = chs[0].get_value()
        ch1 = chs[1].get_value()
        node.set_value(ch0.__dict__[ch1])

    def expression_access(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        ch0 = chs[0].get_value()
        ch1 = chs[1].get_value()
        node.set_value(ch0[ch1])

    def expression_add(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        ch0 = chs[0].get_value()
        ch1 = chs[1].get_value()
        node.set_value(ch0 + ch1)

    def expression_sub(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        ch0 = chs[0].get_value()
        ch1 = chs[1].get_value()
        node.set_value(ch0 - ch1)   
    
    def expression_mul(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        ch0 = chs[0].get_value()
        ch1 = chs[1].get_value()
        node.set_value(ch0 * ch1)
    
    def expression_div(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        ch0 = chs[0].get_value()
        ch1 = chs[1].get_value()
        node.set_value(ch0 / ch1)
    
    def expression_number(self, node):
        chs = node.get_children()
        node.set_value(chs[0])

    def expression_string(self, node):
        chs = node.get_children()
        node.set_value(chs[0])
    
    def expression_eq(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value() == chs[1].get_value())
    def expression_neq(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value() != chs[1].get_value())
    
    def expression_lt(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value() < chs[1].get_value())
    
    def expression_le(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value() <= chs[1].get_value())
    
    def expression_gt(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value() > chs[1].get_value())
    
    def expression_ge(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value() >= chs[1].get_value())

    def expression_and(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value() and chs[1].get_value())
    
    def expression_or(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value() or chs[1].get_value())
    
    def expression_not(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(not chs[0].get_value())
   
    def expression_dispatch_empty(self, node):
       self.annotate_children(node)
       chs = node.get_children()
       node.set_value(chs[0].get_value()())

    def expression_dispatch(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value()(*chs[1].get_value()))
    
    def params_one(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value([chs[0].get_value()])
    
    def params_many(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value() + [chs[1].get_value()])
    
    def param(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value())

    def ID(self, node):
        chs = node.get_children()
        node.set_value(chs[0])

    def DATA(self, node):
        node.set_value(node.get_children()[0])

class Template:
    def __init__(self, template):
        self.ast = parser.parse(template, tracking=True)
        self.symbol_table = SymbolTable()
        self.annotator = Annotator()

    def render(self, **kwargs):
        for k in kwargs:
            self.symbol_table.add(k, kwargs[k])
        self.symbol_table.add('range', range)
        self.symbol_table.add('len', len)
        self.annotator.evaluate(self.ast, self.symbol_table)
        return self.ast.get_value()

if __name__ == "__main__":
    class WithParent:
        def __init__(self):
            self.parent = ['ibrahem']

    class WithName:
        def __init__(self):
            self.name = "7mada"
    def is_prime(n):
        for x in range(2, n):
            if n % x == 0:
                return False
        return True

    data = r"""
    Hello, My name is {{ omar }}
    my parent name is {{ parent.name }}
    I want to condition on something
    {{ if count == 1 }}
    this is data
    {{ omar1.parent[name] }}
    this is another data
    {{ endif }}


    and finally this is for loops:
    {{ for var in range(1, 5) }}
    data inside the loop
    {{ var + "1" }}

    {{ endfor }}

    conditioning on string
    {{ if name == "o\"omar'\qmar" }}
    yay!
    {{ endif }}
    Functinos:
    With empty arguments: {{ f1() }}
    With one arg: {{ f2(1) }}
    With two args: {{ f3(1, 2) }}
    multiple elements for:
    {{ for x, y in enumerate(lst)}}
    {{ str(x) + " " + str(y) }}
    {{ endfor }}
    """
    def f1():
        return 1

    def f2(n):
        return n

    def f3(a, b):
        return a + b

    print(Template(data).render(omar="omar", parent=WithName(), count=1, omar1=WithParent(), name = 0, f1 = f1, f2 = f2, f3 = f3, str = str, enumerate = enumerate, lst = [1, 2, 3]))

