import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("app-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": "my-vpc"
    }
)

# Create an Internet Gateway
igw = aws.ec2.InternetGateway("app-igw",
    vpc_id=vpc.id,
    tags={
        "Name": "my-internet-gateway"
    }
)

# Create a public subnet
subnet = aws.ec2.Subnet("app-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="ap-southeast-1a",
    map_public_ip_on_launch=True,
    tags={
        "Name": "my-public-subnet"
    }
)

# Create a Route Table
route_table = aws.ec2.RouteTable("app-route-table",
    vpc_id=vpc.id,
    tags={
        "Name": "my-route-table"
    }
)



# Create a route to the Internet Gateway
route = aws.ec2.Route("app-route",
    route_table_id=route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw.id,
)

# Associate the Route Table with the subnet
route_table_association = aws.ec2.RouteTableAssociation("app-route-table-assoc",
    subnet_id=subnet.id,
    route_table_id=route_table.id
)

# Create security groups
# Define a security group for SSH access (optional, but you can use web-sg/worker-sg for SSH as shown)
# If you want a dedicated SSH security group, you can add:

ssh_sg = aws.ec2.SecurityGroup("ssh-sg",
    vpc_id=vpc.id,
    description="Allow SSH access",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]  # Restrict to your IP in production
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ]
)
rabbitmq_sg = aws.ec2.SecurityGroup("rabbitmq-sg",
    vpc_id=vpc.id,
    description="Allow RabbitMQ traffic",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=5672,
            to_port=5672,
            cidr_blocks=["10.0.0.0/16"]
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=15672,
            to_port=15672,
            cidr_blocks=["10.0.0.0/16"]
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ]
)

redis_sg = aws.ec2.SecurityGroup("redis-sg",
    vpc_id=vpc.id,
    description="Allow Redis traffic",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=6379,
            to_port=6379,
            cidr_blocks=["10.0.0.0/16"]
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ]
)

web_sg = aws.ec2.SecurityGroup("web-sg",
    vpc_id=vpc.id,
    description="Allow web traffic",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=5000,
            to_port=5000,
            cidr_blocks=["0.0.0.0/0"]
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]  # Restrict to your IP in production
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ]
)

worker_sg = aws.ec2.SecurityGroup("worker-sg",
    vpc_id=vpc.id,
    description="Allow worker traffic",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]  # Restrict to your IP in production
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ]
)

flower_sg = aws.ec2.SecurityGroup("flower-sg",
    vpc_id=vpc.id,
    description="Allow Flower traffic",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=5555,
            to_port=5555,
            cidr_blocks=["0.0.0.0/0"]
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]  # Restrict to your IP in production
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ]
)

# Create an EC2 key pair
key_pair = aws.ec2.KeyPair("app-key-pair",
    key_name="app-key-pair",
    public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC89NY9kgeAjvNUi0oNKSHBkvFjz3O3JFhAV5ByBhgNwKhYpJyxjoaydzdlDhvh/31+TRDOnf0pcxuV+h2SIkESZjkhngpghl11+imnzZUIXvYPAT3DpbqeCMb7XypurQxUZIxBc5G57nNe+oLDRLoLjAsnZtJFN7YJvtLsKkxfhDpI7WtjGU4rl/V5ejFs4WyPJuj2MEeObGTlFqr1lgeIPuE8a95LnLleEVJQ541tetzgPSaSGnenYlMH8dJpEspQGLhVyFoutonOWIdGukkU1A+M7e4y8Wg1fiJ5B5S9gydMmCFHAueKQy3vTH0HmzjDYNX4VoE9k1b4L2OGg+nB shaan@DESKTOP-RN29TTL"  # Replace with your public key
)


# Get the latest Ubuntu 22.04 LTS AMI
ubuntu_ami = aws.ec2.get_ami(
    most_recent=True,
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
        ),
        aws.ec2.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"]
        )
    ],
    owners=["099720109477"]  # Canonical's AWS account ID
)

# User data script for Ubuntu
user_data = """#!/bin/bash
set -ex
apt-get update -y
apt-get install -y docker.io git
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
/usr/local/bin/docker-compose up -d
"""


# Create EC2 instances
rabbitmq_instance = aws.ec2.Instance("rabbitmq-instance",
    instance_type="t2.micro",
    ami=ubuntu_ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[rabbitmq_sg.id],
    key_name=key_pair.key_name,
    user_data=user_data,
    associate_public_ip_address=True,
    tags={"Name": "rabbitmq-instance"}
)

redis_instance = aws.ec2.Instance("redis-instance",
    instance_type="t2.micro",
    ami=ubuntu_ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[redis_sg.id],
    key_name=key_pair.key_name,
    user_data=user_data,
    associate_public_ip_address=True,
    tags={"Name": "redis-instance"}
)

web_instance = aws.ec2.Instance("web-instance",
    instance_type="t2.micro",
    ami=ubuntu_ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[web_sg.id],
    key_name=key_pair.key_name,
    user_data=user_data,
    associate_public_ip_address=True,
    tags={"Name": "web-instance"}
)

default_worker_instance = aws.ec2.Instance("default-worker-instance",
    instance_type="t2.micro",
    ami=ubuntu_ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[worker_sg.id],
    key_name=key_pair.key_name,
    user_data=user_data,
    associate_public_ip_address=True,
    tags={"Name": "default-worker-instance"}
)

data_worker_instance = aws.ec2.Instance("data-worker-instance",
    instance_type="t2.micro",
    ami=ubuntu_ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[worker_sg.id],
    key_name=key_pair.key_name,
    user_data=user_data,
    associate_public_ip_address=True,
    tags={"Name": "data-worker-instance"}
)

email_worker_instance = aws.ec2.Instance("email-worker-instance",
    instance_type="t2.micro",
    ami=ubuntu_ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[worker_sg.id],
    key_name=key_pair.key_name,
    user_data=user_data,
    associate_public_ip_address=True,
    tags={"Name": "email-worker-instance"}
)

file_worker_instance = aws.ec2.Instance("file-worker-instance",
    instance_type="t2.micro",
    ami=ubuntu_ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[worker_sg.id],
    key_name=key_pair.key_name,
    user_data=user_data,
    associate_public_ip_address=True,
    tags={"Name": "file-worker-instance"}
)

flower_instance = aws.ec2.Instance("flower-instance",
    instance_type="t2.micro",
    ami=ubuntu_ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[flower_sg.id],
    key_name=key_pair.key_name,
    user_data=user_data,
    associate_public_ip_address=True,
    tags={"Name": "flower-instance"}
)

# Export instance IPs and key pair name
pulumi.export("key_pair_name", key_pair.key_name)
pulumi.export("rabbitmq_private_ip", rabbitmq_instance.private_ip)
pulumi.export("redis_private_ip", redis_instance.private_ip)
pulumi.export("web_public_ip", web_instance.public_ip)
pulumi.export("flower_public_ip", flower_instance.public_ip)
pulumi.export("ubuntuAmiId", ubuntu_ami.id)

