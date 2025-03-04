from typing import (Any, ClassVar, Dict, List, Mapping, Optional,
                    Sequence)

from typing_extensions import Self

from viam.components.sensor import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes

#list of imports added for the sensor componeent Work in progress
from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, List, cast
from viam.components.sensor import *
from viam.utils import SensorReading
from viam.services.vision import *

#imports for getting Camera directly
from viam.components.camera import *

# Added to connect directly


class SimpleDetection(Sensor, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("jadorg", "simple-module"), "simple-detection"
    )

    
    CAMERA_ATTRIBUTE = "camera"
    SENSOR_ATTRIBUTE = "sensor"
    DETECTION_CONFIDENCE_ATTRIBUTE = "detection_confidence"
    DEFAULT_DETECTION_CONFIDENCE = 0.6

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Sensor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        # Added to read from existing sensor in order to save in variables at creation time
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        fields = config.attributes.fields

        if not SimpleDetection.CAMERA_ATTRIBUTE in fields:
            raise Exception("Missing camera attribute.")
        elif not fields[SimpleDetection.CAMERA_ATTRIBUTE].HasField("string_value"):
            raise Exception("camera attribute must be a string.")

        if not SimpleDetection.SENSOR_ATTRIBUTE in fields:
            raise Exception("Missing sensor attribute.")
        elif not fields[SimpleDetection.SENSOR_ATTRIBUTE].HasField("string_value"):
            raise Exception("sensor attribute must be a string.")

        if SimpleDetection.DETECTION_CONFIDENCE_ATTRIBUTE in fields: 
            if not fields[SimpleDetection.DETECTION_CONFIDENCE_ATTRIBUTE].HasField("number_value"):
                raise Exception("detection_confidence must be a number") 
            elif not 0 <= fields[SimpleDetection.DETECTION_CONFIDENCE_ATTRIBUTE].number_value <= 1: 
                raise Exception("detection_confidence must be between 0 and 1") 

        return []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """

        fields = config.attributes.fields

        self.actual_camera_name = str(fields[SimpleDetection.CAMERA_ATTRIBUTE].string_value)

        # TODO: remove requirement of duplicate entries of a dependency as well as entering the name
        # we should be able to go through the dependencies and find one that matches.
        # alternatively, is there a way to make the dependency implicit so that we don't have to 
        # add it in the config?
        self.actual_sensor_name = str(fields[SimpleDetection.SENSOR_ATTRIBUTE].string_value)
        actual_sensor = dependencies[VisionClient.get_resource_name(self.actual_sensor_name)]
        self.actual_sensor = cast(VisionClient, actual_sensor)

        if SimpleDetection.DETECTION_CONFIDENCE_ATTRIBUTE in fields: 
            self.detection_confidence = fields[SimpleDetection.DETECTION_CONFIDENCE_ATTRIBUTE].number_value
        else:
            self.detection_confidence = SimpleDetection.DEFAULT_DETECTION_CONFIDENCE

        return super().reconfigure(config, dependencies)
    

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        

        cam_detections = await self.actual_sensor.get_detections_from_camera(self.actual_camera_name)

        person_detected = 0
        for detection in cam_detections:
            if detection.confidence >= self.detection_confidence and detection.class_name == "Person":
                person_detected = 1
                break

        return {
            "person_detected": person_detected,
        }

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        raise NotImplementedError()
