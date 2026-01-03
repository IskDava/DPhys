import numpy
import math

class MismatchedTypes(Exception):
    def __init__(self, operator: str, *operands):
        s = f"unsupported operand type(s) for {operator}:"
        for operand in operands[:-1]:
            s += f" '{operand}',"
        s = s[:-1]
        s += f" and {operands[-1]}"
        super().__init__(s)

class unit:
    value: float = None
    shortname = "c.u."
    fullname = "conventional unit"
    
    # initialization

    def __init__(self, value: float, shortprexif="", longprefix=""):
        self.value = value * 1.0
        self.shortname = f"{shortprexif}{self.shortname}"

        #if longprefix: longprefix += " "
        
        self.fullname = f"{longprefix}{self.fullname}"

    # representation

    def __repr__(self):
        return f"unit(value={self.value})"
    
    def __str__(self):
        if self.value % 1 == 0:
            return f"{int(self.value)} {self.shortname}"
        return f"{self.value} {self.shortname}"
    
    def full(self):
        if self.value % 1 == 0:
            return f"{int(self.value)} {self.fullname}(-s)"
        return f"{self.value} {self.fullname}(-s)"
    
    def as_giga(self):
        return unit(self.value / 1_000_000_000, shortprexif="G", longprefix="giga")
    
    def as_mega(self):
        return unit(self.value / 1_000_000, shortprexif="M", longprefix="mega")
    
    def as_kilo(self):
        return unit(self.value / 1_000, shortprexif="k", longprefix="kilo")
    
    def as_deci(self):
        return unit(self.value * 10, shortprexif="d", longprefix="deci")
    
    def as_centi(self):
        return unit(self.value * 100, shortprexif="c", longprefix="centi")
    
    def as_milli(self):
        return unit(self.value * 1_000, shortprexif="m", longprefix="milli")
    
    def as_micro(self):
        return unit(self.value * 1_000_000, shortprexif="μ", longprefix="milli")
    
    def as_nano(self):
        return unit(self.value * 1_000_000_000, shortprexif="n", longprefix="nano")

    def __format__(self, format_spec):
        return float.__format__(self.value, format_spec)
    
    # comparision and arithmetic

    def calculate(self, other, operation, operator):
        typ = type(other)
        if isinstance(other, unit):
            return unit(self.value.__getattribute__(operation)(other.value))
        elif typ in [int, float]:
            return unit(self.value.__getattribute__(operation)(other))
        raise MismatchedTypes(operator, self.fullname, typ)


    def __eq__(self, other):
        return self.calculate(other, '__eq__', '==')
    
    def __ne__(self, other):
        return self.calculate(other, '__ne__', '!=')
    
    def __gt__(self, other):
        return self.calculate(other, '__gt__', '>')
    
    def __lt__(self, other):
        return self.calculate(other, '__lt__', '<')
    
    def __ge__(self, other):
        return self.calculate(other, '__ge__', '>=')
    
    def __le__(self, other):
        return self.calculate(other, '__le__', '<=')
    
    def __add__(self, other):
        return self.calculate(other, '__add__', '+')
    
    def __sub__(self, other):
        return self.calculate(other, '__sub__', '-')
        
    def __mul__(self, other):
        return self.calculate(other, '__mul__', '*')
    
    def __truediv__(self, other):
        return self.calculate(other, '__truediv__', '/')
    
    def __floordiv__(self, other):
        return self.calculate(other, '__floordiv__', '//')
    
    def __mod__(self, other):
        return self.calculate(other, '__mod__', '%')
    
    def __pow__(self, other):
        return self.calculate(other, '__pow__', '**')
    
    def __radd__(self, other):
        return self + other
    
    def __rsub__(self, other):
        return -(self - other)
    
    def __rmul__(self, other):
        return self * other
    
    def __rtruediv__(self, other):
        if self == 0:
            return unit(0)
        return (self / other) ** -1
    
    def __rfloordiv__(self, other):
        floordiv = self // other
        if floordiv == 0:
            return unit(0)
        return (self // other) ** -1 // 1
    
    def __rmod__(self, other):
        return self.calculate(other, '__rmod__', '%')
    
    def __rpow__(self, other):
        return self.calculate(other, '__rpow__', '**')
    
    # unary 

    def __neg__(self):
        return unit(-self.value)
    
    def __pos__(self):
        return unit(+self.value)
    
    def __abs__(self):
        return unit(abs(self.value))

def giga(u: unit) -> unit:
    return u * 1_000_000_000

def mega(u: unit) -> unit:
    return u * 1_000_000

def kilo(u: unit) -> unit:
    return u * 1_000

def deci(u: unit) -> unit:
    return u / 10

def centi(u: unit) -> unit:
    return u / 100

def milli(u: unit) -> unit:
    return u / 1_000

def micro(u: unit) -> unit:
    return u / 1_000_000

def nano(u: unit) -> unit:
    return u / 1_000_000_000


a = unit(2_000_000_000)
b = unit(5)


print(a.as_micro())