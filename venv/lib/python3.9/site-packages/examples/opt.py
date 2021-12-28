from dataclasses import dataclass

from serde import deserialize, serialize
from serde.json import from_json, to_json
from typing import Optional


@deserialize
@serialize
@dataclass
class Bar:
    i: int
    s: str
    f: float
    b: bool


@deserialize
@serialize
@dataclass
class Foo:
    bar: Optional[Bar]


def main():
    f = Foo(bar=Bar(i=10, s='foo', f=100.0, b=True))
    print(f"Into Json: {to_json(f)}")

    s = '{"bar": {"i": 10, "s": "foo", "f": 100.0, "b": true}}'
    print(f"From Json: {from_json(Optional[Foo], s)}")


if __name__ == '__main__':
    main()
