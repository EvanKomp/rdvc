from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


@dataclass
# pylint: disable=too-many-instance-attributes
class InstanceType:
    name: str
    partition: str
    gpus: int
    cpus: int
    mem: int = 0
    exclusive: bool = False
    nodes: int = 1
    time: Optional[str] = None  # e.g., "01:00:00" for 1 hour
    constraint: Optional[str] = None  # SLURM feature constraint
    additional_sbatch_options: Dict[str, str] = field(default_factory=dict)  # e.g., {"qos": "high", "account": "myaccount"}

    def to_key_value_options(self) -> Dict[str, Any]:
        options = {
            "partition": self.partition,
            "gpus": self.gpus,
            "cpus-per-task": self.cpus,
            "mem": self.mem,
            "nodes": self.nodes,
        }
        if self.constraint:
            options["constraint"] = self.constraint
        if self.time:
            options["time"] = self.time
        # Merge additional sbatch options
        options.update(self.additional_sbatch_options)
        return options

    def to_flag_options(self) -> List[str]:
        if self.exclusive:
            return ["exclusive"]

        return []


class InstanceTypes(Enum):

    DEBUG = InstanceType(
        name="debug",
        partition="debug",
        gpus=0,
        cpus=1,
        mem=1000,
        time="00:05:00",  # 30 minutes
        # additional_sbatch_options={"qos": "normal"} 
    )

    @classmethod
    def to_dict(cls) -> Dict[str, InstanceType]:
        return {instance.value.name: instance.value for instance in cls}

    @classmethod
    def from_name(cls, name: str) -> InstanceType:
        return cls.to_dict()[name]
