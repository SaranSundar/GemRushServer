from serde import serialize
from dataclasses import dataclass


@serialize(rename_all='pascalcase')
@dataclass
class Foo:
    v: int
