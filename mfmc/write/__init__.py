from collections.abc import Mapping
import dataclasses
import pathlib

import yaml

types_file = pathlib.Path(__file__).parent.parent / "types.yml"
with open(types_file) as f:
    config = yaml.safe_load(f)


def _get_params(
    part_config: Mapping[str, Mapping[str, str]],
) -> list[tuple[str, str] | tuple[str, str, dataclasses.Field]]:
    params = []

    for k, v in {
        **part_config["mandatory_datasets"],
        **part_config["mandatory_attributes"],
    }.items():
        if k == "TYPE":
            continue

        params.append((k.lower(), v))

    try:
        items = {
            **part_config["optional_datasets"],
            **part_config["optional_attributes"],
        }.items()
    except KeyError:
        items = part_config["optional_datasets"].items()

    for k, v in items:
        params.append((k.lower(), v, dataclasses.field(default=None, kw_only=True)))

    return params


Law = dataclasses.make_dataclass("Law", _get_params(config["law"]))
Probe = dataclasses.make_dataclass("Probe", _get_params(config["probe"]))
Sequence = dataclasses.make_dataclass("Sequence", _get_params(config["sequence"]))
