import pytest

from compose_viz.compose import Compose
from compose_viz.extends import Extends
from compose_viz.parser import Parser
from compose_viz.port import Port
from compose_viz.service import Service
from compose_viz.volume import AccessMode, Volume, VolumeType


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "tests/in/000001.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                    ),
                ]
            ),
        ),
        (
            "tests/in/000010.yaml",
            Compose(
                [
                    Service(
                        name="base",
                        image="busybox",
                    ),
                    Service(
                        name="common",
                        extends=Extends(service_name="base"),
                    ),
                    Service(
                        name="cli",
                        extends=Extends(service_name="common"),
                    ),
                ]
            ),
        ),
        (
            "tests/in/000011.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        networks=["admin"],
                        extends=Extends(service_name="frontend"),
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        extends=Extends(service_name="frontend"),
                    ),
                ]
            ),
        ),
        (
            "tests/in/000100.yaml",
            Compose(
                [
                    Service(
                        name="web",
                        image="build from .",
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                    ),
                    Service(
                        name="redis",
                        image="redis:alpine",
                    ),
                ]
            ),
        ),
        (
            "tests/in/000101.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        ports=[
                            Port(host_port="8000", container_port="5001"),
                        ],
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        networks=["back-tier", "admin"],
                    ),
                ]
            ),
        ),
        (
            "tests/in/000110.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                    ),
                    Service(
                        name="monitoring",
                        extends=Extends(service_name="frontend"),
                    ),
                    Service(
                        name="backend",
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5001"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/000111.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        networks=["admin"],
                        extends=Extends(service_name="frontend"),
                    ),
                    Service(
                        name="backend",
                        ports=[
                            Port(host_port="8000", container_port="5001"),
                        ],
                        networks=["back-tier", "admin"],
                        extends=Extends(service_name="frontend"),
                    ),
                ]
            ),
        ),
        (
            "tests/in/001000.yaml",
            Compose(
                [
                    Service(
                        name="web",
                        image="build from .",
                        depends_on=["db", "redis"],
                    ),
                    Service(
                        name="redis",
                        image="redis",
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/001001.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                        depends_on=["monitoring", "backend"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                    ),
                ]
            ),
        ),
        (
            "tests/in/001010.yaml",
            Compose(
                [
                    Service(
                        name="web",
                        depends_on=["db", "redis"],
                        extends=Extends(service_name="redis"),
                    ),
                    Service(
                        name="redis",
                        image="redis",
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/001011.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        networks=["front-tier", "back-tier"],
                        depends_on=["monitoring", "backend"],
                        extends=Extends(service_name="backend"),
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                    ),
                ]
            ),
        ),
        (
            "tests/in/001100.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        depends_on=["backend"],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        ports=[
                            Port(host_port="8000", container_port="5001"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/001101.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                        depends_on=["backend"],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                    ),
                ]
            ),
        ),
        (
            "tests/in/001110.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                    ),
                    Service(
                        name="monitoring",
                        depends_on=["backend"],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                    ),
                    Service(
                        name="backend",
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5001"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/001111.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        networks=["admin"],
                        depends_on=["backend"],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                    ),
                ]
            ),
        ),
        (
            "tests/in/010000.yaml",
            Compose(
                [
                    Service(
                        name="backend",
                        image="awesome/backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/010001.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/010010.yaml",
            Compose(
                [
                    Service(
                        name="common",
                        image="busybox",
                        volumes=[
                            Volume(source="common-volume", target="/var/lib/backup/data", access_mode=AccessMode.rw)
                        ],
                    ),
                    Service(
                        name="cli",
                        extends=Extends(service_name="common"),
                        volumes=[Volume(source="cli-volume", target="/var/lib/backup/data", access_mode=AccessMode.ro)],
                    ),
                ]
            ),
        ),
        (
            "tests/in/010011.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        extends=Extends(service_name="monitoring"),
                    ),
                ]
            ),
        ),
        (
            "tests/in/010100.yaml",
            Compose(
                [
                    Service(
                        name="backend",
                        image="awesome/backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/010101.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/010110.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        extends=Extends(service_name="monitoring"),
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/010111.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        extends=Extends(service_name="monitoring"),
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/011000.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        depends_on=["backend"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                    ),
                ]
            ),
        ),
        (
            "tests/in/011001.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                    ),
                ]
            ),
        ),
        (
            "tests/in/011010.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                    ),
                ]
            ),
        ),
        (
            "tests/in/011011.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                    ),
                ]
            ),
        ),
        (
            "tests/in/011100.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        ports=[
                            Port(host_port="8000", container_port="5000"),
                        ],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["backend"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        ports=[
                            Port(host_port="8000", container_port="5001"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/011101.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/011110.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/011111.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                    ),
                ]
            ),
        ),
        (
            "tests/in/100000.yaml",
            Compose(
                [
                    Service(
                        name="web",
                        image="build from .",
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/100001.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/100010.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        extends=Extends(service_name="frontend"),
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/100011.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        extends=Extends(service_name="frontend"),
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/100100.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/100101.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/100110.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/100111.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/101000.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        depends_on=["monitoring"],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/101001.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        depends_on=["monitoring"],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/101010.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/101011.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/101100.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        depends_on=["monitoring"],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/101101.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        depends_on=["monitoring"],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/101110.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/101111.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/110000.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/110001.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/110010.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        extends=Extends(service_name="frontend"),
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/110011.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        extends=Extends(service_name="frontend"),
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/110100.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/110101.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/110110.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/110111.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/111000.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        depends_on=["backend"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/111001.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/111010.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/111011.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/111100.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/111101.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        image="awesome/backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/111110.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                    ),
                    Service(
                        name="backend",
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
        (
            "tests/in/111111.yaml",
            Compose(
                [
                    Service(
                        name="frontend",
                        image="awesome/webapp",
                        networks=["front-tier", "back-tier"],
                    ),
                    Service(
                        name="monitoring",
                        image="awesome/monitoring",
                        networks=["admin"],
                    ),
                    Service(
                        name="backend",
                        networks=["back-tier", "admin"],
                        volumes=[
                            Volume(source="db-data", target="/data"),
                            Volume(
                                source="/var/run/postgres/postgres.sock",
                                target="/var/run/postgres/postgres.sock",
                                type=VolumeType.bind,
                            ),
                        ],
                        depends_on=["monitoring"],
                        extends=Extends(service_name="frontend"),
                        ports=[
                            Port(host_port="8000", container_port="5010"),
                        ],
                        links=["db:database"],
                    ),
                    Service(
                        name="db",
                        image="postgres",
                    ),
                ]
            ),
        ),
    ],
)
def test_parse_file(test_input: str, expected: Compose) -> None:
    parser = Parser()
    actual = parser.parse(test_input)

    assert len(actual.services) == len(expected.services)

    for actual_service, expected_service in zip(actual.services, expected.services):
        assert actual_service.name == expected_service.name
        assert actual_service.image == expected_service.image

        assert len(actual_service.ports) == len(expected_service.ports)
        for actual_port, expected_port in zip(actual_service.ports, expected_service.ports):
            assert actual_port.host_port == expected_port.host_port
            assert actual_port.container_port == expected_port.container_port
            assert actual_port.protocol == expected_port.protocol

        assert actual_service.networks == expected_service.networks

        assert len(actual_service.volumes) == len(expected_service.volumes)
        for actual_volume, expected_volume in zip(actual_service.volumes, expected_service.volumes):
            assert actual_volume.source == expected_volume.source
            assert actual_volume.target == expected_volume.target
            assert actual_volume.type == expected_volume.type

        assert actual_service.depends_on == expected_service.depends_on
        assert actual_service.links == expected_service.links

        assert (actual_service.extends is not None) == (expected_service.extends is not None)

        if (actual_service.extends is not None) and (expected_service.extends is not None):
            assert actual_service.extends.service_name == expected_service.extends.service_name
            assert actual_service.extends.from_file == expected_service.extends.from_file
