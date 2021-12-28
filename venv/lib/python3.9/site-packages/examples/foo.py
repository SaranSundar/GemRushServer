from dataclasses import dataclass

from serde import deserialize, serialize
from typing import Optional
from serde.json import from_json, to_json


@deserialize
@serialize
@dataclass
class Foo:
    value: int
    another: Optional[str] = None


def main():
    f = Foo(10)
    print(f"Into Json: {to_json(f)}")

    s = '{"value": 10}'
    print(f"From Json: {from_json(Foo, s)}")


if __name__ == '__main__':
    main()
