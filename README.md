# AzureLBTest

Architectural Prototype for the _Ultrasound in the Cloud_ project.

To run:
```
# Read how to setup environment here:
https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-tutorial-create-first-template?tabs=azure-cli

# Create Azure Resource Group:
az group create --name lbTest --location "North Europe"

# Deploy the 'vm-deploy' ARM template
# Note the output of the command - specifically the 'load-balancer-ip'
az deployment group create --name lbtest --resource-group lbtest --template-file <path>/vm-deploy.json

# Run the test using the ip/dns of the Load Balancer as seen in the above output
python3 algo-test.py lbtest-4hh4llfhizcxelb.northeurope.cloudapp.azure.com
```