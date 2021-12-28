from serde import serde, to_dict, from_dict

@serde
class Foo:
    i: int
    s: str
    f: float
    b: bool


d = to_dict(Foo(i=10, s='foo', f=100.0, b=True))
print(d)

foo = from_dict(Foo, d)

print(foo)
