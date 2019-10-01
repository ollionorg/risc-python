# -*- coding: utf-8 -*-
"""Define the RISC models module."""
import logging
import uuid as _uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List

import pandas as pd
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

    def to_list_factory(self, class_type: Any, factory_objects: List[Any]) -> List[Any]:
        """Handle the casting of lists to a list of the provided object type."""
        factories_data: List[Any] = []

        if not factory_objects:
            return factories_data

        if isinstance(factory_objects[0], class_type):
            factories_data = factory_objects
        else:
            factories_data = [class_type(**item) for item in factory_objects]

        return factories_data

    def to_obj_factory(self, class_type: Any, factory_object: Any) -> Any:
        """Handle the casting of an object to the provided object type."""
        if not factory_object:
            return class_type()

        if isinstance(factory_object, class_type):
            return factory_object
        return class_type(**factory_object)


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

    response: Response = Response()


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

    assessments: List[Any] = field(default_factory=list)

    def __post_init__(self):
        """Handle post initialization steps."""
        self.assessments: List[RiscAssessment] = self.to_list_factory(
            class_type=RiscAssessment, factory_objects=self.assessments
        )


@dataclass
class RiscStacks(RiscResponse):
    """Define the Stacks resource model schema."""

    stacks: List[Any] = field(default_factory=list)

    def __post_init__(self):
        """Handle post initialization steps."""
        self.stacks: List[RiscStack] = self.to_list_factory(
            class_type=RiscStack, factory_objects=self.stacks
        )


@dataclass
class RiscStackConnectivity(RiscResourceModel):
    """Define the Connectivity resource model schema."""

    avg_duration_per_connection: float = 0.0
    avg_kbps_per_connection: float = 0.0
    avg_rtt_per_connection: float = 0.0
    connections_seen_via_netstat: int = 0
    dest_location: int = 0
    dest_location_name: str = ""
    max_kbps_per_connection: float = 0.0
    max_rtt_per_connection: float = 0.0
    min_rtt_per_connection: float = 0.0
    number_of_distinct_protocols: int = 0
    number_of_distinct_source_ip_dest_ip_pairs: int = 0
    source_location_name: str = ""
    source_locationid: int = 0
    total_bytes: int = 0
    total_duration_per_connection: float = 0.0
    total_flows: int = 0


@dataclass
class RiscStackConnectivityParent(RiscResourceModel):
    """Define the parent Stack Connectivity resource model schema."""

    connectivity: List[Any] = field(default_factory=list)
    returnStatus: str = ""
    returnStatusDetail: str = ""

    def __post_init__(self):
        """Handle post initialization steps."""
        self.connectivity = self.to_list_factory(
            class_type=RiscStackConnectivity, factory_objects=self.connectivity
        )

    @property
    def dataframe(self):
        """Handle converting the connectivity list of objects to a pandas DataFrame."""
        connectivity_dict: List[Dict[str, Any]] = self.response.json().get(
            "connectivity", []
        )
        if not connectivity_dict:
            return pd.DataFrame()
        return pd.DataFrame.from_dict(connectivity_dict)


@dataclass
class RiscDeviceConnectivity(RiscResourceModel):
    """Define the Device Connectivity resource model schema."""

    avg_duration: float = 0.0
    avg_kbps: float = 0.0
    avg_rtt: float = 0.0
    dest_application: str = ""
    dest_application_context: str = ""
    dest_application_instance: str = ""
    dest_bytes: int = 0
    dest_deviceid: int = 0
    dest_ip: str = ""
    dest_packet_count: int = 0
    dest_packet_loss: int = 0
    dest_port: int = 0
    dest_process: str = ""
    max_kbps: float = 0.0
    max_rtt: float = 0.0
    min_rtt: float = 0.0
    netstat_count: int = 0
    source_application: str = ""
    source_application_context: str = ""
    source_application_instance: str = ""
    source_bytes: int = 0
    source_deviceid: int = 0
    source_packet_count: int = 0
    source_packet_loss: int = 0
    source_process: str = ""
    src_ip: str = ""
    total_bytes: int = 0
    total_duration: float = 0.0
    total_packets: int = 0


@dataclass
class RiscDeviceConnectivityParent(RiscResourceModel):
    """Define the parent Device Connectivity resource model schema."""

    connectivity: List[Any] = field(default_factory=list)
    returnStatus: str = ""
    returnStatusDetail: str = ""

    def __post_init__(self):
        """Handle post initialization steps."""
        self.connectivity = self.to_list_factory(
            class_type=RiscDeviceConnectivity, factory_objects=self.connectivity
        )

    @property
    def dataframe(self):
        """Handle converting the connectivity list of objects to a pandas DataFrame."""
        connectivity_dict: List[Dict[str, Any]] = self.response.json().get(
            "connectivity", []
        )
        if not connectivity_dict:
            return pd.DataFrame()
        return pd.DataFrame.from_dict(connectivity_dict)


@dataclass
class RiscTag(RiscResourceModel):
    """Define the Tag resource model schema."""

    tagid: int = 0
    tagkey: str = ""
    tagvalue: str = ""


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
        """Handle post initialization steps."""
        self.tags: List[RiscTag] = self.to_list_factory(
            class_type=RiscTag, factory_objects=self.tags
        )
