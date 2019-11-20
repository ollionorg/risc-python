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


def format_bytes(size) -> Dict[str, Any]:
    """Format bytes to KB, MB, GB, and TB."""
    # 2**10 = 1024
    power = 2 ** 10
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return {"size": roundup(size), "label": f"{power_labels[n]}B"}


def handle_disk_sizing(
    total_size: str, free_size: str, fudge_factor: float = 1.5
) -> Dict[str, Any]:
    """Determine disk sizing based on the provided fudge factor and utilized space."""
    free = int(free_size)
    total = int(total_size)
    used = total - free
    proposed_size = used * fudge_factor
    recommended = (
        proposed_size if proposed_size <= total and proposed_size != 0 else total
    )
    return format_bytes(recommended)
