#!/usr/bin/env python3
"""
Scrapli Router Configuration Gatherer

This script connects to network routers using the scrapli library and
retrieves their running configuration.

Supports multiple platforms:
- Cisco IOS
- Cisco IOS-XE
- Cisco NX-OS
- Arista EOS
- Juniper JunOS
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

from scrapli.driver.core import (
    IOSXEDriver,
    IOSXRDriver,
    NXOSDriver,
    EOSDriver,
    JunosDriver,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class RouterCredentials:
    """Router connection credentials"""
    host: str
    username: str
    password: str
    platform: str  # 'cisco_iosxe', 'cisco_nxos', 'arista_eos', 'juniper_junos'
    port: int = 22
    auth_strict_key: bool = False


class RouterConfigGatherer:
    """
    A class to connect to routers and gather their configuration
    using the scrapli library.
    """

    # Map platform names to scrapli drivers
    PLATFORM_DRIVERS = {
        'cisco_iosxe': IOSXEDriver,
        'cisco_iosxr': IOSXRDriver,
        'cisco_nxos': NXOSDriver,
        'arista_eos': EOSDriver,
        'juniper_junos': JunosDriver,
    }

    # Map platforms to their show running-config commands
    CONFIG_COMMANDS = {
        'cisco_iosxe': 'show running-config',
        'cisco_iosxr': 'show running-config',
        'cisco_nxos': 'show running-config',
        'arista_eos': 'show running-config',
        'juniper_junos': 'show configuration',
    }

    def __init__(self, output_dir: str = 'router_configs'):
        """
        Initialize the RouterConfigGatherer

        Args:
            output_dir: Directory to save configuration files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def connect_and_gather(self, router: RouterCredentials) -> Dict[str, str]:
        """
        Connect to a router and gather its configuration

        Args:
            router: RouterCredentials object with connection details

        Returns:
            Dictionary containing hostname, config, and timestamp
        """
        logger.info(f"Connecting to {router.host} ({router.platform})...")

        try:
            # Get the appropriate driver for the platform
            driver_class = self.PLATFORM_DRIVERS.get(router.platform)
            if not driver_class:
                raise ValueError(f"Unsupported platform: {router.platform}")

            # Create connection parameters
            connection_params = {
                'host': router.host,
                'auth_username': router.username,
                'auth_password': router.password,
                'port': router.port,
                'auth_strict_key': router.auth_strict_key,
                'timeout_socket': 30,
                'timeout_transport': 30,
            }

            # Connect to the router
            with driver_class(**connection_params) as conn:
                conn.open()
                logger.info(f"Successfully connected to {router.host}")

                # Get hostname
                hostname_response = conn.send_command("show version")
                hostname = self._extract_hostname(hostname_response.result, router.platform)

                # Get configuration
                config_command = self.CONFIG_COMMANDS.get(router.platform)
                config_response = conn.send_command(config_command)

                if config_response.failed:
                    raise Exception(f"Failed to retrieve configuration: {config_response.result}")

                logger.info(f"Successfully retrieved configuration from {router.host}")

                result = {
                    'hostname': hostname,
                    'ip_address': router.host,
                    'platform': router.platform,
                    'config': config_response.result,
                    'timestamp': datetime.now().isoformat(),
                }

                # Save configuration to file
                self._save_config(result)

                return result

        except Exception as e:
            logger.error(f"Error connecting to {router.host}: {str(e)}")
            raise

    def _extract_hostname(self, version_output: str, platform: str) -> str:
        """
        Extract hostname from show version output

        Args:
            version_output: Output from show version command
            platform: Router platform

        Returns:
            Hostname string
        """
        lines = version_output.split('\n')

        # Try to find hostname in output
        for line in lines:
            if 'hostname' in line.lower():
                parts = line.split()
                if len(parts) >= 2:
                    return parts[-1]

        # If not found, return "unknown"
        return "unknown"

    def _save_config(self, config_data: Dict[str, str]) -> None:
        """
        Save configuration to a file

        Args:
            config_data: Dictionary containing config and metadata
        """
        hostname = config_data['hostname']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save the raw configuration
        config_filename = f"{hostname}_{timestamp}.txt"
        config_path = self.output_dir / config_filename

        with open(config_path, 'w') as f:
            f.write(config_data['config'])

        logger.info(f"Configuration saved to {config_path}")

        # Save metadata as JSON
        metadata_filename = f"{hostname}_{timestamp}_metadata.json"
        metadata_path = self.output_dir / metadata_filename

        metadata = {
            'hostname': config_data['hostname'],
            'ip_address': config_data['ip_address'],
            'platform': config_data['platform'],
            'timestamp': config_data['timestamp'],
            'config_file': config_filename,
        }

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Metadata saved to {metadata_path}")

    def gather_multiple_routers(self, routers: List[RouterCredentials]) -> List[Dict[str, str]]:
        """
        Connect to multiple routers and gather their configurations

        Args:
            routers: List of RouterCredentials objects

        Returns:
            List of dictionaries containing config data for each router
        """
        results = []

        for router in routers:
            try:
                result = self.connect_and_gather(router)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to gather config from {router.host}: {str(e)}")
                results.append({
                    'hostname': 'unknown',
                    'ip_address': router.host,
                    'platform': router.platform,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat(),
                })

        return results


def main():
    """
    Example usage of the RouterConfigGatherer
    """
    # Example router configurations
    routers = [
        RouterCredentials(
            host='192.168.1.1',
            username='admin',
            password='password',
            platform='cisco_iosxe'
        ),
        RouterCredentials(
            host='192.168.1.2',
            username='admin',
            password='password',
            platform='cisco_nxos'
        ),
    ]

    # Create gatherer instance
    gatherer = RouterConfigGatherer(output_dir='router_configs')

    # Gather configurations from all routers
    logger.info("Starting configuration gathering...")
    results = gatherer.gather_multiple_routers(routers)

    # Print summary
    logger.info("\n" + "="*50)
    logger.info("Configuration Gathering Summary")
    logger.info("="*50)

    successful = sum(1 for r in results if 'error' not in r)
    failed = len(results) - successful

    logger.info(f"Total routers: {len(results)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")

    for result in results:
        if 'error' in result:
            logger.info(f"❌ {result['ip_address']} - Error: {result['error']}")
        else:
            logger.info(f"✓ {result['hostname']} ({result['ip_address']})")


if __name__ == '__main__':
    main()
