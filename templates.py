def cloudformation_template(resources, description=None, params=None):
    d = {
        "AWSTemplateFormatVersion": '2010-09-09',
        "Resources": resources
    }
    if description:
        d["Description"] = description
    if params:
        d["Parameters"] = params
    return d

def parameter_template(description, keytype, additional_params=None):
    d = {
        "Description": description,
        "Type": keytype
    }
    if additional_params:
        for k in additional_params:
            d[k] = additional_params[k]
    return d


def codepipeline_template(key, artifactstorelocation, artifactstoretype, name, rolearn, stages):
    return {
        "Type" : "AWS::CodePipeline::Pipeline",
        "Properties" : {
            "ArtifactStore" : {
                "EncryptionKey" : key,
                "Location" : artifactstorelocation,
                "Type" : artifactstoretype
            },
            "Name" : name,
            "RestartExecutionOnUpdate" : True,
            "RoleArn" : rolearn,
            "Stages" : stages
        }
    }

def codepipeline_stage_template(actions, name):
    return {
        "Actions": actions,
        "Name": name
    }

def codepipeline_action_template(actioncat, actionowner, actionprovider, configuration, name, order, inputartifacts=None, outputartifacts=None):
    d = {
        "ActionTypeId" : {
            "Category" : actioncat,
            "Owner" : actionowner,
            "Provider" : actionprovider,
            "Version" : "1"
        },
        "Configuration" : configuration,
        "Name" : name,
        "RunOrder" : order
    }
    if inputartifacts:
        d["InputArtifacts"] = inputartifacts
    if outputartifacts:
        d["OutputArtifacts"] = outputartifacts
    return d

def codepipeline_webhook_template(secret, name, targetaction, targetpipeline, targetversion):
    return {
        "Type" : "AWS::CodePipeline::Webhook",
        "Properties" : {
            "Authentication" : "GITHUB_HMAC",
            "AuthenticationConfiguration" : {
                "SecretToken" : secret
            },
            "Filters": [{
                "JsonPath": "$.ref",
                "MatchEquals": "refs/heads/\{Branch\}"
            }],
            "Name" : name,
            "RegisterWithThirdParty": True,
            "TargetAction" : targetaction,
            "TargetPipeline" : targetpipeline,
            "TargetPipelineVersion" : targetversion
        }
    }

def role_template(policy=None, service="ec2.amazonaws.com"):
    d = {
        "Type": "AWS::IAM::Role",
        "Properties": {
            "AssumeRolePolicyDocument": {
                "Version" : "2012-10-17",
                "Statement": [ {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [ service ]
                    },
                    "Action": [ "sts:AssumeRole" ]
                } ]
            }
        }
    }
    if policy:
        d["Properties"]["Policies"] = [ {
            "PolicyName": "root",
            "PolicyDocument": policy
        } ]
    return d

def autoscaling_group_template(name, launchconfig, maxsize, minsize, vpczones):
    return {
        "Type" : "AWS::AutoScaling::AutoScalingGroup",
        "Properties" : {
            "AutoScalingGroupName" : name,
            "LaunchConfigurationName" : launchconfig,
            "MaxSize" : maxsize,
            "MinSize" : minsize,
            "VPCZoneIdentifier" : vpczones
        }
    }

def autoscaling_config_template(imageid, instancetype, keyname, secgroups, userdata):
    return {
        "Type" : "AWS::AutoScaling::LaunchConfiguration",
        "Properties" : {
            "AssociatePublicIpAddress" : True,
            "ImageId" : imageid,
            "InstanceType" : instancetype,
            "KeyName" : keyname,
            "SecurityGroups" : secgroups,
            "UserData" : userdata
        }
    }

def codebuild_project_template(artifacts, sources, description, encryptionkey, computetype, image, envirtype, name, servicerole, environmentvariables=[], secgroupids=None, subnets=None, vpcid=None):
    d = {
        "Type" : "AWS::CodeBuild::Project",
        "Properties" : {
            "Artifacts" : artifacts[0],
            "Description" : description,
            "EncryptionKey" : encryptionkey,
            "Environment" : {
                "ComputeType" : computetype,
                "Image" : image,
                "ImagePullCredentialsType" : "CODEBUILD",     
                "Type" : envirtype
            },
            "Name" : name,
            "ServiceRole" : servicerole,
            "Source" : sources[0]
        }
    }
    if len(artifacts) > 1:
        d["SecondaryArtifacts"] = artifacts[1:]
    if len(sources) > 1:
        d["SecondarySources"] = sources[1:]
    if len(environmentvariables) > 0:
        d["EnvironmentVariables"] = environmentvariables
    if secgroupids and subnets and vpcid:
        d["VpcConfig"] = {
            "SecurityGroupIds" : secgroupids,
            "Subnets" : subnets,
            "VpcId" : vpcid
        }
    return d

def codebuild_source_template(sourceid):
    return {
        "SourceIdentifier" : sourceid,
        "Type" : "CODEPIPELINE"
    }

def codebuild_artifact_template(artifactid):
    return {
        "ArtifactIdentifier" : artifactid,
        "Type" : "CODEPIPELINE"
    }

def codedeploy_app_template(name, platform="Server"):
    return {
        "Type" : "AWS::CodeDeploy::Application",
        "Properties" : {
            "ApplicationName" : name,
            "ComputePlatform" : platform
        }
    }

def codedeploy_dg_template(name, elbinfo, rolearn, targetgroupinfo=None):
    d = {
        "Type" : "AWS::CodeDeploy::DeploymentGroup",
        "Properties" : {
            "ApplicationName" : name,
            "DeploymentStyle": {
                "DeploymentOption": "WITH_TRAFFIC_CONTROL"
            },
            "LoadBalancerInfo" : {
                "ElbInfoList" : elbinfo
            },
            "ServiceRoleArn" : rolearn
        }
    }
    if targetgroupinfo:
        d["Properties"]["LoadBalancerInfo"]["TargetGroupInfoList"] = targetgroupinfo
    return d

def ec2_ebsvolume_template(availabilityzone, size):
    return {
        "Type":"AWS::EC2::Volume",
        "Properties" : {
            "AvailabilityZone" : availabilityzone,
            "Size" : size
        }
    }

def ec2_instance_template(imageid, instancetype, keyname, securitygroups, subnetid=None, userdata=None, volumes=None):
    d = {
        "Type" : "AWS::EC2::Instance",
        "Properties" : {
            "ImageId" : imageid,
            "InstanceType" : instancetype,
            "KeyName" : keyname,
            "SecurityGroupIds" : securitygroups
        }
    }
    if subnetid:
        d["Properties"]["SubnetId"] = subnetid
    if userdata:
        d["Properties"]["UserData"] = userdata
    if volumes:
        d["Properties"]["Volumes"] = volumes
    return d

def ec2_sg_template(groupname, description, inboundrules, outboundrules, vpcid):
    return {
        "Type" : "AWS::EC2::SecurityGroup",
        "Properties" : {
            "GroupName" : groupname,
            "GroupDescription" : description,
            "SecurityGroupEgress" : outboundrules,
            "SecurityGroupIngress" : inboundrules,
            "VpcId" : vpcid
        }
    }

def ec2_subnet_template(availabilityzone, cdir, vpcid, public=False):
    return {
        "Type" : "AWS::EC2::Subnet",
        "Properties" : {
            "AvailabilityZone" : availabilityzone,
            "CidrBlock" : cdir,
            "MapPublicIpOnLaunch": public,
            "VpcId" : vpcid
        }
    }

def ec2_vpc_template(cdir="10.0.0.0/16"):
    return {
        "Type" : "AWS::EC2::VPC",
        "Properties" : {
            "CidrBlock" : cdir,
            "EnableDnsSupport" : True,
            "EnableDnsHostnames" : True
        }
    }

def ec2_ig_template():
    return {
        "Type" : "AWS::EC2::InternetGateway",
        "Properties" : {}
    }

def ec2_ig_attachment_template(gateway, vpcid):
    return {
        "Type" : "AWS::EC2::VPCGatewayAttachment",
        "Properties" : {
            "InternetGatewayId" : gateway,
            "VpcId" : vpcid
        }
    }

def ecs_cluster_template(name):
    return {
    "Type" : "AWS::ECS::Cluster",
    "Properties" : {
        "ClusterName" : name
        }
    }

def ecs_service_template(clustername, loadbalancers, taskdef):
    return {
        "Type" : "AWS::ECS::Service",
        "Properties" : {
            "Cluster" : clustername,
            "DesiredCount" : 1,
            "LaunchType" : "EC2",
            "LoadBalancers" : loadbalancers,
            "TaskDefinition" : taskdef
        }
    }

def ecs_takdef_template(containerdef, family):
    return {
        "Type" : "AWS::ECS::TaskDefinition",
        "Properties" : {
            "ContainerDefinitions" : containerdef,
            "ExecutionRoleArn" : "arn:aws:iam::XXX:role/ecsTaskExecutionRole",
            "Family" : family,
            "TaskRoleArn" : "arn:aws:iam::XXX:role/ecsTaskExecutionRole"
        }
    }

def elbv2_lb_template(name, scheme, securitygroups, subnetids, lbtype):
    return {
        "Type" : "AWS::ElasticLoadBalancingV2::LoadBalancer",
        "Properties" : {    
            "IpAddressType" : "ipv4",
            "Name" : name,
            "Scheme" : scheme,
            "SecurityGroups" : securitygroups,
            "Subnets" : subnetids,
            "Type" : lbtype
        }
    }

def elbv2_tg_template(name, port, protocol, targets, targettype, vpcid):
    return {
        "Type" : "AWS::ElasticLoadBalancingV2::TargetGroup",
        "Properties" : {
            "Name" : name,
            "Port" : port,
            "Protocol" : protocol,
            "Targets" : targets,
            "TargetType" : targettype,
            "VpcId" : vpcid
        }
    }

def kms_key_template(description, policy):
    return {
        "Type" : "AWS::KMS::Key",
        "Properties" : {
            "Description" : description,
            "KeyPolicy" : policy
        }
    }

def kms_alias_template(alias, keyid):
    return {
        "Type" : "AWS::KMS::Alias",
        "Properties" : {
            "AliasName" : alias,
            "TargetKeyId" : keyid
        }
    }

def route53_recordset_template(name, dnstype, hostedzoneid=None, dnsname=None, outhostedzoneid=None, records=None, ttl=None):
    d = {
        "Type" : "AWS::Route53::RecordSet",
        "Properties" : {
            "Name" : name,
            "Type" : dnstype
        }
    }
    if hostedzoneid:
        d["Properties"]["HostedZoneId"] = hostedzoneid
    if dnsname and outhostedzoneid:
        d["Properties"]["AliasTarget"] = {
            "DNSName": dnsname,
            "HostedZoneId" : outhostedzoneid
        }
    if records and ttl:
        d["Properties"]["ResourceRecords"] = records
        d["Properties"]["TTL"] = ttl
    return d

def route53_hostedzone_template(dnsname):
    return {
        "Type" : "AWS::Route53::HostedZone",
        "Properties" : {
            "Name" : dnsname
        }
    }

def s3_template(bucketname=None, accesscontrol=None, redirecthost=None, indexdoc=None, errordoc=None):
    if bucketname:
        if redirecthost != None:
            d = {
                "Type" : "AWS::S3::Bucket",
                "Properties" : {
                    "BucketName" : bucketname,
                    "WebsiteConfiguration" : {
                        "RedirectAllRequestsTo": {
                            "HostName" : redirecthost,
                            "Protocol" : "https"
                        }
                    }
                }
            }
        elif indexdoc != None and errordoc != None:
            d = {
                "Type" : "AWS::S3::Bucket",
                "Properties" : {
                    "AccessControl" : accesscontrol,
                    "BucketName" : bucketname,
                    "WebsiteConfiguration" : {
                        "IndexDocument": indexdoc,
                        "ErrorDocument": errordoc
                    }
                }
            }  
        else:
            d = {
                "Type" : "AWS::S3::Bucket",
                "Properties" : {
                    "AccessControl" : accesscontrol,
                    "BucketName" : bucketname,
                }
            }
        if accesscontrol:
            d["Properties"]["AccessControl"] = accesscontrol
    else:
        d = {
            "Type" : "AWS::S3::Bucket"
        }
    return d

def sqs_template(fifoduplicate, queuedelay, fifo, queuename, messagewait, visibilitytimeout):
    return {
        "Type" : "AWS::SQS::Queue",
        "Properties" : {
            "ContentBasedDeduplication" : fifoduplicate,
            "DelaySeconds": queuedelay,
            "FifoQueue" : fifo,
            "QueueName": queuename,
            "ReceiveMessageWaitTimeSeconds": messagewait,
            "VisibilityTimeout": visibilitytimeout
        }
    }

def sqs_policy_template(policyjson, queues):
    return {
        "Type" : "AWS::SQS::QueuePolicy",
        "Properties" : {
            "PolicyDocument" : policyjson,
            "Queues" : queues
        }
    }

def rds_dbinstance_template(allocatedstorage, availabilityzone, dbinstanceclass, dbname, dbsubnetgroup, username, password, vpcsg):
    return {
        "Type" : "AWS::RDS::DBInstance",
        "Properties" :
        {
            "AllocatedStorage" : str(allocatedstorage),
            "AvailabilityZone" : availabilityzone,
            "DBInstanceClass" : dbinstanceclass,
            "DBName" : dbname,
            "DBSubnetGroupName": dbsubnetgroup,
            "Engine" : "postgres",
            "MasterUsername" : username,
            "MasterUserPassword" : password,
            "PubliclyAccessible" : False,
            "StorageEncrypted" : True,
            "StorageType" : "gp2",
            "VPCSecurityGroups" : vpcsg
        }
    }

def rds_subnetgroup_template(description, name, subnets):
    return {
        "Type" : "AWS::RDS::DBSubnetGroup",
        "Properties" : {
            "DBSubnetGroupDescription" : description,
            "DBSubnetGroupName" : name,
            "SubnetIds" : subnets
        }
    }
