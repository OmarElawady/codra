from parser import parser
from symboltable import SymbolTable
from functools import reduce
data = r"""
Hello, My name is {{ omar }}
my parent name is {{ parent.name }}
I want to condition on something
{{ if count == 1 }}
this is data
{{ omar.parent[name] }}
this is another data
{{ endif }}


and finally this is for loops:
{{ for var in range(1, 5) }}
data inside the loop
{{ var + 1 }}

{{ endfor }}

conditioning on string
{{ if name == "o\"omar'\qmar" }}
yay!
{{ endif }}
"""
def strip(string):
    if len(string) and string[0] == '\n':
        string = string[1:]
    if len(string) and string[-1] == '\n':
        string = string[:-1]
    return string
class Annotator:
    def __init__(self):
        self.evaluator = {
        }

    def evaluate(self, node, symbol_table):
        self.symbol_table = symbol_table
        self.annotate(node)
    
    def annotate(self, node):
        if type(node) == str:
            print(node)
        getattr(self, node.get_name().replace('-', '_'))(node)
    
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
        node.set_value(strip(self.combine_children(node)))

    def construct_if(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        if chs[0].get_value():
            node.set_value(strip(chs[1].get_value()))
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
        node.set_value(strip(result))
    
    def expression_id(self, node):
        self.annotate_children(node)
        id_name = node.get_children()[0].get_value()
        node.set_value(self.symbol_table.get_value(id_name))

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
   
    def expression_dispatch(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value()(*chs[1].get_value()))
    
    def params_full(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value(chs[0].get_value())
    
    def params_empty(self, node):
        node.set_value([])
    
    def params1(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value([chs[0].get_value()] + chs[1].get_value())

    def params1_1(self, node):
        self.annotate_children(node)
        chs = node.get_children()
        node.set_value([chs[0].get_value()])

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
        self.ast = parser.parse(template)
        self.symbol_table = SymbolTable()
        self.annotator = Annotator()

    def render(self, **kwargs):
        for k in kwargs:
            self.symbol_table.add(k, kwargs[k])
        self.symbol_table.add('range', range)
        self.symbol_table.add('len', len)
        self.annotator.evaluate(self.ast, self.symbol_table)
        return self.ast.get_value()

data = """
{{ for i in range(1, 10) }}
  {{ for j in range(1, i) }}
    {{ if is_prime(i + j) }}
        {{i}} + {{j}} = {{i + j}} is prime
    {{ endif }}
    {{ if not is_prime(i + j) }}
        {{i}} + {{j}} = {{i + j}} is not prime
    {{ endif }}
  {{ endfor }}
{{ endfor }}
"""
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

print(Template(data).render(is_prime=is_prime))

