#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, Token
from cdktf_cdktf_provider_aws import AwsProvider

from imports.vpc import Vpc
from imports.eks import Eks


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, 'Aws', region='us-west-1')

        my_vpc = Vpc(self, 'aadiVpc',
                     name='aadi-vpc',
                     cidr='10.0.0.0/16',
                     azs=['us-west-1b', 'us-west-1c'],
                     private_subnets=['10.0.1.0/24', '10.0.2.0/24'],
                     public_subnets=['10.0.3.0/24','10.0.4.0/24'],
                     enable_nat_gateway=True
                     )

        my_eks = Eks(self, 'aadiEks',
                     cluster_name='aadi-eks',
                     subnets=Token().as_list(my_vpc.private_subnets_output),
                     vpc_id=Token().as_string(my_vpc.vpc_id_output),
                     manage_aws_auth=False,
                     cluster_version='1.21'
                     )


        # define resources here


app = App()
MyStack(app, "test_cdktf")

app.synth()
