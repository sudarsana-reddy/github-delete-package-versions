from dataclasses import dataclass, field
from typing import List

@dataclass
class GitHubPackageInputs:
    token: str
    owner: str
    package_type: str
    retention_number: int
    delete_versions_pattern: str
    package_list: List[str] = field(default_factory=list)    
    