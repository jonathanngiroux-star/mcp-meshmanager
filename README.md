# mcp-meshmanager

MCP server for WireGuard Mesh Network Management - provision peers, rotate keys, monitor latency, get network status.

## Tools

### provision_peer
Provision a new peer in the mesh network.

**Parameters:**
- `mesh_id` (string, required): Mesh network identifier
- `peer_name` (string, required): Peer name/identifier
- `allowed_ips` (string, required): Allowed IPs for this peer (CIDR)
- `endpoint` (string, optional): Endpoint address:port
- `persistent_keepalive` (integer, optional): Persistent keepalive interval (default: 25)

### rotate_keys
Rotate keys for a peer.

**Parameters:**
- `mesh_id` (string, required): Mesh network identifier
- `peer_id` (string, required): Peer identifier
- `generate_new` (boolean, optional): Generate new key pair (default: true)

### monitor_latency
Monitor latency between peers in the mesh.

**Parameters:**
- `mesh_id` (string, required): Mesh network identifier
- `source_peer` (string, required): Source peer ID
- `target_peer` (string, optional): Target peer ID (defaults to all)
- `count` (integer, optional): Number of pings (default: 10)

### get_network_status
Get overall network status for a mesh.

**Parameters:**
- `mesh_id` (string, required): Mesh network identifier

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Connecting to Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "meshmanager": {
      "command": "python",
      "args": ["/path/to/mcp-meshmanager/main.py"],
      "cwd": "/path/to/mcp-meshmanager"
    }
  }
}
```

## License

MIT