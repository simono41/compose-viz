from typing import Dict, List, Optional

from ruamel.yaml import YAML

from compose_viz.compose import Compose, Service
from compose_viz.extends import Extends
from compose_viz.port import Port
from compose_viz.volume import Volume, VolumeType


class Parser:
    def __init__(self):
        pass

    def parse(self, file_path: str) -> Compose:
        # load the yaml file
        with open(file_path, "r") as f:
            try:
                yaml = YAML(typ="safe", pure=True)
                yaml_data = yaml.load(f)
            except Exception as e:
                raise RuntimeError(f"Error parsing file '{file_path}': {e}")
        # validate the yaml file
        if not yaml_data:
            raise RuntimeError("Empty yaml file, aborting.")
        if not yaml_data.get("services"):
            raise RuntimeError("No services found, aborting.")

        # parse services data into Service objects
        services = self.parse_service_data(yaml_data["services"])

        # create Compose object
        compose = Compose(services)

        return compose

    def parse_service_data(self, services_yaml_data: Dict[str, dict]) -> List[Service]:
        services: List[Service] = []
        for service, service_name in zip(services_yaml_data.values(), services_yaml_data.keys()):

            service_image: Optional[str] = None
            if service.get("image"):
                service_image = service["image"]
            elif service.get("build"):
                service_image = "build from " + service["build"]

            service_networks: List[str] = []
            if service.get("networks"):
                if type(service["networks"]) is list:
                    service_networks = service["networks"]
                elif type(service["networks"]) is dict:
                    service_networks = list(service["networks"].keys())

            service_extends: Optional[Extends] = None
            if service.get("extends"):
                if service["extends"].get("service"):
                    service_extends = Extends(service_name=service["extends"]["service"])

            service_ports: List[Port] = []
            if service.get("ports"):
                if type(service["ports"]) is list:
                    for port_data in service["ports"]:
                        if ':' not in port_data:
                            raise RuntimeError("Invalid ports input, aborting.")
                        spilt_data = port_data.split(":", 1)
                        service_ports.append(Port(host_port=spilt_data[0], 
                                    container_port=spilt_data[1]))

            service_depends_on: List[str] = []
            if service.get("depends_on"):
                service_depends_on = service["depends_on"]

            service_volumes: List[Volume] = []
            if service.get("volumes"):
                for volume_data in service["volumes"]:
                    if type(volume_data) is dict:
                        volume_source: str = None
                        volume_target: str = None
                        volume_type: VolumeType.volume = None
                        if volume_data.get("source"):
                            volume_source = volume_data["source"]
                        if volume_data.get("target"):
                            volume_target = volume_data["target"]
                        if volume_data.get("type"):
                            volume_type = VolumeType[volume_data["type"]]
                        service_volumes.append(Volume(source=volume_source,
                                                    target=volume_target, 
                                                    type=volume_type))
                    elif type(volume_data) is str:
                        if ':' not in volume_data:
                            raise RuntimeError("Invalid volume input, aborting.")
                        spilt_data = volume_data.split(":", 1)
                        service_volumes.append(Volume(source=spilt_data[0], target=spilt_data[1]))

            service_links: List[str] = []
            if service.get("links"):
                service_links = service["links"]

            services.append(
                Service(
                    name=service_name,
                    image=service_image,
                    networks=service_networks,
                    extends=service_extends,
                    ports=service_ports,
                    depends_on=service_depends_on,
                    volumes=service_volumes,
                    links=service_links,
                )
            )
            # Service print debug
            # print("--------------------")
            # print("Service name: {}".format(service_name))
            # print("image: {}".format(service_image))
            # print("networks: {}".format(service_networks))
            # print("image: {}".format(service_image))
            # print("extends: {}".format(service_extends))
            # print("ports: {}".format(service_ports))
            # print("depends: {}".format(service_depends_on))

        return services
