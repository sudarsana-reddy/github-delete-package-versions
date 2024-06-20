import json
import requests

class GitHubPackageVersionsAPI:
    def __init__(self, token, owner):
        """
        Initialize the GitHubPackageVersionsAPI class.

        :param token: GitHub personal access token.
        :param owner: The owner of the repository.
        :param repo: The name of the repository.
        :param package_type: The type of the package (e.g., npm, maven, docker, etc.).
        :param package_name: The name of the package.
        """
        self.per_page = 100
        self.token = token
        self.owner = owner        
        self.base_url = "https://api.github.com"
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }       

    def getPackageVersions(self, package_name, package_type="maven"):

        page_number = 1
        has_next_page = True
        versions = []

        print(f"Retrieving versions for package '{package_name}' ({package_type})")
        try:

            while has_next_page:        
                # Construct the API URL for the package's releases
                package_vesrions_url = f"{self.base_url}/users/{self.owner}/packages/{package_type}/{package_name}/versions?per_page={self.per_page}&page={page_number}"
                response = requests.get(package_vesrions_url, headers=self.headers)

                if response.status_code == 200:
                    data = response.json()            
                    versions.extend(data)                
                    print(f"Total versions: {len(data)}")
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


    def deleteOldVersions(self, package_name, package_type, retention_number, delete_versions_pattern):
        print(f"Deleting old versions for package '{package_name}' ({package_type})")
        versions = self.getPackageVersions(package_name, package_type)
        branch_versions = [version for version in versions if version["name"].startswith(delete_versions_pattern)]
        to_be_deleted_versions = branch_versions[retention_number:]
        
        failed_versions = []
        print(f"Trying to delete {len(to_be_deleted_versions)} old versions...")

        for version in to_be_deleted_versions:
            print(f"Deleting version: {version['name']}")
            version_url = f"{self.base_url}/users/{self.owner}/packages/{package_type}/{package_name}/versions/{version['id']}"
            response = requests.delete(version_url, headers=self.headers)
            if response.status_code == 204:
                print(f"Deleted version: {version['name']}")
            else:
                print(f"Failed to delete version: {version['id']} - {response.status_code} - {response.text}")
                failed_versions.append(version['name'])

        print(f"Deleted {len(to_be_deleted_versions) - len(failed_versions)} versions.")
        if failed_versions:
            print(f"Failed versions: {failed_versions}")    

