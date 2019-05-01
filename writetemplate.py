from decouple import config
import json
from templates import *

if __name__ == "__main__":
    BASE_URL = config("BASE_URL")
    BASE_NAME = config("BASE_NAME")
    BASE_UNDERNAME = config("BASE_UNDERNAME")

    template = cloudformation_template(**{
        "description": "Basic template for deploying and altering {} Application.".format(BASE_NAME),
        "params": {
            "GitHubAccountName": parameter_template(**{
                "description": "GitHub account name for access to source repositories.",
                "keytype": "String",
                "additional_params": {
                    "NoEcho": True
                }
            }),
            "GitHubFrontendRepo": parameter_template(**{
                "description": "GitHub Frontend source repository.",
                "keytype": "String",
                "additional_params": {
                    "Default": config("GITHUB_FRONTEND_REPO")
                }
            }),
            "GitHubBackendRepo": parameter_template(**{
                "description": "GitHub Backend source repository.",
                "keytype": "String",
                "additional_params": {
                    "Default": config("GITHUB_BACKEND_REPO")
                }
            }),
            "GitHubBranch": parameter_template(**{
                "description": "GitHub branch for development deployment.",
                "keytype": "String",
                "additional_params": {
                    "Default": config("GITHUB_BRANCH")
                }
            }),
            "GitHubFrontendSecret": parameter_template(**{
                "description": "GitHub secret for Frontend webhook access.",
                "keytype": "String",
                "additional_params": {
                    "NoEcho": True
                }
            }),
            "GitHubBackendSecret": parameter_template(**{
                "description": "GitHub secret for Backend webhook access.",
                "keytype": "String",
                "additional_params": {
                    "NoEcho": True
                }
            }),
            "GitHubOAuthToken": parameter_template(**{
                "description": "GitHub OAuth Token for webhook access.",
                "keytype": "String",
                "additional_params": {
                    "NoEcho": True
                }
            }),
            "UserDBUsername": parameter_template(**{
                "description": "Master username for SQL-based User Database.",
                "keytype": "String",
                "additional_params": {
                    "NoEcho": True
                }
            }),
            "UserDBPassword": parameter_template(**{
                "description": "Master password for SQL-based User Database.",
                "keytype": "String",
                "additional_params": {
                    "NoEcho": True
                }
            }),
            "Neo4jDBUsername": parameter_template(**{
                "description": "Master username for Neo4j User Database.",
                "keytype": "String",
                "additional_params": {
                    "NoEcho": True
                }
            }),
            "Neo4jDBPassword": parameter_template(**{
                "description": "Master password for Neo4j Database.",
                "keytype": "String",
                "additional_params": {
                    "NoEcho": True
                }
            }),
            "StackKeyName": parameter_template(**{
                "description": BASE_NAME+" EC2 key name.",
                "keytype": "String",
                "additional_params": {
                    "Default": BASE_UNDERNAME
                }
            }),
        },
        "resources": {
            BASE_NAME+"S3Role": role_template(**{
                "service": "s3.amazonaws.com",
                "policy": {
                    "Statement": [
                        {
                            "Action": [
                                "s3:*"
                            ],
                            "Resource": "*",
                            "Effect": "Allow"
                        }
                    ]
                }
            }),
            BASE_NAME+"PipelineRole": role_template(**{
                "service": "codepipeline.amazonaws.com",
                "policy": {
                    "Statement": [
                        {
                            "Action": [
                                "iam:PassRole"
                            ],
                            "Resource": "*",
                            "Effect": "Allow",
                            "Condition": {
                                "StringEqualsIfExists": {
                                    "iam:PassedToService": [
                                        "cloudformation.amazonaws.com",
                                        "elasticbeanstalk.amazonaws.com",
                                        "ec2.amazonaws.com",
                                        "ecs-tasks.amazonaws.com"
                                    ]
                                }
                            }
                        },
                        {
                            "Action": [
                                "codecommit:CancelUploadArchive",
                                "codecommit:GetBranch",
                                "codecommit:GetCommit",
                                "codecommit:GetUploadArchiveStatus",
                                "codecommit:UploadArchive"
                            ],
                            "Resource": "*",
                            "Effect": "Allow"
                        },
                        {
                            "Action": [
                                "codedeploy:CreateDeployment",
                                "codedeploy:GetApplication",
                                "codedeploy:GetApplicationRevision",
                                "codedeploy:GetDeployment",
                                "codedeploy:GetDeploymentConfig",
                                "codedeploy:RegisterApplicationRevision"
                            ],
                            "Resource": "*",
                            "Effect": "Allow"
                        },
                        {
                            "Action": [
                                "elasticbeanstalk:*",
                                "ec2:*",
                                "elasticloadbalancing:*",
                                "autoscaling:*",
                                "cloudwatch:*",
                                "s3:*",
                                "sns:*",
                                "cloudformation:*",
                                "rds:*",
                                "sqs:*",
                                "ecs:*"
                            ],
                            "Resource": "*",
                            "Effect": "Allow"
                        },
                        {
                            "Action": [
                                "lambda:InvokeFunction",
                                "lambda:ListFunctions"
                            ],
                            "Resource": "*",
                            "Effect": "Allow"
                        },
                        {
                            "Action": [
                                "opsworks:CreateDeployment",
                                "opsworks:DescribeApps",
                                "opsworks:DescribeCommands",
                                "opsworks:DescribeDeployments",
                                "opsworks:DescribeInstances",
                                "opsworks:DescribeStacks",
                                "opsworks:UpdateApp",
                                "opsworks:UpdateStack"
                            ],
                            "Resource": "*",
                            "Effect": "Allow"
                        },
                        {
                            "Action": [
                                "cloudformation:CreateStack",
                                "cloudformation:DeleteStack",
                                "cloudformation:DescribeStacks",
                                "cloudformation:UpdateStack",
                                "cloudformation:CreateChangeSet",
                                "cloudformation:DeleteChangeSet",
                                "cloudformation:DescribeChangeSet",
                                "cloudformation:ExecuteChangeSet",
                                "cloudformation:SetStackPolicy",
                                "cloudformation:ValidateTemplate"
                            ],
                            "Resource": "*",
                            "Effect": "Allow"
                        },
                        {
                            "Action": [
                                "codebuild:BatchGetBuilds",
                                "codebuild:StartBuild"
                            ],
                            "Resource": "*",
                            "Effect": "Allow"
                        },
                        {
                            "Effect": "Allow",
                            "Action": [
                                "devicefarm:ListProjects",
                                "devicefarm:ListDevicePools",
                                "devicefarm:GetRun",
                                "devicefarm:GetUpload",
                                "devicefarm:CreateUpload",
                                "devicefarm:ScheduleRun"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Effect": "Allow",
                            "Action": [
                                "servicecatalog:ListProvisioningArtifacts",
                                "servicecatalog:CreateProvisioningArtifact",
                                "servicecatalog:DescribeProvisioningArtifact",
                                "servicecatalog:DeleteProvisioningArtifact",
                                "servicecatalog:UpdateProduct"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Effect": "Allow",
                            "Action": [
                                "cloudformation:ValidateTemplate"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Effect": "Allow",
                            "Action": [
                                "ecr:DescribeImages"
                            ],
                            "Resource": "*"
                        }
                    ]
                }
            }),
            BASE_NAME+"DeployRole": role_template(**{
                "service": "codedeploy.amazonaws.com",
                "policy": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": [
                                "s3:*"
                            ],
                            "Resource": "*"
                        }
                    ]
                }
            }),
            BASE_NAME+"BuildRole": role_template(**{
                "service": "codebuild.amazonaws.com",
                "policy": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "CloudWatchLogsPolicy",
                            "Effect": "Allow",
                            "Action": [
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents"
                            ],
                            "Resource": [
                                "*"
                            ]
                        },
                        {
                            "Sid": "CodeCommitPolicy",
                            "Effect": "Allow",
                            "Action": [
                                "codecommit:GitPull"
                            ],
                            "Resource": [
                                "*"
                            ]
                        },
                        {
                            "Sid": "S3GetObjectPolicy",
                            "Effect": "Allow",
                            "Action": [
                                "s3:GetObject",
                                "s3:GetObjectVersion"
                            ],
                            "Resource": [
                                "*"
                            ]
                        },
                        {
                            "Sid": "S3PutObjectPolicy",
                            "Effect": "Allow",
                            "Action": [
                                "s3:PutObject"
                            ],
                            "Resource": [
                                "*"
                            ]
                        },
                        {
                            "Sid": "ECRPullPolicy",
                            "Effect": "Allow",
                            "Action": [
                                "ecr:BatchCheckLayerAvailability",
                                "ecr:GetDownloadUrlForLayer",
                                "ecr:BatchGetImage"
                            ],
                            "Resource": [
                                "*"
                            ]
                        },
                        {
                            "Sid": "ECRAuthPolicy",
                            "Effect": "Allow",
                            "Action": [
                                "ecr:GetAuthorizationToken"
                            ],
                            "Resource": [
                                "*"
                            ]
                        }    
                    ]
                }
            }),
            BASE_NAME+"Pipeline": codepipeline_template(**{
                "key": {
                    "Id": {"Ref": BASE_NAME+"Key"},
                    "Type": "KMS"
                },
                "artifactstorelocation": {"Ref": BASE_NAME+"ArtifactStore"},
                "artifactstoretype": "S3",
                "name": BASE_UNDERNAME+"-pipeline",
                "rolearn": {"Fn::GetAtt": [BASE_NAME+"PipelineRole", "Arn"]},
                "stages": [
                    codepipeline_stage_template(**{
                        "actions": [
                            codepipeline_action_template(**{
                                "actioncat": "Source",
                                "actionowner": "ThirdParty",
                                "actionprovider": "GitHub",
                                "configuration": {
                                    "Owner": {"Ref": "GitHubAccountName"},
                                    "Repo": {"Ref": "GitHubFrontendRepo"},
                                    "PollForSourceChanges": False,
                                    "Branch": {"Ref": "GitHubBranch"},
                                    "OAuthToken": {"Ref": "GitHubOAuthToken"}
                                },
                                "name": "FrontendApplicationSource",
                                "order": 1,
                                "inputartifacts": None,
                                "outputartifacts": [
                                    {
                                        "Name" : "FrontendSourceArtifact"
                                    }
                                ]
                            }),
                            codepipeline_action_template(**{
                                "actioncat": "Source",
                                "actionowner": "ThirdParty",
                                "actionprovider": "GitHub",
                                "configuration": {
                                    "Owner": {"Ref": "GitHubAccountName"},
                                    "Repo": {"Ref": "GitHubBackendRepo"},
                                    "PollForSourceChanges": False,
                                    "Branch": {"Ref": "GitHubBranch"},
                                    "OAuthToken": {"Ref": "GitHubOAuthToken"}
                                },
                                "name": "BackendApplicationSource",
                                "order": 1,
                                "inputartifacts": None,
                                "outputartifacts": [
                                    {
                                        "Name" : "BackendSourceArtifact"
                                    }
                                ]
                            })
                        ],
                        "name": "Sources"
                    }),
                    codepipeline_stage_template(**{
                        "actions": [
                            codepipeline_action_template(**{
                                "actioncat": "Build",
                                "actionowner": "AWS",
                                "actionprovider": "CodeBuild",
                                "configuration": {
                                    "ProjectName": {"Ref": BASE_NAME+"FrontendBuildProject"},
                                    "PrimarySource": "FrontendSourceArtifact"
                                },
                                "name": "FrontendApplicationDeploy",
                                "order": 1,
                                "inputartifacts": [
                                    {
                                        "Name" : "FrontendSourceArtifact"
                                    }
                                ],
                                "outputartifacts": [
                                    {
                                        "Name" : "FrontendBuildArtifact"
                                    }
                                ]
                            }),
                            codepipeline_action_template(**{
                                "actioncat": "Build",
                                "actionowner": "AWS",
                                "actionprovider": "CodeBuild",
                                "configuration": {
                                    "ProjectName": {"Ref": BASE_NAME+"BackendBuildProject"},
                                    "PrimarySource": "BackendSourceArtifact"
                                },
                                "name": "BackendApplicationDeploy",
                                "order": 1,
                                "inputartifacts": [
                                    {
                                        "Name" : "BackendSourceArtifact"
                                    }
                                ],
                                "outputartifacts": [
                                    {
                                        "Name" : "BackendBuildArtifact"
                                    }
                                ]
                            })
                        ],
                        "name": "Build"
                    }),
                    codepipeline_stage_template(**{
                        "actions": [
                            codepipeline_action_template(**{
                                "actioncat": "Deploy",
                                "actionowner": "AWS",
                                "actionprovider": "S3",
                                "configuration": {
                                    "BucketName": {"Ref": BASE_NAME+"FrontendDeploymentBucket"},
                                    "Extract": True
                                },
                                "name": "FrontendApplicationDeploy",
                                "order": 1,
                                "inputartifacts": [
                                    {
                                        "Name" : "BackendBuildArtifact"
                                    }
                                ]
                            }),
                            codepipeline_action_template(**{
                                "actioncat": "Deploy",
                                "actionowner": "AWS",
                                "actionprovider": "CodeDeploy",
                                "configuration": {
                                    "ApplicationName": {"Ref": BASE_NAME+"BackendDeployApplication"},
                                    "DeploymentGroupName": {"Ref": BASE_NAME+"BackendDeployGroup"}
                                },
                                "name": "BackendApplicationDeploy",
                                "order": 1,
                                "inputartifacts": [
                                    {
                                        "Name" : "BackendBuildArtifact"
                                    }
                                ]
                            })
                        ],
                        "name": "Deploy"
                    })
                ]
            }),
            BASE_NAME+"ArtifactStore": s3_template(),
            # BASE_NAME+"FrontendWebhook": codepipeline_webhook_template(**{
            #     "secret": {"Ref": "GitHubSecret"},
            #     "name": BASE_UNDERNAME+"-frontend-webhook",
            #     "targetaction": "FrontendApplicationSource",
            #     "targetpipeline": {"Ref": BASE_NAME+"Pipeline"},
            #     "targetversion": "1"
            # }),
            # BASE_NAME+"BackendWebhook": codepipeline_webhook_template(**{
            #     "secret": {"Ref": "GitHubSecret"},
            #     "name": BASE_UNDERNAME+"-backend-webhook",
            #     "targetaction": "BackendApplicationSource",
            #     "targetpipeline": {"Ref": BASE_NAME+"Pipeline"},
            #     "targetversion": "1"
            # }),
            BASE_NAME+"FrontendBuildProject": codebuild_project_template(**{
                "artifacts": [codebuild_artifact_template(**{
                    "artifactid": "FrontendApplicationBuildArtifact"
                })],
                "sources": [codebuild_source_template(**{
                    "sourceid": "FrontendApplicationSource"
                })],
                "description": "Builds static react application Frontend for {}.".format(BASE_NAME),
                "encryptionkey": {"Ref": BASE_NAME+"Key"},
                "computetype": "BUILD_GENERAL1_SMALL",
                "image": "aws/codebuild/standard:1.0",
                "envirtype": "LINUX_CONTAINER",
                "name": BASE_UNDERNAME+"-frontend-build",
                "servicerole": {"Ref": BASE_NAME+"BuildRole"}
            }),
            BASE_NAME+"BackendBuildProject": codebuild_project_template(**{
                "artifacts": [codebuild_artifact_template(**{
                    "artifactid": "BackendApplicationBuildArtifact"
                })],
                "sources": [codebuild_source_template(**{
                    "sourceid": "BackendApplicationSource"
                })],
                "description": "Builds Flask application Backend for {}.".format(BASE_NAME),
                "encryptionkey": {"Ref": BASE_NAME+"Key"},
                "computetype": "BUILD_GENERAL1_SMALL",
                "image": "aws/codebuild/standard:1.0",
                "envirtype": "LINUX_CONTAINER",
                "name": BASE_UNDERNAME+"-backend-build",
                "servicerole": {"Ref": BASE_NAME+"BuildRole"}
            }),
            BASE_NAME+"FrontendDeploymentBucket": s3_template(**{
                "accesscontrol": "PublicRead",
                "bucketname": BASE_URL,
                "indexdoc": "index.html",
                "errordoc": "index.html"
            }),
            BASE_NAME+"PhotoBucket": s3_template(**{
                "accesscontrol": "Private",
                "bucketname": "files."+BASE_URL
            }),
            BASE_NAME+"BackendDeployApplication": codedeploy_app_template(**{
                "name": BASE_NAME+"BackendCodeDeployApp"
            }),
            BASE_NAME+"BackendDeployGroup": codedeploy_dg_template(**{
                "name": {"Ref": BASE_NAME+"BackendDeployApplication"},
                "elbinfo": [{"Name": {"Fn::GetAtt": [BASE_NAME+"BackendELB", "LoadBalancerName"]}}],
                "rolearn": {"Fn::GetAtt": [BASE_NAME+"DeployRole", "Arn"]}
            }),
            BASE_NAME+"BackendEC2Server": ec2_instance_template(**{
                "imageid": "ami-0de53d8956e8dcf80",
                "instancetype": "t2.micro",
                "keyname": {"Ref": "StackKeyName"},
                "securitygroups": [{"Ref": BASE_NAME+"PublicSG"}],
                "subnetid": {"Ref": BASE_NAME+"SubnetPublicA"}
            }),
            BASE_NAME+"BackendELB": elbv2_lb_template(**{
                "name": BASE_UNDERNAME+"-backend-elb",
                "scheme": "internet-facing",
                "securitygroups": [
                    {"Ref": BASE_NAME+"PublicSG"}
                ],
                "subnetids": [
                    {"Ref": BASE_NAME+"SubnetPublicA"},
                    {"Ref": BASE_NAME+"SubnetPublicB"}
                ],
                "lbtype": "application"
            }),
            # BASE_NAME+"BackendELBHTTPTargetGroup": elbv2_tg_template(**{
            #     "name": BASE_UNDERNAME+"-backend-http",
            #     "port": 80,
            #     "protocol": "TCP",
            #     "targets": [
            #         {
            #             "Id" : {"Ref": BASE_NAME+"BackendEC2Server"},
            #             "Port" : 80
            #         }
            #     ],
            #     "targettype": "instance",
            #     "vpcid": {"Ref": BASE_NAME+"VPC"}
            # }),
            # BASE_NAME+"BackendELBHTTPSTargetGroup": elbv2_tg_template(**{
            #     "name": BASE_UNDERNAME+"-backend-https",
            #     "port": 443,
            #     "protocol": "TCP",
            #     "targets": [
            #         {
            #             "Id" : {"Ref": BASE_NAME+"BackendEC2Server"},
            #             "Port" : 443
            #         }
            #     ],
            #     "targettype": "instance",
            #     "vpcid": {"Ref": BASE_NAME+"VPC"}
            # }),
            BASE_NAME+"UserDB": rds_dbinstance_template(**{
                "allocatedstorage": 20,
                "availabilityzone": "us-east-1a",
                "dbinstanceclass": "db.t2.medium",
                "dbname": BASE_NAME+"DBUser",
                "dbsubnetgroup": {"Ref": BASE_NAME+"DBSubnetGroup"},
                "username": {"Ref": "UserDBUsername"},
                "password": {"Ref": "UserDBPassword"},
                "vpcsg": [{"Ref": BASE_NAME+"PrivateUserDBSG"}]
            }),
            BASE_NAME+"DBSubnetGroup": rds_subnetgroup_template(**{
                "description": BASE_NAME+" DB subnet group.",
                "name": BASE_UNDERNAME+"-db-subgroup",
                "subnets": [
                    {"Ref": BASE_NAME+"SubnetPrivateA"},
                    {"Ref": BASE_NAME+"SubnetPrivateB"},
                    {"Ref": BASE_NAME+"SubnetPrivateC"},
                    {"Ref": BASE_NAME+"SubnetPrivateD"}
                ]
            }),
            BASE_NAME+"GraphDB": ec2_instance_template(**{
                "imageid": "ami-80861296",
                "instancetype": "t2.medium",
                "keyname": {"Ref": "StackKeyName"},
                "securitygroups": [{"Ref": BASE_NAME+"PrivateNeoSG"}],
                "subnetid": {"Ref": BASE_NAME+"SubnetPrivateC"},
                "userdata": { "Fn::Base64" : { "Fn::Join" : ["", [
                    "#!/bin/bash -v\n",
                    "# Make the filesystem for the database\n",
                    "mkdir -p /var/lib/neo4j\n",
                    "mkfs.ext4 /dev/sdb\n",
                    "mount /dev/sdb /var/lib/neo4j\n",
                    "echo '/dev/sdb /var/lib/neo4j auto defaults 0 0' >> /etc/fstab\n",
                    "wget -O - http://debian.neo4j.org/neotechnology.gpg.key| apt-key add -\n",
                    "echo 'deb http://debian.neo4j.org/repo stable/' > /etc/apt/sources.list.d/neo4j.list\n",
                    "apt-get update -y\n",
                    "apt-get install -y openjdk-8-jre neo4j-enterprise haproxy\n",
                    "cat <<EOF > /etc/haproxy/haproxy.cfg\n",
                    "global\n",
                    "    daemon\n",
                    "    maxconn 256\n",
                    "\n",
                    "defaults\n",
                    "    mode http\n",
                    "    timeout connect 5000ms\n",
                    "    timeout client 50000ms\n",
                    "    timeout server 50000ms\n",
                    "",
                    "frontend http-in\n",
                    "    bind *:80\n",
                    "    default_backend neo4j\n",
                    "",
                    "\n",
                    "backend neo4j\n",
                    "    server s1 127.0.0.1:7474 maxconn 32\n",
                    "\n",
                    "listen admin\n",
                    "    bind *:8080\n",
                    "    stats enable\n",
                    "EOF\n",
                    "# install the packages \n",
                    "# tweak the config\n",
                    "sed -i 's/ENABLED=0/ENABLED=1/' /etc/default/haproxy\n",
                    "echo 'dbms.connector.bolt.address=0.0.0.0:7687' >> /etc/neo4j/neo4j.conf\n",
                    "echo 'wrapper.java.additional=-Dneo4j.ext.udc.source=ec2neo' >> /etc/neo4j/neo4j-wrapper.conf\n",
                    "service neo4j restart\n",
                    "service haproxy restart\n",
                    "cat <<EOF > /etc/cron.daily/neo4j_backup\n",
                    "#!/bin/bash\n",
                    "set -e\n",
                    "backup_dir='/var/tmp/neo4j_backup'\n",
                    "backup_archive='/mnt'\n",
                    "neo4j-backup --from single://localhost -to \\${backup_dir}\n",
                    "tar -czf \\${backup_archive}//neo4j_backup.\\$(date +%FT%T).tgz \\${backup_dir}\n",
                    "rm -rf \\${backup_dir}\n",
                    "EOF\n",
                    "chown root:root /etc/cron.daily/neo4j_backup\n",
                    "chmod 0755 /etc/cron.daily/neo4j_backup\n"
                ]]}},
                "volumes" : [
                    {
                        "VolumeId" : { "Ref" : BASE_NAME+"GraphDBEBSVolume" },
                        "Device" : "/dev/sdj"
                    }
                ]
            }),
            BASE_NAME+"GraphDBEBSVolume": ec2_ebsvolume_template(**{
                "availabilityzone": {"Fn::GetAtt": [BASE_NAME+"SubnetPrivateC", "AvailabilityZone"]},
                "size": "100"
            }),
            BASE_NAME+"Key": kms_key_template(**{
                "description": BASE_NAME+" KMS key.",
                "policy": {
                    "Version": "2012-10-17",
                    "Id": BASE_UNDERNAME+"-key-default",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": { "AWS": "arn:aws:iam::380871635215:root" },
                            "Action": [
                                "kms:*"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Effect": "Allow",
                            "Principal": { "AWS": {"Fn::GetAtt": [BASE_NAME+"PipelineRole", "Arn"]} },
                            "Action": [
                                "kms:*"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Effect": "Allow",
                            "Principal": { "AWS": {"Fn::GetAtt": [BASE_NAME+"BuildRole", "Arn"]} },
                            "Action": [
                                "kms:*"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Effect": "Allow",
                            "Principal": { "AWS": {"Fn::GetAtt": [BASE_NAME+"DeployRole", "Arn"]} },
                            "Action": [
                                "kms:*"
                            ],
                            "Resource": "*"
                        }
                    ]
                }
            }),
            BASE_NAME+"VPC": ec2_vpc_template(),
            BASE_NAME+"VPCInternetGateway": ec2_ig_template(),
            BASE_NAME+"VPCInternetGatewayAttatchment": ec2_ig_attachment_template(**{
                "gateway": {"Ref": BASE_NAME+"VPCInternetGateway"},
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"SubnetPublicA": ec2_subnet_template(**{
                "availabilityzone": "us-east-1a",
                "cdir": "10.0.1.0/24",
                "public": True,
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"SubnetPublicB": ec2_subnet_template(**{
                "availabilityzone": "us-east-1b",
                "cdir": "10.0.2.0/24",
                "public": True,
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"SubnetPrivateA": ec2_subnet_template(**{
                "availabilityzone": "us-east-1a",
                "cdir": "10.0.3.0/24",
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"SubnetPrivateB": ec2_subnet_template(**{
                "availabilityzone": "us-east-1b",
                "cdir": "10.0.4.0/24",
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"SubnetPrivateC": ec2_subnet_template(**{
                "availabilityzone": "us-east-1c",
                "cdir": "10.0.5.0/24",
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"SubnetPrivateD": ec2_subnet_template(**{
                "availabilityzone": "us-east-1d",
                "cdir": "10.0.6.0/24",
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"PublicSG": ec2_sg_template(**{
                "groupname": BASE_NAME+"PublicSG",
                "description": BASE_NAME+" Public Security Group.",
                "inboundrules": [
                    {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : 80,
                        "IpProtocol" : "tcp",
                        "ToPort" : 80
                    },
                    {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : 443,
                        "IpProtocol" : "tcp",
                        "ToPort" : 443
                    }
                ],
                "outboundrules": [
                     {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : -1,
                        "IpProtocol" : "-1",
                        "ToPort" : -1
                    }
                ],
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"PrivateNeoSG": ec2_sg_template(**{
                "groupname": BASE_NAME+"PrivateNeoSG",
                "description": BASE_NAME+" Private Security Group for Neo4j DB.",
                "inboundrules": [
                    {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : 6362,
                        "IpProtocol" : "tcp",
                        "ToPort" : 6372
                    },
                    {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : 7474,
                        "IpProtocol" : "tcp",
                        "ToPort" : 7474
                    },
                    {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : 7473,
                        "IpProtocol" : "tcp",
                        "ToPort" : 7473
                    },
                    {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : 7687,
                        "IpProtocol" : "tcp",
                        "ToPort" : 7687
                    }
                ],
                "outboundrules": [
                    {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : -1,
                        "IpProtocol" : "-1",
                        "ToPort" : -1
                    }
                ],
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"PrivateUserDBSG": ec2_sg_template(**{
                "groupname": BASE_NAME+"PrivateUserDBSG",
                "description": BASE_NAME+" EC2 Private Security Group for RDS User DB.",
                "inboundrules": [
                    {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : 5432,
                        "IpProtocol" : "tcp",
                        "ToPort" : 5432
                    }
                ],
                "outboundrules": [
                    {
                        "CidrIp" : "0.0.0.0/0",
                        "FromPort" : -1,
                        "IpProtocol" : "-1",
                        "ToPort" : -1
                    }
                ],
                "vpcid": {"Ref": BASE_NAME+"VPC"}
            }),
            BASE_NAME+"HostedZone": route53_hostedzone_template(**{
                "dnsname": BASE_URL
            }),
            BASE_NAME+"FrontendRecordSet": route53_recordset_template(**{
                "hostedzoneid": {"Ref": BASE_NAME+"HostedZone"},
                "name": BASE_URL,
                "dnstype": "A",
                "outhostedzoneid": {"Fn::FindInMap" : [ "RegionMap", { "Ref" : "AWS::Region" }, "S3hostedzoneID"]},
                "dnsname": {"Fn::FindInMap" : [ "RegionMap", { "Ref" : "AWS::Region" }, "websiteendpoint"]}
            }),
            BASE_NAME+"BackendRecordSet": route53_recordset_template(**{
                "dnsname": {"Fn::GetAtt": [BASE_NAME+"BackendELB", "DNSName"]},
                "outhostedzoneid": "Z35SXDOTRQ7X7K",
                "hostedzoneid": {"Ref": BASE_NAME+"HostedZone"},
                "name": "api."+BASE_URL,
                "dnstype": "A"
            }),
            BASE_NAME+"PhotoRecordSet": route53_recordset_template(**{
                "hostedzoneid": {"Ref": BASE_NAME+"HostedZone"},
                "name": "photo."+BASE_URL,
                "dnstype": "A",
                "outhostedzoneid": {"Fn::FindInMap" : [ "RegionMap", { "Ref" : "AWS::Region" }, "S3hostedzoneID"]},
                "dnsname": {"Fn::FindInMap" : [ "RegionMap", { "Ref" : "AWS::Region" }, "websiteendpoint"]}
            }),
            BASE_NAME+"UserDBRecordSet": route53_recordset_template(**{
                "hostedzoneid": {"Ref": BASE_NAME+"HostedZone"},
                "name": "user."+BASE_URL,
                "dnstype": "CNAME",
                "records": [
                    {"Fn::GetAtt": [BASE_NAME+"UserDB", "Endpoint.Address"]}
                ],
                "ttl": "900"
            }),
            BASE_NAME+"Neo4jRecordSet": route53_recordset_template(**{
                "hostedzoneid": {"Ref": BASE_NAME+"HostedZone"},
                "name": "graph."+BASE_URL,
                "dnstype": "CNAME",
                "records": [
                    {"Fn::GetAtt": [BASE_NAME+"GraphDB", "PrivateDnsName"]}
                ],
                "ttl": "900"
            })
        }
    })
    template["Mappings"] = {}
    template["Mappings"]["RegionMap"] = {
        "us-east-1" : { "S3hostedzoneID" : "Z3AQBSTGFYJSTF", "websiteendpoint" : "s3-website-us-east-1.amazonaws.com" },
        "us-west-1" : { "S3hostedzoneID" : "Z2F56UZL2M1ACD", "websiteendpoint" : "s3-website-us-west-1.amazonaws.com" },
        "us-west-2" : { "S3hostedzoneID" : "Z3BJ6K6RIION7M", "websiteendpoint" : "s3-website-us-west-2.amazonaws.com" },            
        "eu-west-1" : { "S3hostedzoneID" : "Z1BKCTXD74EZPE", "websiteendpoint" : "s3-website-eu-west-1.amazonaws.com" },
        "ap-southeast-1" : { "S3hostedzoneID" : "Z3O0J2DXBE1FTB", "websiteendpoint" : "s3-website-ap-southeast-1.amazonaws.com" },
        "ap-southeast-2" : { "S3hostedzoneID" : "Z1WCIGYICN2BYD", "websiteendpoint" : "s3-website-ap-southeast-2.amazonaws.com" },
        "ap-northeast-1" : { "S3hostedzoneID" : "Z2M4EHUR26P7ZW", "websiteendpoint" : "s3-website-ap-northeast-1.amazonaws.com" },
        "sa-east-1" : { "S3hostedzoneID" : "Z31GFT0UA1I2HV", "websiteendpoint" : "s3-website-sa-east-1.amazonaws.com" }
    }
    with open("template.json", "w") as fp:
        json.dump(template, fp, indent=4)
