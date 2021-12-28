from serde import serde, to_tuple, from_tuple

@serde
class Foo:
    i: int
    s: str
    f: float
    b: bool


d = to_tuple(Foo(i=10, s='foo', f=100.0, b=True))
print(d)

foo = from_tuple(Foo, d)

print(foo)
