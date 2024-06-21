import os 
import json
import sys

from github_package_versions_api import GitHubPackageVersionsAPI

class MainClass:
    def __init__(self, token, owner):
        self.api = GitHubPackageVersionsAPI(token, owner)
    

if __name__ == "__main__":
    
    packages = json.loads(os.getenv("PACKAGE_LIST", '[]'))
    package_type = os.getenv("PACKAGE_TYPE")
    owner = os.getenv("OWNER", "sudarsana-reddy")
    token = os.getenv("PAT")
    retention_number = int(os.getenv("RETENTION_NUMBER", 4))
    delete_versions_pattern = os.getenv("DELETE_VERSIONS_PATTERN")

    if(len(packages) == 0):
        print("No packages found in the package list")
        sys.exit(0)

    main_class = MainClass(token, owner)
    for package in packages:
        main_class.api.deleteOldVersions(package, package_type, retention_number, delete_versions_pattern)
    
