# -*- coding: utf-8 -*-
"""Define the RISC utilities."""
import math
from typing import Any, Dict

from risc.__version__ import __version__ as risc_version


def get_user_agent(user_agent: str = "risc-python") -> str:
    """Get the current module version."""
    user_agent_str: str = f"{user_agent}/{risc_version}"
    return user_agent_str


def roundup(x: float) -> int:
    """Round the provided float up to the nearest tens."""
    return int(math.ceil(x / 10.0)) * 10


def determine_bytes(size: float) -> Dict[str, Any]:
    """Determine the highest denomination from bytes to KB, MB, GB, and TB.

    Args:
        size (int): The size, in bytes.

    Returns:
        dict: The dictionary mapping of highest bytes denomination and the equivalent size.

    """
    power = 2 ** 10
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return {"size": size, "label": f"{power_labels[n]}B"}


def format_bytes(size: float, denomination: str = "GB") -> float:
    """Convert bytes to the desired denomination.

    Args:
        size (int): The size, in bytes.
        denomination (str): The byte denomination to convert size to.
            Defaults to: GB. Options are: KB, MB, GB, and TB.

    Returns:
        float: The float formatted to the requested denomination.

    """
    bytes_map = {"KB": 2**10, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    if denomination not in bytes_map.keys():
        raise ValueError(
            f"Invalid option provided to format_bytes denomination argument! Options are: {bytes_map.keys()}"
        )
    converted_size: float = size / bytes_map[denomination]
    return converted_size


def handle_disk_sizing(
    total_size: str, free_size: str, fudge_factor: float = 1.5
) -> Dict[str, Any]:
    """Determine disk sizing based on the provided fudge factor and utilized space."""
    free = int(free_size)
    total = int(total_size)
    used: int = total - free
    proposed_size: float = used * fudge_factor
    recommended: float = float(
        proposed_size if proposed_size <= total and proposed_size != 0 else total
    )
    recommended_gb: float = format_bytes(recommended)
    formatted_recommendation: Dict[str, Any] = {"size": roundup(recommended_gb), "label": "GB"}
    return formatted_recommendation
