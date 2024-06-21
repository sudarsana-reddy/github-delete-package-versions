import os 
import json
import sys

from github_package_versions_api import GitHubPackageVersionsAPI
from inputs import GitHubPackageInputs

def get_env_variables_with_validation():
    owner = os.getenv("OWNER", "sudarsana-reddy")

    package_list = json.loads(os.getenv("PACKAGE_LIST", '["npm-proj"]'))
    if(len(package_list) == 0):
        print("No packages found in the package list")
        sys.exit(1)

    package_type = os.getenv("PACKAGE_TYPE", "npm")
    if(package_type is None):
        print("PACKAGE_TYPE is required")
        sys.exit(1)
    

    token = os.getenv("PAT")
    if(token is None):
        print("PAT (personal access token) is required")
        sys.exit(1)

    retention_number = int(os.getenv("RETENTION_NUMBER", 3))

    delete_versions_pattern = os.getenv("DELETE_VERSIONS_PATTERN", "1.")
    if(delete_versions_pattern is None):
        print("DELETE_VERSIONS_PATTERN is required")
        sys.exit(1)

    github_package_inputs = GitHubPackageInputs(token=token, 
                                                owner=owner, 
                                                package_type=package_type,
                                                retention_number=retention_number, 
                                                delete_versions_pattern=delete_versions_pattern, 
                                                package_list=package_list)    

    return github_package_inputs;
    

github_package_inputs = get_env_variables_with_validation()
api = GitHubPackageVersionsAPI(github_package_inputs)
api.deleteOldVersions()

