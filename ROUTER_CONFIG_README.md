# Router Configuration Gatherer with Scrapli

A Python tool for connecting to network routers and gathering their configurations using the scrapli library.

## Features

- Connect to multiple router platforms (Cisco IOS-XE, NX-OS, Arista EOS, Juniper JunOS)
- Retrieve and save router configurations automatically
- Support for batch processing multiple routers
- Save configurations with timestamps
- JSON metadata for each configuration backup
- Comprehensive error handling and logging

## Supported Platforms

- Cisco IOS-XE
- Cisco IOS-XR
- Cisco NX-OS
- Arista EOS
- Juniper JunOS

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

1. Edit `router_inventory.json` with your router details:

```json
{
  "routers": [
    {
      "host": "192.168.1.1",
      "username": "admin",
      "password": "your_password",
      "platform": "cisco_iosxe",
      "port": 22,
      "auth_strict_key": false
    }
  ]
}
```

2. Run the script:

```bash
python router_config_gather.py
```

### Using in Your Code

```python
from router_config_gather import RouterConfigGatherer, RouterCredentials

# Define router credentials
router = RouterCredentials(
    host='192.168.1.1',
    username='admin',
    password='cisco123',
    platform='cisco_iosxe'
)

# Create gatherer and connect
gatherer = RouterConfigGatherer(output_dir='router_configs')
result = gatherer.connect_and_gather(router)

print(f"Configuration gathered from {result['hostname']}")
```

### Gathering from Multiple Routers

```python
from router_config_gather import RouterConfigGatherer, RouterCredentials

routers = [
    RouterCredentials(host='192.168.1.1', username='admin',
                     password='pass1', platform='cisco_iosxe'),
    RouterCredentials(host='192.168.1.2', username='admin',
                     password='pass2', platform='cisco_nxos'),
    RouterCredentials(host='192.168.1.3', username='admin',
                     password='pass3', platform='arista_eos'),
]

gatherer = RouterConfigGatherer(output_dir='configs')
results = gatherer.gather_multiple_routers(routers)
```

### Loading Credentials from JSON

```python
import json
from router_config_gather import RouterConfigGatherer, RouterCredentials

# Load router inventory from JSON file
with open('router_inventory.json', 'r') as f:
    config = json.load(f)

# Convert to RouterCredentials objects
routers = [RouterCredentials(**r) for r in config['routers']]

# Gather configurations
gatherer = RouterConfigGatherer()
results = gatherer.gather_multiple_routers(routers)
```

## Output Files

The tool saves two files for each router:

1. **Configuration file**: `hostname_YYYYMMDD_HHMMSS.txt`
   - Contains the full running configuration

2. **Metadata file**: `hostname_YYYYMMDD_HHMMSS_metadata.json`
   - Contains router information and backup details

Example metadata:
```json
{
  "hostname": "router01",
  "ip_address": "192.168.1.1",
  "platform": "cisco_iosxe",
  "timestamp": "2025-11-03T10:30:45.123456",
  "config_file": "router01_20251103_103045.txt"
}
```

## Platform-Specific Commands

The tool automatically uses the appropriate command for each platform:

| Platform | Command |
|----------|---------|
| Cisco IOS-XE | `show running-config` |
| Cisco IOS-XR | `show running-config` |
| Cisco NX-OS | `show running-config` |
| Arista EOS | `show running-config` |
| Juniper JunOS | `show configuration` |

## Examples

See `example_usage.py` for comprehensive examples including:
- Single router configuration gathering
- Multiple router batch processing
- Custom output directories
- Loading credentials from JSON files

## Error Handling

The tool includes comprehensive error handling:
- Connection failures are logged but don't stop batch processing
- Failed routers are reported in the results with error details
- All operations are logged for troubleshooting

## Logging

Logging is configured to show:
- Connection attempts
- Successful/failed operations
- File save locations
- Error messages with details

Log level can be adjusted in the script:
```python
logging.basicConfig(level=logging.DEBUG)  # For verbose output
```

## Security Notes

- Store credentials securely (consider using environment variables or a secrets manager)
- Use `auth_strict_key=False` only in lab environments
- Keep configuration backups secure as they contain sensitive information
- Consider using SSH key authentication instead of passwords

## Requirements

- Python 3.7+
- scrapli >= 2023.1.30
- Network connectivity to target routers
- SSH access to routers

## Troubleshooting

### SSH Connection Issues
- Verify network connectivity: `ping <router_ip>`
- Check SSH is enabled on the router
- Verify credentials are correct
- Check firewall rules

### Authentication Errors
- Confirm username and password
- Check if AAA is configured correctly on the router
- Try with `auth_strict_key=True` if using known SSH keys

### Platform Not Supported
- Check the platform name matches one of: `cisco_iosxe`, `cisco_nxos`, `arista_eos`, `juniper_junos`, `cisco_iosxr`
- Platform names are case-sensitive

## Contributing

Feel free to submit issues or pull requests for improvements!

## Author

Created by @nikhilpatil030
