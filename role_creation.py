'''
Works only for the Actual Customer Session ID
'''

import json
import requests

def getIICSSessionID(url, username, password):
    '''
        Calls the Login API and returns the Session ID and the baseAPI URL.
    '''
    IICSLoginurl = f"{url}/saas/public/core/v3/login"
    json_body = {
        "username":f"{username}",
        "password":f"{password}"
    }
    headersIICS = {
        "Content-Type" : "application/json",
        "Accept" : "application/json"
    }

    INFASessionID = "NA"
    baseApiURl = "NA"
    
    try:
        respIICSLogin = requests.post(url=IICSLoginurl, json=json_body, headers=headersIICS)
        
        if respIICSLogin.status_code >= 200 and respIICSLogin.status_code <300:
            respIICS = respIICSLogin.json()
            INFASessionID = respIICS["userInfo"]["sessionId"]
            baseApiURl = respIICS["products"][0]["baseApiUrl"]
        
    except:
        print("Something went wrong in getting the In-house session ID with which the User role will be created. \n Check the \"getIICSSessionID\" method")

    return INFASessionID, baseApiURl


def getUserRolePreviliges(url, Customr_Session_ID, RoleName):
    '''
        Returns the Customer User role priviliges and for reference writes into a local file 'previliges.json'.
    '''
    q = f"roleName==\"{RoleName}\"&expand=privileges"
    headers = {
        "INFA-SESSION-ID" : f"{Customr_Session_ID}"
    }
    RoleDetails_url = f"{url}/saas/public/core/v3/roles?q={q}"

    previliges = []
    try:
        resp = requests.get(url=RoleDetails_url, headers=headers)

        if(resp.status_code >= 200 and resp.status_code < 300):
            roleDetails = resp.json()
            roleDetail = roleDetails[0]

            previliges = roleDetail["privileges"]

        with open('./previliges.json', 'w') as f:
            f.write(str(previliges))
        
    except:
        print("Something went wrong in retrieving the Customer User Role priliges. \n Check the \"getUserRolePreviliges\" method")

    return previliges


def filterprivileges(previliges):
    '''
        Retrieves the Role IDs of the customer's previliges json and returns any array of the Role IDs.
    '''

    filteredPreviliges = []
    supportedServices = ["Admin", "APICenter", "ApplicationIntegration", "CLAIREGPT","DataGovernance", "Ingestion", "IntegrationHub", "DI", "DataMarketplace", "Profile", "DQ", "", "HumanTasks", "MDMConfigUI", "MDMBusinessApp", "MetadataControlPlane", "Monitor", ""]

    '''
        As of Dec 2024, the role replications is only for the services as listed above
    '''

    for prev in previliges:
        if(prev["status"] == "Enabled" or prev["status"] == "Default"):
            '''
                Considering only the Enabled/ Default statuses of the Customer's role
            '''
            if(prev["service"] in supportedServices):
                filteredPreviliges.append(prev["id"])
    
    return filteredPreviliges


def createUserRoleInhouse(sessionID, baseApiURl, INFA_Inhouse_Role_Name, customer_previliges):
    '''
        Creates the Role in the in-house environment and prints the role ID for reference
    '''
    roleCreation_url = f"{baseApiURl}/public/core/v3/roles"
    headers = {
        "INFA-SESSION-ID" : f"{sessionID}"
    }

    previliges = filterprivileges(customer_previliges)

    body = {
        "name" : f"{INFA_Inhouse_Role_Name}",
        "description" : "Created using RoleReplication tool",
        "privileges" : previliges
    }

    try:
        resp = requests.post(url=roleCreation_url, headers=headers, json=body)
        
        newRoleID = ""
        
        if(resp.status_code >= 200 and resp.status_code < 300):
            createdRoleDetail = resp.json()
            newRoleID = createdRoleDetail["id"]
        else:
            print("Error code: ", resp.status_code)
            print("Error: \n", resp.content)
            
            return "NA"
    
    except Exception:
        print("Something went wrong in the Role Creation. \n Check the \"createUserRoleInhouse\" method")
    
    return newRoleID    


if __name__ == "__main__":
    INFA_Inhouse_url = ""
    INFA_Inhouse_username = ""
    INFA_Inhouse_password = ""
    Customer_Server_API_URL = ""
    Customr_Session_ID = ""
    Customer_Role_Name = ""
    INFA_Inhouse_Role_Name = ""
    
    with open("./config.json", "r") as f:
        file_json = json.load(f)
        INFA_Inhouse_url = file_json["INFA_Inhouse_url"]
        INFA_Inhouse_username = file_json["INFA_Inhouse_username"]
        INFA_Inhouse_password = file_json["INFA_Inhouse_password"]

        Customer_Server_API_URL = file_json["Customer_Server_API_URL"]
        Customr_Session_ID = file_json["Customr_Session_ID"]

        Customer_Role_Name = file_json["Customer_Role_Name"]

        INFA_Inhouse_Role_Name = file_json["INFA_Inhouse_Role_Name"]

    '''
        Get the customer role's previliges.
    '''
    customer_previliges = getUserRolePreviliges(
        Customer_Server_API_URL,
        Customr_Session_ID,
        Customer_Role_Name
    )

    '''
        Get the session ID and the base API URL for the in-house environment with which the role will be replicated.
    '''
    sessionID, baseApiURl = getIICSSessionID(
        url=INFA_Inhouse_url,
        username=INFA_Inhouse_username,
        password=INFA_Inhouse_password
    )
    
    '''
        List only the supported services and get the Role IDs; then create the role in-house
    '''
    roleID = createUserRoleInhouse(
        sessionID,
        baseApiURl,
        INFA_Inhouse_Role_Name,
        customer_previliges
    )

    print("Role created\n Role ID: ", roleID)