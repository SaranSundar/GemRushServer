from dataclasses import dataclass
from serde import serialize, deserialize
from serde.toml import from_toml, to_toml


@deserialize
@serialize
@dataclass(frozen=True)
class GcpProject:
    project_id: str
    bucket: str
    dataset: str


@deserialize
@serialize
@dataclass(frozen=True)
class Gcp:
    dev: GcpProject
    test: GcpProject
    prod: GcpProject


@deserialize
@serialize
@dataclass(frozen=True)
class Config:
    gcp: Gcp


doc_nested = """
[gcp]
    [gcp.prod]
    project_id = "dataverbinders"
    bucket = "dataverbinders"
    dataset = "some_dataset"

    [gcp.test]
    project_id = "dataverbinders-test"
    bucket = "dataverbinders-test"
    dataset = "some_dataset_test"

    [gcp.dev]
    project_id = "dataverbinders-dev"
    bucket = "dataverbinders-dev"
    dataset = "some_dataset_dev"
"""

cfg = Config(
    Gcp(
        prod=GcpProject("dataverbinders", "dataverbinders", "some_dataset"),
        test=GcpProject("dataverbinders-test", "dataverbinders-test", "some_dataset_test"),
        dev=GcpProject("dataverbinders-dev", "dataverbinders-dev", "some_dataset_dev"),
    )
)

cfg = from_toml(Config, doc_nested)
print(cfg)
print(to_toml(cfg))
