The script takes the following as input:


1) INFA_Inhouse_url
  The cloud URL for the in-house environment where you wanted to replicate the Role.
  
      E.G:
        https://dm-ap.informaticacloud.com
  

2) INFA_Inhouse_username
  The username of the environment mentioned
  

3) INFA_Inhouse_password
  The password for the username mentioned
  

4) Customer_Server_API_URL
  The customer environment Server URL which can be obtained in the Website URL once logged into the IDMC environment
  
      E.G:
        https://emw1.dm-em.informaticacloud.com
  

5) Customr_Session_ID
  The customer's session ID when logged in through a valid user credential
      

6) Customer_Role_Name
  The customer's user role name that you want to replicate in inhouse.


7) INFA_Inhouse_Role_Name
  The user role name that you want to create in the in-house environment.


Refer to the config.json file for reference.

**Note:
**

The script only works only when the session ID passed in the config json is obtained from logging into the IDMC environment with some valid user credential, i.e., to be short, this doesn't work with the impersonation token.

The output of the script is the newly created role's ID.
