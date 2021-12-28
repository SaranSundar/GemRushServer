from dataclasses import dataclass, field
from serde import serialize, deserialize
from serde.json import from_json, to_json
import numpy as np
import numpy.typing as npt


@serialize
@deserialize
@dataclass
class Foo:
    a: npt.NDArray[np.float64] = field(
        metadata={
            'serde_serializer': lambda x: x.tolist(),
            'serde_deserializer': lambda x: np.array(x, dtype=np.float64),
        }
    )

    def __post_init__(self):
        self.a = np.array(self.a, dtype=np.float64)

# Create using a list
f = Foo(a=[1., 0.])

# Check type of "f.a"
print(type(f.a))

# Serialize
print(to_json(f))

# Deserialize
s = '{"a": [1.0, 2.0]}'
print(from_json(Foo, s))
