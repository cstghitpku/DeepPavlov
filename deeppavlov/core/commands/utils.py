# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pathlib import Path
from typing import Union, Dict, TypeVar

from deeppavlov.core.common.file import read_json

# noinspection PyShadowingBuiltins
_T = TypeVar('_T', str, float, bool, list, dict)


def _parse_item(item: _T, variables: Dict[str, _T]) -> _T:
    if isinstance(item, str):
        return item.format(**variables)
    elif isinstance(item, list):
        return [_parse_item(item, variables) for item in item]
    elif isinstance(item, dict):
        return {k: _parse_item(v, variables) for k, v in item.items()}
    else:
        return item


def parse_config(config: Union[str, Path, dict]) -> dict:
    if isinstance(config, (str, Path)):
        config = read_json(config)

    variables = {
        'DEEPPAVLOV_ROOT': Path(__file__).parent.parent.parent
    }
    for var_dict in config.get('metadata', {}).get('variables', []):
        for name, value in var_dict.items():
            variables[name] = value.format(**variables)

    return _parse_item(config, variables)


def expand_path(path: Union[str, Path]) -> Path:
    """Make path expansion."""
    return Path(path).expanduser().resolve()


def import_packages(packages: list) -> None:
    """Import packages from list to execute their code."""
    for package in packages:
        __import__(package)
