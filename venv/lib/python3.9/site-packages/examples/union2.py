from dataclasses import dataclass, field
from typing import Dict, Union, Optional
from serde import serialize, deserialize
from serde.yaml import from_yaml


@deserialize
@serialize
@dataclass
class ReadOperation:
    pattern: str
    type: str
    properties: Optional[Dict[str, str]]


@deserialize
@serialize
@dataclass
class CopyOperation:
    filename: str
    from_: str = field(metadata={'serde_rename': 'from'})


@deserialize
@serialize
@dataclass
class Spec:
    pipeline: Dict[str, Union[CopyOperation, ReadOperation]]


@deserialize
@serialize
@dataclass
class API:
    spec: Spec


with open("api.yml") as f:
    spec = from_yaml(API, f.read())
    print(spec)
