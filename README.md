# AzureLBTest

Architectural Prototype for the _Ultrasound in the Cloud_ project.

To run:
```
# Read how to setup environment here:
https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-tutorial-create-first-template?tabs=azure-cli

# Create Azure Resource Group:
az group create --name lbTest --location "North Europe"

# Deploy the 'vm-deploy' ARM template
az deployment group create --name lbtest --resource-group lbtest --template-file <path>/vm-deploy.json
```