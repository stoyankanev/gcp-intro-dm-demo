# GCP Short Intro Demonstration For Tieto Specialists  <!-- omit in toc -->


# Table of Contents  <!-- omit in toc -->
- [Introduction](#Introduction)
- [Generating the SSH Key](#Generating-the-SSH-Key)
- [GCP Solution](#GCP-Solution)
  - [Creating the Environmental Variables Script File](#Creating-the-Environmental-Variables-Script-File)
  - [Creating the Infra Project](#Creating-the-Infra-Project)
  - [Deployment Manager Code](#Deployment-Manager-Code)
  - [Deployment Manager Yaml Configuration](#Deployment-Manager-Yaml-Configuration)
  - [Deployment](#Deployment)
  - [VPC](#VPC)
  - [VM](#VM)
  - [Deployment Script](#Deployment-Script)
  - [Developing the GCP Infra JSON Representation](#Developing-the-GCP-Infra-JSON-Representation)
  - [Incremental Development](#Incremental-Development)
- [Demonstration Manuscript](#Demonstration-Manuscript)
- [Comparing GCP Deployment Manager and Terraform](#Comparing-GCP-Deployment-Manager-and-Terraform)
- [Comparing Cloud IaC Native Tools](#Comparing-Cloud-IaC-Native-Tools)
- [Suggestions How to Continue this Demonstration](#Suggestions-How-to-Continue-this-Demonstration)
- [Issue with Creating the Infra Project Using Deployment Manager](#Issue-with-Creating-the-Infra-Project-Using-Deployment-Manager)


# Introduction

This demonstration can be used in training new cloud specialists who don't need to have any prior knowledge of GCP (Google Cloud Platform) but who want to start working on GCP projects and building their GCP competence (well, a bit of GCP knowledge is required - GCP main concepts, how to use the GCP Portal and CLI).

This demonstration is basically the same as [gcp-intro-demo](https://github.com/tieto-pc/gcp-intro-demo) with one difference: gcp-intro-demo uses [Terraform](https://www.terraform.io/) as IaC tool, and gcp-intro-dm-demo uses [GCP Deployment Manager](https://cloud.google.com/deployment-manager/docs/). The idea is to introduce another way to create infrastructure code in GCP and let developers to compare Terraform and GCP Deployment Manager and make their own decision which tool to use in their future projects.

This project demonstrates basic aspects how to create cloud infrastructure as code. The actual infra is very simple: just one virtual machine instance. We create a virtual private cloud [vpc](https://cloud.google.com/vpc/) and an application subnet into which we create a [VM](https://cloud.google.com/compute/docs/instances/). There is also one [firewall](https://cloud.google.com/vpc/docs/firewalls) in the VPC that allows inbound traffic only using ssh port 22. 

I tried to keep this demonstration as simple as possible. The main purpose is not to provide an example how to create a cloud system (e.g. not recommending VMs over containers) but to provide a very simple example of infrastructure code and tooling related creating the infra. I have provided some suggestions how to continue this demonstration at the end of this document - you can also send me email to my corporate email and suggest what kind of GCP or GCP POCs you need in your team - I can help you to create the POCs for your customer meetings.

There are two equivalent cloud native deployment demonstrations in other "Big three" cloud provider platforms: AWS demonstration - [aws-intro-cloudformation-demo](https://github.com/tieto-pc/aws-intro-cloudformation-demo), and Azure demonstration - [azure-intro-arm-demo](https://github.com/tieto-pc/azure-intro-arm-demo) - compare these native IaC tools between  GCP, AWS and Azure platforms - they are pretty different (when compared to equivalent Terraform based implementations which are incredibly similar - the very reason why Terraform is my choice of IaC tool). There are two chapters at the end of this document in which I compare these tools: "Comparing GCP Deployment Manager and Terraform" and "Comparing Cloud IaC Native Tools".

There are a lot of [GCP Deployment Manager Samples provided by Google](https://github.com/GoogleCloudPlatform/deploymentmanager-samples) - you should use these examples as a starting point for your own GCP Deployment Manager IaC, I did too.


# Generating the SSH Key

Let's first manually generate the ssh key that we need when we validate that we can ssh to the VM (the Terraform version creates the key pair automatically but I didn't bother to automate this part in this demonstration).

You can generate the ssh key that we are going to need using the following procedure (in bash, using Windows you have google how to do it, possibly the easiest way to do this in a Windows box is to use Git Bash).

```bash
mkdir .ssh
cd .ssh
ssh-keygen -t rsa -f dm-vm -C user@debian.com
xclip -sel clip < dm-vm.pub
```

Then paste the string to the ```deployment.yaml``` file (there is a [deployment-template.yaml](dm/deployment-template.yaml) that you can use as a template) - for the value of parameter ```public_key```.

When you are ready with the deployment you can ssh to the VM like:

```bash
ssh -i .ssh/dm-vm user@IP-NUMBER-HERE
```

# GCP Solution

The diagram below depicts the main services / components of the solution.

![GCP Intro Demo Architecture](docs/gcp-intro-demo.png?raw=true "GCP Intro Demo Architecture")

So, the system is extremely simple (for demonstration purposes): Just one VPC, one application subnet and one Compute instance (VM) doing nothing in the subnet. One Firewall rule in the VPC which allows only ssh traffic to the Compute instance. 

## Creating the Environmental Variables Script File

First create environment variables file in ~/.gcp/<YOUR-ADMIN-FILE>.sh. Use file [gcp_env_template.sh](gcp_env_template.sh) as a template.

Then source the environment variables file:

```bash
# Source environment variables.
source ~/.gcp/<ENV-VAR-FILE>.sh
```


## Creating the Infra Project

Due to my GCP organization restrictions I was not able to create the infra project as part of the Deployment Manager IaC (see a more detailed explanation in chapter "Issue with Creating the Infra Project Using Deployment Manager"). Therefore we create the infra project using cli:

```bash
source ~/.gcp/<ENV-VAR-FILE>.sh
./create-infra-proj.sh
```

NOTE: We don't need to create an admin project as in the equivalent [gcp-intro-demo](https://github.com/tieto-pc/gcp-intro-demo) Terraform implementation since we create the deployment and the actual deployed infra resources into the same infra project (and not the deployment in the admin project and the deployed infra resources into the infra project as would have been the case if we could have created the infra project as part of the Deployment Manager IaC, see a more detailed explanation in chapter "Issue with Creating the Infra Project Using Deployment Manager").

The script creates the infra project (id and name are populated by the environment variables file), and then creates a gcloud configuration for the new project and finally turns on the services that we need for the deployment and for the actual infra demonstration (basically compute - for the VM).


## Deployment Manager Code

All right. We have the infra project and the cli configuration now. We are ready to make the infra deployment into the infra project but before that let's investigate our Deployment Manager solution a bit.

As [recommended by Google](https://cloud.google.com/deployment-manager/docs/step-by-step-guide/create-a-template) you should use Python to create your GCP Deployment Manager templates. I love that - I have been using Python for some 20 years and it is my favourite scripting tool. Therefore I'm using Python in this gcp-intro-dm-demo demonstration (other options would have been plain yaml or jinja templating - yak). The Deployment Manager template files and scripts can be found in the [dm](dm) folder.


## Deployment Manager Yaml Configuration

Read the [Creating a Template](https://cloud.google.com/deployment-manager/docs/step-by-step-guide/create-a-template) documentation as an introduction to GCP Deployment Manager configuration files.

First you need to create the Deployment Manager Yaml configuration. Use [deployment-template.yaml](dm/deployment-template.yaml) file as a template. Populate your deployment values to the file. 

This file basically imports the Python configuration files and provides the arguments for various parameters needed in those Python configuration files.


## Deployment

The GCP Deployment Manager expects to find a ```GenerateConfig(context)``` function that it uses to create the infrastructure based on the IaC. The file [deployment.py](dm/deployment.py) file provides this function. The nice thing about using Python instead of JSON/YAML (compared to AWS/CloudFormation and Azure/ARM) is that you can use a real Turing complete programming language - and you can create the solution any way you like. I considered various ways how to create this IaC solution and I finally decided to create this kind of stucture: vpc.py creates the network infrastructure resources and vm.py the VM infrastructure resources and deployment.py uses vpc.py and vm.py and creates the final deployment manager configuration. If you look at the deployment.py you can see that it calls vpc.py and vm.py modules and adds the infra definitions from those modules to the resources list. Finally this function returns a JSON structure with ```resources``` key. 

So, GCP Deployment Manager expects the ```GenerateConfig(context)``` function to return a list which comprises all resources for the infrastructure. We'll see an example later on how to debug this list.


## VPC

The [vpc.py](dm/vpc.py) module creates the [vpc](https://cloud.google.com/vpc/) (virtual private cloud), the subnet and the firewall rule to allow ssh traffic to this VPC. We set auto-create-subnetworks to false since we want to create the subnet using IaC in this demonstration.

Note that in GCP VPC is a global entity and you don't assign an address space ([cidr](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)) to it as in AWS and Azure. You assign the address space to subnet. 

The [firewall rule](https://cloud.google.com/vpc/docs/firewalls) definition opens port 22 for ssh connections. NOTE: We do not restrict any source addresses - in real world system you should restrict the source ip addresses, of course. But don't worry - there is just one VM and we protect the VM with ssh keys (see VM chapter later).

So, the [vpc.py](dm/vpc.py) module creates resources: [network](https://cloud.google.com/compute/docs/reference/rest/v1/networks) (vpc), [subnet](https://cloud.google.com/compute/docs/reference/rest/v1/subnetworks) and [firewall](https://cloud.google.com/compute/docs/reference/rest/v1/firewalls). You can check all [Supported resource types](https://cloud.google.com/deployment-manager/docs/configuration/supported-resource-types) in Google documentation. E.g. the [network](https://cloud.google.com/compute/docs/reference/rest/v1/networks) documentation provides all parameters that you need to populate for that resource. So, basically I used the [Supported resource types](https://cloud.google.com/deployment-manager/docs/configuration/supported-resource-types) to check what parameters I need and created the JSON structure in the related Python function (more about debugging the JSON structure later).

The Deployment Manager Python solution provides a nice way to refer to previously created resources, example in subnet which refers to vpc (network):

```python
'network': '$(ref.%s.selfLink)' % my_vpc_name,
```

Finally the [vpc.py](dm/vpc.py) module returns the JSON representation of the resources in a list (```ret = [network, subnet, firewall]```).

NOTE: After deployment if you look at the "VPC Network" section in GCP Portal you notice that there is also a default VPC network - gcloud created that as part of the infra project creation. We could have deleted that default network but in this demonstration we didn't bother to do that. The nice thing in the equivalent [gcp-intro-demo](https://github.com/tieto-pc/gcp-intro-demo) Terraform IaC implementation is that you can create the infra project as part of the IaC solution and there is a ```auto_create_network``` flag which you can set to false (not to create the default network for the project).

## VM

The [vm.py](dm/vm.py) module creates resources: [external ip](https://cloud.google.com/compute/docs/reference/rest/v1/addresses) and [vm](https://cloud.google.com/compute/docs/reference/rest/v1/instances). The idea is the same as in [vpc.py](dm/vpc.py): the [vm.py](dm/vm.py) module creates the JSON representations of the resources and returns them as a list.


## Deployment Script

The deployment bash script is given in file [create-deployment.sh](dm/create-deployment.sh).


## Developing the GCP Infra JSON Representation

The nice thing about using Python to create the GCP infra JSON representation is that you have the full power of a real programming language. If you look at the Python code and compare it to equivalent [Azure ARM](https://github.com/tieto-pc/azure-intro-arm-demo) and [AWS CloudFormation](https://github.com/tieto-pc/aws-intro-cloudformation-demo) demonstrations you realize that using Python you have a lot more freedom to create the IaC than pure declarative languages: ARM - JSON, and CloudFormation - YAML.

It would be a bit stupid to make some changes to the Python code, try to deploy it using gcloud, wait and find out that your deployment failed for a simple syntax error. Therefore I created [mymain.py](dm/mymain.py) module which I used to check that there were no syntax errors and that the final JSON representation looked the same as [Supported resource types](https://cloud.google.com/deployment-manager/docs/configuration/supported-resource-types) Google documentation.

I used [PyCharm](https://www.jetbrains.com/pycharm/) which is my favourite Python IDE. It is easy to create a Run Configuration in PyCharm and run the main module. In that file I first created a GCP context simulator ```simulateContext()``` which I used to simulate how GCP would inject certain parameters to the deployment (actually I read the exact same Yaml configuration that I use in the actual deployment). So, running the ```main()``` function you can simulate how GCP would create the JSON representation of the infrastructure resources and use this output as a debugging tool. 


## Incremental Development

When I was developing the infra I created the whole IaC solution in one shot and then just deployed it using the [create-deployment.sh](dm/create-deployment.sh) script - and the deployment went smoothly as in American movies. Of course not. :-)  I created the deployment incrementally - as you always have to do when creating new IaC solutions. So, I used the [create-deployment.sh](dm/create-deployment.sh) script to create the initial deployment (for the first resource: network). Then I incrementally created the next resources one after another and updated the deployment after every new resource:

```bash
gcloud deployment-manager deployments update ${VAR_INFRA_PROJ_ID}-deployment --config deployment.yaml --project $VAR_INFRA_PROJ_ID
```

# Demonstration Manuscript

NOTE: These instructions are for Linux (most probably should work for Mac as well). If some Tieto employee is using Windows I would appreciate to get a merge request to provide instructions for a Windows workstation as well.

Let's finally give detailed demonstration manuscript how you are able to deploy the infra of this demonstration to your GCP account - you need a GCP account for this demonstration, of course. You can order a private GCP account or you can contact your line manager if you are allowed to use Tieto's GCP account (contact the administrator in Tieto Yammer Google Cloud Platform group).  **NOTE**: Watch for costs! Always finally destroy your infrastructure once you are ready (never leave any resources to run indefinitely in your GCP account to generate costs).

1. You need some understanding how to use GCP, gcloud etc. Read Google documentation.
2. Install [GCP command line interface](https://cloud.google.com/sdk/).
3. Clone this project: git clone https://github.com/tieto-pc/gcp-intro-dm-demo.git
4. Create the environment variables file as described earlier. Use [gcp_env_template.sh](gcp_env_template.sh) as a template.
5. Create the ssh keys as described above.
6. Open console and source the environment variable file (```source <FILE>```).
7. Run ```create-infra-proj.sh``` which creates the infra project and your gcloud configuration.
8. Go to the [dm](dm) directory.
9. Create a deployment.yaml file. Use [deployment-template.yaml](dm/deployment-template.yaml) file as a template.
10. Run ```create-deployment.sh``` script which calls Deployment Manager using gcloud cli - Deployment Manager runs the deployment process using ```deployment.yaml``` file.
11. Open GCP Portal and browse different views to see what entities were created:
    1. Home => Select the project you created.
    2. Click the "VPC Network". Browse subnets etc.
    3. Click the "Compute Engine". Browse different information regarding the VM.
12. Test to get ssh connection to the VM instance:
    1.  ```gcloud compute instances list``` => list VMs (should be only one) => check the external ip.
    2.  ssh -i .ssh/dm_vm user@IP-NUMBER-HERE
13. Finally destroy the infra using ```gcloud deployment-manager deployments delete ${VAR_INFRA_PROJ_ID}-deployment --project $VAR_INFRA_PROJ_ID``` command. Check manually also using Portal that all resources in that project have been destroyed. **NOTE**: It is utterly important that you always destroy your infrastructure when you don't need it anymore - otherwise the infra will generate costs to you or to your unit. Finally you can destroy the infra project also either using gcloud cli or the GCP Portal.

The official demo is over. Next you could do the equivalent [gcp-intro-demo](https://github.com/tieto-pc/gcp-intro-demo) that uses Terraform. Then compare the Terraform and Deployment Manager code and also the workflows. Evaluate the two tools - which pros and cons they have when compared to each other? Which one would you like to start using? And why?

# Comparing GCP Deployment Manager and Terraform

In this chapter I shortly compare this gcp-intro-dm-demo that uses [GCP Deployment Manager](https://cloud.google.com/deployment-manager/docs/) to the previous [gcp-intro-demo](https://github.com/tieto-pc/gcp-intro-demo) demonstration that uses [Terraform](https://www.terraform.io/) as IaC tool. Possibly later I write a longer blog post regarding my experiences using these two tools.

The major pro regarding Terraform is that if you do multi-cloud development (as I do - AWS, GCP and Azure) it is a really powerfull benefit to have one tool to create IaC for all three cloud platforms. Terraform also provides powerfull declarative language (HCL) for creating IaC solutions. All major cloud services are supported in Terraform and usually new major services are supported pretty soon they are launched by the cloud provider. 

GCP Deployment Manager with Python is not bad either. Compared to AWS CloudFormation and Azure ARM I must say that I liked best GCP Deployment Manager. The possibility to create the IaC solution using a familiar real programming language (Pytho) is a real benefit. You can easily modularize your Python IaC solution and create in-house development&debugging tools (as I did with [mymain.py](dm/mymain.py) ). Since Deployment Manager is the cloud native IaC tool for GCP Google provides a Deployment Manager Portal view to look entities that are part of the deployment - this is a nice feature that cannot be not provided by Terraform, of course. In Deployment Manager view after a successful deployment you can check all parameter values of the resources you deployed. And with a failed deployment the view provides you information regarding the errors in your deployment. 

If you use a good Terraform plugin with a powerfull IDE (as I do with IntelliJ IDEA) writing Terraform code is a real joy. The IDE provides nice context help for parameters that are available for the resource you are editing. I didn't do a Google search if I could find equivalent tooling for the Deployment Manager - if there is one it would have helped editing the JSON structures inside the Python code. In that sense I felt it was easier to create the resources using Terraform than Python/JSON.


# Comparing Cloud IaC Native Tools

The major benefit with GCP Deployment Manager is that you can use Python compared to AWS/CloudFormation (YAML) and Azure/ARM (JSON). Using a real programming language you have a lot more freedom than using a declarative language like YAML or JSON. CloudFormation and ARM provide various mechanisms e.g. how to refer to previously created resources (e.g. CloudFormation: ```IamInstanceProfile: !Ref MyEC2IamInstanceProfile``` and ARM: ```"networkSecurityGroup": { "id": "[resourceId ('Microsoft.Network/networkSecurityGroups', variables('networkSecurityGroupName'))]" }```) - but using a declarative language is always clumsy compared to a real programming language.

Maybe I later on write a longer blog post regarding my experiences with these tools. 



# Suggestions How to Continue this Demonstration

We could add e.g. an instance group and a load balancer to this demonstration but let's keep this demonstration as short as possible so that it can be used as a GCP introduction demonstration. If there are some improvement suggestions that our Tieto developers would like to see in this demonstration let's create other small demonstrations for those purposes, e.g.:
- Create a custom Linux image that has the Java app baked in.
- An instance group (with CRM app baked in) + a load balancer.
- Logs to StackDriver.
- Use container instead of VM.


# Issue with Creating the Infra Project Using Deployment Manager

I spent one day trying to figure out why I can't create the infra project using Deployment Manager. I tried to follow the [Automating project creation with Google Cloud Deployment Manager](https://cloud.google.com/blog/products/gcp/automating-project-creation-with-google-cloud-deployment-manager) document but I got constantly the same error: 

```text
message: '{"ResourceType":"cloudresourcemanager.v1.project","ResourceErrorCode":"403","ResourceErrorMessage":{"code":403,"message":"User
    is not authorized.","status":"PERMISSION_DENIED","statusMessage":"Forbidden","requestPath":"https://cloudresourcemanager.googleapis.com/v1/projects","httpMethod":"POST"}}'
```

This was really frustrating since I was able to create the infra project earlier using Terraform and also using command ```gcloud projects create ...```. But there was no ```roles/resourcemanager.projectCreator``` role (there was Resource Manager / "Project Deleter" and "Project Mover" roles though, :-) ) when I tried to add that role for the admin project's service account as described in [README](https://github.com/GoogleCloudPlatform/deploymentmanager-samples/tree/master/examples/v2/project_creation) of the project_creation sample.

Finally I had a conversation with our GCP organization administrator and realized that it is not possible in our GCP organization to create projects from another project using Deployment Manager due organization policy (it is pretty restricted who can create new projects). Therefore in this demonstration we create the infra project using gcloud cli and the infra project is not part of the actual IaC solution (as in the equivalent [gcp-intro-demo](https://github.com/tieto-pc/gcp-intro-demo) Terraform implementation).



