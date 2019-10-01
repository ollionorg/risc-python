#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Define the RISC primary module."""
import hashlib
import logging
import os
from typing import Any, Dict

import fire
import requests
from requests.models import Response
from requests.sessions import Session

from .models import RiscAssessment, RiscAssessments, RiscDeviceConnectivityParent, RiscStackConnectivityParent
from .utils import get_user_agent

logger = logging.getLogger(__name__)


class RISC:
    """Define the RISC toplevel class."""

    def __init__(
        self, api_token: str = "", user_id: str = "", password: str = ""
    ) -> None:
        """Initialize the RISC class."""
        self.api_host: str = os.environ.get(
            "RISC_API_HOST", "https://api.riscnetworks.com"
        )
        self.api_version: str = os.environ.get("RISC_API_VERSION", "1_0")
        self.api_endpoint: str = os.environ.get(
            "RISC_API_ENDPOINT", f"{self.api_host}/{self.api_version}"
        )
        self.assessment_code: str = os.environ.get("RISC_ASSESSMENT_CODE", "")
        self.assessment_filters: Dict[str, str] = dict(
            zip(*[iter(os.environ.get("RISC_ASSESSMENT_FILTERS", "").split(","))] * 2)
        )

        self.auth: Dict[str, str] = {
            "user_id": user_id or os.environ.get("RISC_USERNAME", ""),
            "password": password or os.environ.get("RISC_PASSWORD", ""),
            "api_token": api_token or os.environ.get("RISC_API_TOKEN", ""),
        }
        self.session: Session = requests.Session()
        self.session.headers.update({"User-Agent": get_user_agent()})

        if self.assessment_filters:
            self.assessment = self.get_assessment(**self.assessment_filters)
            self.assessment_code = self.assessment.assessment_code

        if (
            not self.assessment_code
            and not self.assessment_filters
            or (self.assessment_filters and not self.assessment_code)
        ):
            logger.error("You must configure the assessment code or filter criteria!")
            return

        self.token = self.get_auth_token()
        self.session.headers.update(
            {"token": self.token, "assessmentcode": self.assessment_code}
        )

    def __repr__(self):
        """Provide the representation for the RISC object."""
        if self.assessment:
            return f"<RISC - User: {self.auth.get('user_id', '')} - Assessment: {self.assessment.assessment_code}>"
        return f"<RISC - User: {self.auth.get('user_id', '')}>"

    def build_auth(self) -> Dict[str, str]:
        """Build the API authentication token."""
        user_id: str = self.auth.get("user_id", "")
        _api_token: str = self.auth.get("api_token", "")
        _password: str = self.auth.get("password", "")
        logger.info("Building authentication dictionary for user: %s" % user_id)

        md5_password: str = hashlib.md5(_password.encode()).hexdigest().upper()
        md5_api_token: str = f"{_api_token}{md5_password}"
        auth_string: str = hashlib.md5(md5_api_token.encode()).hexdigest()
        logger.info("Authentication md5 hash: %s" % auth_string)
        auth = {"userid": user_id, "password": auth_string}

        if self.assessment_code:
            auth["assessmentcode"] = self.assessment_code
        return auth

    def get_assessments(self) -> RiscAssessments:
        """Get the RISC assessment code.

        Returns:
            str: The RISC assessment code.

        """
        payload = self.build_auth()
        response: Response = self.session.get(
            f"{self.api_endpoint}/getAssessments", headers=payload
        )

        if response.status_code != 200:
            logger.error("Unable to retrieve the assessment code!")
            return RiscAssessments()

        assessment_items = response.json().get("assessments", [])
        _assessments = RiscAssessments(assessments=assessment_items)
        return _assessments

    def get_assessment(self, **kwargs) -> RiscAssessment:
        """Get the RISC assessment code.

        Returns:
            str: The RISC assessment code.

        """
        response_data: RiscAssessments = self.get_assessments()
        if not response_data:
            return RiscAssessment()

        if len(response_data.assessments) > 1:
            logger.warn(
                "Multiple assessments found for the provided filter criteria! Returning the first result..."
            )
        return next(item for item in response_data.assessments if not item.is_demo)

    def get_auth_token(self):
        """Authenticate with RISC.

        Returns:
            str: The final authentication token to be used with subsequent requests.

        """
        token: str = ""
        payload: Dict[str, str] = self.build_auth()
        response: Response = self.session.post(
            f"{self.api_endpoint}/getAuthToken", json=payload
        )

        if response.status_code != 200:
            logger.info("Unable to get the authentication token!")
            return token

        try:
            token = response.json().get("token", "")
        except Exception as e:
            logger.error(
                "Error encountered while fetching the authentication token: %s" % e
            )
        return token

    def assets_get_summary(self):
        """Use to retrieve a list of device types and counts."""
        response: Response = self.session.get(f"{self.api_endpoint}/assets/getSummary")
        return response

    def assets_get_assets(
        self,
        device_type: str = "",
        stack_id: int = 0,
        device_id: str = "",
        tag_id: str = "",
        page: int = 0,
    ) -> Response:
        """Use to retrieve a list of device types and counts."""
        uri_base = (
            f"{self.api_endpoint}/assets/getAssets{'/paginated/' if page else ''}"
        )

        if page:
            self.session.headers.update({"page": str(page)})

        if device_type:
            uri = f"{uri_base}/byType/{device_type}"
        elif stack_id:
            uri = f"{uri_base}/byStack/{stack_id}"
        elif device_id:
            uri = f"{uri_base}/byDevice/{device_id}"
        elif tag_id:
            uri = f"{uri_base}/byTag/{tag_id}"
        else:
            logger.error("No filter criteria specified! You must pass in an option!")
            return Response()

        response: Response = self.session.get(uri)

        if page:
            del self.session.headers["page"]

        return response

    def stacks_get_summary(self):
        """Use to retrieve a list of stacks."""
        response: Response = self.session.get(f"{self.api_endpoint}/stacks/getSummary")
        return response

    def stacks_get_summary_cost(self, provider_id: str):
        """Use to retrieve a list of stack costs."""
        response: Response = self.session.get(
            f"{self.api_endpoint}/stacks/getSummaryWithCost/{provider_id}"
        )
        return response

    def stacks_get_connectivity(
        self, stack_id: str = ""
    ) -> RiscStackConnectivityParent:
        """Use to retrieve a list of connected stacks."""
        response: Response = self.session.get(
            f"{self.api_endpoint}/stacks/getConnectivity/{stack_id}"
        )
        if response.status_code != 200:
            return RiscStackConnectivityParent(response=response)

        connectivity_data = response.json()
        return RiscStackConnectivityParent(response=response, **connectivity_data)

    def stacks_get_device_connectivity(
        self, stack_id: int, connectivity_type: str = "internal", page: int = 0
    ) -> RiscDeviceConnectivityParent:
        """Use to retrieve a list of connected stacks."""
        if connectivity_type.lower() not in ["internal", "external"]:
            return RiscDeviceConnectivityParent()

        if page:
            self.session.headers.update({"page": str(page)})

        base_uri = f"{self.api_endpoint}/stacks/get{connectivity_type.title()}DeviceConnectivity"
        uri = f"{base_uri}/{'paginated/' if page else ''}{stack_id}"

        response: Response = self.session.get(uri)

        if page:
            del self.session.headers["page"]

        if response.status_code != 200:
            return RiscDeviceConnectivityParent(response=response)

        connectivity_data = response.json()
        return RiscDeviceConnectivityParent(response=response, **connectivity_data)

    def iaas_get_providers(self):
        """Use to retrieve a list of IaaS providers."""
        response: Response = self.session.get(f"{self.api_endpoint}/iaas/getProviders")
        return response

    def iaas_pricing(self, payload: Dict[str, str]):
        """Use to retrieve a list of IaaS pricing."""
        response: Response = self.session.post(
            f"{self.api_endpoint}/iaas/pricing", json=payload
        )
        return response

    def tags_get_tags(self, payload: Dict[str, str]):
        """Use to retrieve a list of IaaS providers."""
        response: Response = self.session.get(
            f"{self.api_endpoint}/tags/getTags", json=payload
        )
        return response

    def tags_add_tags(self, payload: Dict[str, str]):
        """Use to retrieve a list of IaaS providers."""
        response: Response = self.session.post(
            f"{self.api_endpoint}/tags/addTags", json=payload
        )
        return response

    def assets_search(self, search: str = ""):
        """Get RISC assessment data."""
        response: Response = self.session.get(
            f"{self.api_endpoint}/assets/search/{search}"
        )
        return response

    def ucel_get_checks(self, device_id: str = ""):
        """Use to retrieve a list of checks that have been run against devices."""
        response: Response = self.session.get(
            f"{self.api_endpoint}/ucel/getChecks{'/' + device_id if device_id else ''}"
        )
        return response

    def ucel_get_assets(self, check_id: str = ""):
        """Use to retrieve data on the device(s) by check."""
        response: Response = self.session.get(
            f"{self.api_endpoint}/ucel/getAssets/{check_id}"
        )
        return response

    def ucel_get_assets_paginated(self, check_id: str = "", page: int = 1):
        """Use to retrieve data on the device(s) by check."""
        self.session.headers.update({"page": str(page)})
        response: Response = self.session.get(
            f"{self.api_endpoint}/ucel/getAssets/paginated/{check_id}"
        )
        del self.session.headers["page"]
        return response

    def stacks_get_listeners(self, stack_id: int):
        """Use to retrieve a list of listeners in a stack."""
        response: Response = self.session.get(
            f"{self.api_endpoint}/stacks/getListeners/{stack_id}"
        )
        return response

    def get_swagger(self):
        """Fetch the swagger API configuration file."""
        swagger_resource: Response = self.session.get(
            "https://api.riscnetworks.com/docs/_/resource_list.json"
        )
        return swagger_resource

    def get_server(self, search: str = "", compare: str = "hostname") -> Dict[str, Any]:
        """Sift through the asset search response and only return the relevant host."""
        response: Response = self.assets_search(search=search)
        if response.status_code != 200:
            print("Failure fetching host data!")
            return {}

        host_data = response.json().get("assets", [])
        try:
            return_data = next(
                item
                for item in host_data
                if item["data"][0][compare].lower() == search.lower()
            )
        except (KeyError, IndexError):
            print(f"Unable to find the specified server: ({search})!")
            return {}
        return return_data


def main() -> None:
    """Define the main entry method for the CLI."""
    # Run RISC via the pipeline object for easy CLI access.
    fire.Fire(RISC)


if __name__ == "__main__":
    main()
