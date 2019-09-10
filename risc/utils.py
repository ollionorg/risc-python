# -*- coding: utf-8 -*-
"""Define the RISC utilities."""
from risc.__version__ import __version__ as risc_version


def get_user_agent(user_agent: str = "risc-python"):
    """Get the current module version."""
    user_agent_str: str = f"{user_agent}/{risc_version}"
    return user_agent_str
