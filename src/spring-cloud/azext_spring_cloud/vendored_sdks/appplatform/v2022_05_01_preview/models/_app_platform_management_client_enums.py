# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum, EnumMeta
from six import with_metaclass

class _CaseInsensitiveEnumMeta(EnumMeta):
    def __getitem__(self, name):
        return super().__getitem__(name.upper())

    def __getattr__(cls, name):
        """Return the enum member matching `name`
        We use __getattr__ instead of descriptors or inserting into the enum
        class' __dict__ in order to support `name` and `value` being both
        properties for enum members (which live in the class' __dict__) and
        enum members themselves.
        """
        try:
            return cls._member_map_[name.upper()]
        except KeyError:
            raise AttributeError(name)


class AppResourceProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the App
    """

    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"

class BindingType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Buildpacks Binding Type
    """

    APPLICATION_INSIGHTS = "ApplicationInsights"

class BuildResultProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the KPack build result
    """

    QUEUING = "Queuing"
    BUILDING = "Building"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    DELETING = "Deleting"

class ConfigServerState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """State of the config server.
    """

    NOT_AVAILABLE = "NotAvailable"
    DELETED = "Deleted"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"
    UPDATING = "Updating"

class ConfigurationServiceProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """State of the Application Configuration Service.
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    DELETING = "Deleting"

class CreatedByType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The type of identity that created the resource.
    """

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"

class DeploymentResourceProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the Deployment
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"

class DeploymentResourceStatus(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Status of the Deployment
    """

    STOPPED = "Stopped"
    RUNNING = "Running"

class KPackBuildStageProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The provisioning state of this build stage resource.
    """

    NOT_STARTED = "NotStarted"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"

class ManagedIdentityType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Type of the managed identity
    """

    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned,UserAssigned"

class MonitoringSettingState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """State of the Monitoring Setting.
    """

    NOT_AVAILABLE = "NotAvailable"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"
    UPDATING = "Updating"

class ProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Provisioning state of the Service
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"
    DELETED = "Deleted"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    MOVING = "Moving"
    MOVED = "Moved"
    MOVE_FAILED = "MoveFailed"

class ResourceSkuRestrictionsReasonCode(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Gets the reason for restriction. Possible values include: 'QuotaId',
    'NotAvailableForSubscription'
    """

    QUOTA_ID = "QuotaId"
    NOT_AVAILABLE_FOR_SUBSCRIPTION = "NotAvailableForSubscription"

class ResourceSkuRestrictionsType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Gets the type of restrictions. Possible values include: 'Location', 'Zone'
    """

    LOCATION = "Location"
    ZONE = "Zone"

class ServiceRegistryProvisioningState(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """State of the Service Registry.
    """

    CREATING = "Creating"
    UPDATING = "Updating"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    DELETING = "Deleting"

class SkuScaleType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Gets or sets the type of the scale.
    """

    NONE = "None"
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"

class SupportedRuntimePlatform(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The platform of this runtime version (possible values: "Java" or ".NET").
    """

    JAVA = "Java"
    _NET_CORE = ".NET Core"

class SupportedRuntimeValue(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The raw value which could be passed to deployment CRUD operations.
    """

    JAVA8 = "Java_8"
    JAVA11 = "Java_11"
    NET_CORE31 = "NetCore_31"

class TestKeyType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Type of the test key
    """

    PRIMARY = "Primary"
    SECONDARY = "Secondary"

class TrafficDirection(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The direction of required traffic
    """

    INBOUND = "Inbound"
    OUTBOUND = "Outbound"
