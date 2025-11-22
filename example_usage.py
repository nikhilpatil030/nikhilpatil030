#!/usr/bin/env python3
"""
Example usage of the Router Config Gatherer

This script demonstrates different ways to use the RouterConfigGatherer
to connect to routers and retrieve their configurations.
"""

from router_config_gather import RouterConfigGatherer, RouterCredentials
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_single_router():
    """
    Example: Connect to a single router and gather its configuration
    """
    logger.info("Example 1: Single Router Configuration Gathering")
    logger.info("-" * 50)

    # Define router credentials
    router = RouterCredentials(
        host='192.168.1.1',
        username='admin',
        password='cisco123',
        platform='cisco_iosxe',
        port=22,
        auth_strict_key=False
    )

    # Create gatherer instance
    gatherer = RouterConfigGatherer(output_dir='configs')

    try:
        # Connect and gather configuration
        result = gatherer.connect_and_gather(router)
        logger.info(f"Successfully gathered config from {result['hostname']}")
        logger.info(f"Config length: {len(result['config'])} characters")
    except Exception as e:
        logger.error(f"Failed: {e}")


def example_multiple_routers():
    """
    Example: Connect to multiple routers and gather their configurations
    """
    logger.info("\nExample 2: Multiple Routers Configuration Gathering")
    logger.info("-" * 50)

    # Define multiple routers
    routers = [
        RouterCredentials(
            host='192.168.1.1',
            username='admin',
            password='cisco123',
            platform='cisco_iosxe'
        ),
        RouterCredentials(
            host='192.168.1.2',
            username='admin',
            password='cisco123',
            platform='cisco_nxos'
        ),
        RouterCredentials(
            host='192.168.1.3',
            username='admin',
            password='arista123',
            platform='arista_eos'
        ),
    ]

    # Create gatherer instance
    gatherer = RouterConfigGatherer(output_dir='configs')

    # Gather all configurations
    results = gatherer.gather_multiple_routers(routers)

    # Display results
    for result in results:
        if 'error' not in result:
            logger.info(f"Success: {result['hostname']} ({result['ip_address']})")
        else:
            logger.error(f"Failed: {result['ip_address']} - {result['error']}")


def example_with_custom_output_dir():
    """
    Example: Specify a custom output directory for saved configurations
    """
    logger.info("\nExample 3: Custom Output Directory")
    logger.info("-" * 50)

    router = RouterCredentials(
        host='10.0.0.1',
        username='netadmin',
        password='secure_password',
        platform='juniper_junos'
    )

    # Use custom output directory
    gatherer = RouterConfigGatherer(output_dir='backup_configs/juniper')

    try:
        result = gatherer.connect_and_gather(router)
        logger.info(f"Config saved to: backup_configs/juniper/")
    except Exception as e:
        logger.error(f"Failed: {e}")


def example_load_from_json():
    """
    Example: Load router credentials from a JSON configuration file
    """
    import json
    from pathlib import Path

    logger.info("\nExample 4: Load Credentials from JSON File")
    logger.info("-" * 50)

    # Example JSON structure
    config_data = {
        "routers": [
            {
                "host": "192.168.1.1",
                "username": "admin",
                "password": "cisco123",
                "platform": "cisco_iosxe",
                "port": 22
            },
            {
                "host": "192.168.1.2",
                "username": "admin",
                "password": "cisco123",
                "platform": "cisco_nxos",
                "port": 22
            }
        ]
    }

    # In practice, you would load this from a file:
    # with open('router_config.json', 'r') as f:
    #     config_data = json.load(f)

    # Convert to RouterCredentials objects
    routers = [
        RouterCredentials(**router_config)
        for router_config in config_data['routers']
    ]

    # Gather configurations
    gatherer = RouterConfigGatherer()
    results = gatherer.gather_multiple_routers(routers)

    logger.info(f"Processed {len(results)} routers")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Router Configuration Gatherer - Usage Examples")
    print("="*60)

    # NOTE: These examples will fail without actual routers
    # Uncomment the examples you want to try:

    # example_single_router()
    # example_multiple_routers()
    # example_with_custom_output_dir()
    # example_load_from_json()

    print("\n" + "="*60)
    print("To use these examples:")
    print("1. Update the IP addresses, usernames, and passwords")
    print("2. Uncomment the example you want to run")
    print("3. Run: python example_usage.py")
    print("="*60)
