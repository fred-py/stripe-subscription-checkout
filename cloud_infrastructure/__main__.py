# https://www.pulumi.com/docs/concepts/config/
import pulumi
import pulumi_docker as docker
from pulumi_gcp import cloudrun, config as gcp_config
import  pulumi_gcp as gcp_config
from pulumi_gcp import artifactregistry
import pulumi_random as random
from gcloud_s_manager import get_env



# Import the program's configuration settings.
config = pulumi.Config()
app_path = config.get("appPath", "../checkout-single-subscription")
image_name = config.get("imageName", "united-app")
container_port = config.get_int("containerPort", 8080)
cpu = config.get_int("cpu", 1)
memory = config.get("memory", "1Gi")
concurrency = config.get_int("concurrency", 50)

# Import the provider's configuration settings.
gcp_config = pulumi.Config("gcp")
location = gcp_config.require("region")
project = gcp_config.require("project")

# Get the secret/env variables from gcloud
FLASK_CONFIG = get_env("stripe-checkout-424311", "FLASK_CONFIG")
STRIPE_SECRET_KEY = get_env("stripe-checkout-424311", "STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = get_env("stripe-checkout-424311", "STRIPE_PUBLISHABLE_KEY")
DOMAIN = get_env("stripe-checkout-424311", "DOMAIN")
GOLD_PRICE_ID = get_env("stripe-checkout-424311", "GOLD_PRICE_ID")
SILVER_PRICE_ID = get_env("stripe-checkout-424311", "SILVER_PRICE_ID")
ANY_COMBO_PRICE_ID = get_env("stripe-checkout-424311", "ANY_COMBO_PRICE_ID")
ONE_OFF_PRICE_ID = get_env("stripe-checkout-424311", "ONE_OFF_PRICE_ID")
FAVICON = get_env("stripe-checkout-424311", "FAVICON")
STATIC_DIR = get_env("stripe-checkout-424311", "STATIC_DIR")
UNITED_ADMIN_3 = get_env("stripe-checkout-424311", "UNITED_ADMIN_3")

DATABASE = get_env("stripe-checkout-424311", "DATABASE")
DATABASE_URL = get_env("stripe-checkout-424311", "DATABASE_URL")
HOST = get_env("stripe-checkout-424311", "HOST")
DATABASE_NAME = get_env("stripe-checkout-424311", "DATABASE_NAME")
USER = get_env("stripe-checkout-424311", "USER")
PASSWORD = get_env("stripe-checkout-424311", "PASSWORD")




# Create a unique Artifact Registry repository ID
unique_string = random.RandomString(
    "unique-string",
    length=4,
    lower=True,
    upper=False,
    numeric=True,
    special=False,
)
repo_id = pulumi.Output.concat(
    "repo-",
    unique_string.result
)

# Create an Artifact Registry repository
repository = artifactregistry.Repository(
    "repository",
    description="Repository for container image",
    format="DOCKER",
    location=location,
    repository_id=repo_id,
)

# Form the repository URL
repo_url = pulumi.Output.concat(
    location,
    "-docker.pkg.dev/",
    project,
    "/",
    repository.repository_id
)

# Create a container image for the service.
# Before running `pulumi up`, configure Docker for Artifact Registry authentication
# as described here: https://cloud.google.com/artifact-registry/docs/docker/authentication
image = docker.Image(
    "image",
    image_name=pulumi.Output.concat(repo_url, "/", image_name),
    build=docker.DockerBuildArgs(
        context=app_path,
        # Cloud Run currently requires x86_64 images
        # https://cloud.google.com/run/docs/container-contract#languages
        platform="linux/amd64"
    ),
)

# Create a Cloud Run service definition.
service = cloudrun.Service(
    "service",
    cloudrun.ServiceArgs(
        location=location,
        template=cloudrun.ServiceTemplateArgs(
            spec=cloudrun.ServiceTemplateSpecArgs(
                containers=[
                    cloudrun.ServiceTemplateSpecContainerArgs(
                        image=image.repo_digest,
                        resources=cloudrun.ServiceTemplateSpecContainerResourcesArgs(
                            limits=dict(
                                memory=memory,
                                cpu=cpu,
                            ),
                        ),
                        ports=[
                            cloudrun.ServiceTemplateSpecContainerPortArgs(
                                container_port=container_port,
                            ),
                        ],
                        envs=[
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                #name="FLASK_RUN_PORT",
                                #value=container_port,
                                name="FLASK_CONFIG",
                                value=FLASK_CONFIG,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="STRIPE_SECRET_KEY",
                                value=STRIPE_SECRET_KEY,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(    
                                name="STRIPE_PUBLISHABLE_KEY",
                                value=STRIPE_PUBLISHABLE_KEY,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="DATABASE",
                                value=DATABASE,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="DATABASE_URL",
                                value=DATABASE_URL,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="HOST",
                                value=HOST,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="DATABASE_NAME",
                                value=DATABASE_NAME,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="USER",
                                value=USER,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="PASSWORD",
                                value=PASSWORD,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="DOMAIN",
                                value=DOMAIN,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="GOLD_PRICE_ID",
                                value=GOLD_PRICE_ID,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="SILVER_PRICE_ID",
                                value=SILVER_PRICE_ID,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="ANY_COMBO_PRICE_ID",
                                value=ANY_COMBO_PRICE_ID,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(    
                                name="ONE_OFF_PRICE_ID",
                                value=ONE_OFF_PRICE_ID,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="FAVICON",
                                value=FAVICON,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="STATIC_DIR",
                                value=STATIC_DIR,
                            ),
                            cloudrun.ServiceTemplateSpecContainerEnvArgs(
                                name="UNITED_ADMIN_3",
                                value=UNITED_ADMIN_3,
                            ),
                        ],
                    ),
                ],
                container_concurrency=concurrency,
            ),
        ),
    ),
)

# Create an IAM member to make the service publicly accessible.
invoker = cloudrun.IamMember(
    "invoker",
    cloudrun.IamMemberArgs(
        location=location,
        service=service.name,
        role="roles/run.invoker",
        member="allUsers",
    ),
)

# Export the URL of the service.
pulumi.export("url", service.statuses.apply(lambda statuses: statuses[0].url if statuses else None))
