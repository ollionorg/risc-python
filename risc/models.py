# -*- coding: utf-8 -*-
"""Define the RISC models module."""
import logging
import uuid as _uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List

from requests.models import Response
from requests.sessions import Session

logger = logging.getLogger(__name__)


@dataclass
class AbstractRiscModel:
    """Abstract resource model for all RISC models."""

    uuid: _uuid.UUID = _uuid.uuid4()

    def __str__(self):
        """Define the string representation of the abstract RISC model."""
        return f"<{self.__class__.__name__}: {self.uuid!s}>"

    @property
    def to_dict_items(self):
        """Get the dictionary items of the model's attributes."""
        return self.__dict__.items()

    @property
    def to_dict(self):
        """Get the dictionary representation of the model's attributes."""
        items = self.to_dict_items
        return dict(items)


@dataclass
class RiscResponse(AbstractRiscModel):
    """Abstract resource model for all RISC models."""

    response: Response = Response()
    session: Session = Session()
    items: List[Any] = field(default_factory=list)
    return_status: str = ""
    return_status_detail: str = ""
    json: Dict[str, str] = field(default_factory=dict)
    page: int = 0

    # def __repr__(self):
    #     """Define the representation of a RISC response."""
    #     items = ", ".join(f"{item!s}" for item in self.items)
    #     return f"<{self.__class__.__name__}: ({items})>"


@dataclass
class RiscResourceModel(AbstractRiscModel):
    """Abstract resource model for all RISC models."""

    pass


@dataclass
class RiscAssessment(RiscResourceModel):
    """Define the Assessment resource model schema."""

    address: str = ""
    appliance_public_ip: str = ""
    assessment_code: str = ""
    assessment_stage_description: str = ""
    assessment_stage_name: str = ""
    city: str = ""
    company_name: str = ""
    country: str = ""
    end_date: str = ""
    start_date: str = ""
    state: str = ""
    zip: str = ""
    json: Dict[str, str] = field(default_factory=dict)

    def __str__(self):
        """Define the string representation of the abstract RISC model."""
        return f"<{self.__class__.__name__}: {self.assessment_code}>"

    @property
    def is_demo(self):
        """Determine whether or not the Assessment is a demo."""
        return (
            self.company_name == "Customer Sandbox"
            and self.state == "Kentucky"
            and self.zip == "12345"
            and self.appliance_public_ip == "unknown"
        )


@dataclass
class RiscAssessments(RiscResponse):
    """Define the Assessments resource model schema."""

    assessments: List[Any] = field(default_factory=List[Any])

    def __post_init__(self) -> None:
        self.assessments = self.assessment_factory()

    def assessment_factory(self) -> List[RiscAssessment]:
        if not self.assessments:
            return []
        assess = [RiscAssessment(**item) for item in self.assessments]
        return assess


@dataclass
class RiscStacks(RiscResponse):
    """Define the Stacks resource model schema."""

    stacks: List[Any] = field(default_factory=List[Any])

    def __post_init__(self):
        self.stacks = self.stack_factory()

    def stack_factory(self) -> List[Any]:
        if not self.stacks:
            return []
        return [RiscStack(**item) for item in self.stacks]


@dataclass
class RiscStack(RiscResourceModel):
    """Define the Stack resource model schema."""

    confirmed: str = ""
    confirmedby: str = "not set"
    licensed: int = 0
    num_members_with_failed_checks: int = 0
    num_stack_members: int = 0
    stack_name: str = ""
    stackid: int = 0
    tags: List[Any] = field(default_factory=list)

    def __post_init__(self):
        self.tag = self.tag_factory()

    def tag_factory(self) -> List[Any]:
        if not self.tag:
            return []
        return [RiscTag(**item) for item in self.tag]


@dataclass
class RiscTag(RiscResourceModel):
    """Define the Tag resource model schema."""

    tagid: int = 0
    tagkey: str = ""
    tagvalue: str = ""
