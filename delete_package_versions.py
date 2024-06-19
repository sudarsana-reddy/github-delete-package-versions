import os
import json

import requests

packages = ["npm-proj"]

package_type = "npm"

branch = "uat"

api_endpoint = "https://api.github.com"

owner = "sudarsana-reddy"

token = os.getenv("PAT")

retention_number = 3

headers = {
    "Authorization": f"Bearer {token}"
}

per_page = 100

branch_version_mapping = {
    "sit": "0.",
    "uat": "1.",
}


def getPackageVersions(package_name, package_type="maven"):

    page_number = 1

    has_next_page = True

    print(f"Retrieving versions for package '{package_name}' ({package_type})")

    versions = []

    try:

        while has_next_page:        
            # Construct the API URL for the package's releases
            package_vesrions_url = f"{api_endpoint}/users/{owner}/packages/{package_type}/{package_name}/versions?per_page={per_page}&page={page_number}"
            response = requests.get(package_vesrions_url, headers=headers)

            if response.status_code == 200:
                data = response.json()            
                versions.extend(data)                
                print(f"Total versions: {len(data)}")
                if(len(data) < per_page):
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


def deleteOldVersions(package_name, package_type="maven", branch="sit"):
    print(f"Deleting old versions for package '{package_name}' ({package_type})")
    versions = getPackageVersions(package_name, package_type)
    branch_versions = [version for version in versions if version["name"].startswith(branch_version_mapping[branch])]
    to_be_deleted_versions = branch_versions[retention_number:]
    
    failed_versions = []
    print(f"Trying to delete {len(to_be_deleted_versions)} old versions...")
    for version in to_be_deleted_versions:
        print(f"Deleting version: {version['name']}")
        version_url = f"{api_endpoint}/users/{owner}/packages/{package_type}/{package_name}/versions/{version['id']}"
        response = requests.delete(version_url, headers=headers)
        if response.status_code == 204:
            print(f"Deleted version: {version['name']}")
        else:
            print(f"Failed to delete version: {version['id']} - {response.status_code} - {response.text}")
            failed_versions.append(version['id'])

    print(f"Deleted {len(to_be_deleted_versions) - len(failed_versions)} versions.")
    if failed_versions:
        print(f"Failed versions: {failed_versions}")        


def deletePackageVersions():
    for package in packages:
        deleteOldVersions(package, package_type, branch)    

deletePackageVersions()
