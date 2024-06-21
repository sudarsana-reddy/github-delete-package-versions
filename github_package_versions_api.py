import json
import requests

from inputs import GitHubPackageInputs

class GitHubPackageVersionsAPI:
    def __init__(self, github_package_inputs: GitHubPackageInputs):
        """
        Initialize the GitHubPackageVersionsAPI class.
        :param github_package_inputs: GitHubPackageInputs object containing the necessary inputs.
        """       
       
        self.per_page = 100        
        self.base_url = "https://api.github.com"

        self.inputs = github_package_inputs
        self.headers = {
            'Authorization': f'token {self.inputs.token}',
            'Accept': 'application/vnd.github.v3+json'
        }       

    def getPackageVersions(self, package_name):
        
        page_number = 1
        has_next_page = True
        versions = []

        print(f"Retrieving versions for package '{package_name}' ({self.inputs.package_type})")
        try:

            while has_next_page:        
                # Construct the API URL for the package's releases
                package_vesrions_url = f"{self.base_url}/users/{self.inputs.owner}/packages/{self.inputs.package_type}/{package_name}/versions?per_page={self.per_page}&page={page_number}"
                response = requests.get(package_vesrions_url, headers=self.headers)

                if response.status_code == 200:
                    data = response.json()            
                    versions.extend(data)                
                    print(f"Versions in {page_number}: {len(data)}")
                    if(len(data) < self.per_page):
                        has_next_page = False

                else:
                    print(f"Failed to retrieve data: {response.status_code} - {response.text}")
                    has_next_page = False

                page_number += 1   

            # Print the retrieved versions
            versions.sort(key=lambda x: x["created_at"], reverse=True)        
            print(f"Total versions: {len(versions)}")
            print(json.dumps(versions, indent=2))        
        
        except Exception as e:
            print(f"Error occurred: {e}")

        return versions


    def deleteOldVersions(self):    
        for package in self.inputs.package_list:   
            print(f"Deleting old versions for package '{package}' ({self.inputs.package_type})")
            versions = self.getPackageVersions(package)
            branch_versions = [version for version in versions if version["name"].startswith(self.inputs.delete_versions_pattern)]
            if(len(branch_versions) <= self.inputs.retention_number):
                print("No old versions to delete.")
                return        
            to_be_deleted_versions = branch_versions[self.inputs.retention_number:]
            
            failed_versions = []
            print(f"Trying to delete {len(to_be_deleted_versions)} old versions...")

            for version in to_be_deleted_versions:
                print(f"Deleting version: {version['name']}")
                version_url = f"{self.base_url}/users/{self.inputs.owner}/packages/{self.inputs.package_type}/{package}/versions/{version['id']}"
                response = requests.delete(version_url, headers=self.headers)
                if response.status_code == 204:
                    print(f"Deleted version: {version['name']}")
                else:
                    print(f"Failed to delete version: {version['id']} - {response.status_code} - {response.text}")
                    failed_versions.append(version['name'])

            print(f"Deleted {len(to_be_deleted_versions) - len(failed_versions)} versions.")
            if failed_versions:
                print(f"Failed versions: {failed_versions}")    

