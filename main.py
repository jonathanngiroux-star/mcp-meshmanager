#!/usr/bin/env python3
"""MCP server for meshmanager - WireGuard Mesh Network Management"""

import json
import os
from datetime import datetime
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("mcp-meshmanager")

# Simulated mesh data
MESHES = {
    "mesh-001": {
        "id": "mesh-001",
        "name": "Team Mesh",
        "network": "10.0.0.0/24",
        "port": 51820,
        "peers": {
            "peer-001": {"name": "laptop", "public_key": "key1...", "endpoint": "1.2.3.4:51820", "allowed_ips": "10.0.0.2/32", "last_handshake": "2024-12-25T10:00:00"},
            "peer-002": {"name": "server", "public_key": "key2...", "endpoint": "5.6.7.8:51820", "allowed_ips": "10.0.0.3/32", "last_handshake": "2024-12-25T09:55:00"},
            "peer-003": {"name": "phone", "public_key": "key3...", "endpoint": "9.10.11.12:51820", "allowed_ips": "10.0.0.4/32", "last_handshake": "2024-12-25T09:50:00"},
        }
    },
    "mesh-002": {
        "id": "mesh-002",
        "name": "Home Mesh",
        "network": "10.1.0.0/24",
        "port": 51821,
        "peers": {
            "peer-004": {"name": "desktop", "public_key": "key4...", "endpoint": "13.14.15.16:51821", "allowed_ips": "10.1.0.2/32", "last_handshake": "2024-12-25T09:45:00"},
            "peer-005": {"name": "nas", "public_key": "key5...", "endpoint": "17.18.19.20:51821", "allowed_ips": "10.1.0.3/32", "last_handshake": "2024-12-25T09:40:00"},
        }
    }
}

app = Server("mcp-meshmanager")

TOOLS = [
    Tool(
        name="provision_peer",
        description="Provision a new peer in the mesh network",
        inputSchema={
            "type": "object",
            "properties": {
                "mesh_id": {"type": "string", "description": "Mesh network identifier"},
                "peer_name": {"type": "string", "description": "Peer name/identifier"},
                "allowed_ips": {"type": "string", "description": "Allowed IPs for this peer (CIDR)"},
                "endpoint": {"type": "string", "description": "Endpoint address:port (optional)"},
                "persistent_keepalive": {"type": "integer", "default": 25, "description": "Persistent keepalive interval"}
            },
            "required": ["mesh_id", "peer_name", "allowed_ips"]
        }
    ),
    Tool(
        name="rotate_keys",
        description="Rotate keys for a peer",
        inputSchema={
            "type": "object",
            "properties": {
                "mesh_id": {"type": "string", "description": "Mesh network identifier"},
                "peer_id": {"type": "string", "description": "Peer identifier"},
                "generate_new": {"type": "boolean", "default": true, "description": "Generate new key pair"}
            },
            "required": ["mesh_id", "peer_id"]
        }
    ),
    Tool(
        name="monitor_latency",
        description="Monitor latency between peers in the mesh",
        inputSchema={
            "type": "object",
            "properties": {
                "mesh_id": {"type": "string", "description": "Mesh network identifier"},
                "source_peer": {"type": "string", "description": "Source peer ID"},
                "target_peer": {"type": "string", "description": "Target peer ID (optional, defaults to all)"},
                "count": {"type": "integer", "default": 10, "description": "Number of pings"}
            },
            "required": ["mesh_id", "source_peer"]
        }
    ),
    Tool(
        name="get_network_status",
        description="Get overall network status for a mesh",
        inputSchema={
            "type": "object",
            "properties": {
                "mesh_id": {"type": "string", "description": "Mesh network identifier"}
            },
            "required": ["mesh_id"]
        }
    )
]

app = Server("mcp-meshmanager")

@app.list_tools()
async def list_tools():
    return TOOLS

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "provision_peer":
        mesh_id = arguments.get("mesh_id")
        peer_name = arguments.get("peer_name")
        allowed_ips = arguments.get("allowed_ips")
        endpoint = arguments.get("endpoint")
        persistent_keepalive = arguments.get("persistent_keepalive", 25)
        
        mesh = MESHES.get(mesh_id)
        if not mesh:
            return [TextContent(type="text", text=json.dumps({"error": f"Mesh not found: {mesh_id}"}))]
        
        # Generate keys (simulated)
        private_key = f"priv-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        public_key = f"pub-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        peer_id = f"peer-{len(mesh['peers']) + 1:03d}"
        peer = {
            "name": arguments.get("peer_name"),
            "public_key": public_key,
            "endpoint": arguments.get("endpoint"),
            "allowed_ips": allowed_ips,
            "persistent_keepalive": persistent_keepalive,
            "last_handshake": "never"
        }
        
        # In real implementation, would update mesh config
        result = {
            "status": "ok",
            "tool": "provision_peer",
            "mesh_id": arguments.get("mesh_id"),
            "peer_id": f"peer-{len(MESHES[arguments.get('mesh_id')]['peers']) + 1:03d}",
            "peer_name": peer_name,
            "public_key": f"pub-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "private_key": f"priv-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "allowed_ips": arguments.get("allowed_ips"),
            "endpoint": arguments.get("endpoint"),
            "persistent_keepalive": 25,
            "status": "provisioned",
            "config": f"[Interface]\nPrivateKey = <private_key>\nAddress = {arguments.get('allowed_ips')}\n\n[Peer]\nPublicKey = <server_public_key>\nEndpoint = <server_endpoint>\nAllowedIPs = {arguments.get('allowed_ips')}\nPersistentKeepalive = 25"
        }
        return [TextContent(type="text", text=json.dumps(result))]
    
    elif name == "rotate_keys":
        mesh_id = arguments.get("mesh_id")
        peer_id = arguments.get("peer_id")
        generate_new = arguments.get("generate_new", True)
        
        mesh = MESHES.get(mesh_id)
        if not mesh:
            return [TextContent(type="text", text=json.dumps({"error": f"Mesh not found: {mesh_id}"}))]
        
        peer = mesh["peers"].get(peer_id)
        if not peer:
            return [TextContent(type="text", text=json.dumps({"error": f"Peer not found: {peer_id}"}))]
        
        old_public = peer["public_key"]
        new_public = f"pub-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        new_private = f"priv-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        peer["public_key"] = new_public
        
        result = {
            "status": "ok",
            "tool": "rotate_keys",
            "mesh_id": mesh_id,
            "peer_id": peer_id,
            "old_public_key": old_public,
            "new_public_key": new_public,
            "new_private_key": new_private if generate_new else "not_generated",
            "rotated_at": datetime.now().isoformat(),
            "note": "Update all peer configs with new public key"
        }
        return [TextContent(type="text", text=json.dumps(result))]
    
    elif name == "monitor_latency":
        mesh_id = arguments.get("mesh_id")
        source_peer = arguments.get("source_peer")
        target_peer = arguments.get("target_peer")
        count = arguments.get("count", 10)
        
        mesh = MESHES.get(mesh_id)
        if not mesh:
            return [TextContent(type="text", text=json.dumps({"error": f"Mesh not found: {mesh_id}"}))]
        
        # Simulated latency measurements
        results = []
        target_peers = [target_peer] if target_peer else [p for p in mesh["peers"] if p != source_peer]
        
        import random
        for target in target_peers:
            latencies = [round(random.uniform(1.5, 45.0), 1) for _ in range(count)]
            avg_latency = sum(latencies) / len(latencies)
            results.append({
                "source": source_peer,
                "target": target,
                "count": count,
                "avg_ms": round(sum(latencies) / len(latencies), 1),
                "min_ms": min(latencies),
                "max_ms": max(latencies),
                "packet_loss": round(random.random() * 2, 1),
                "timestamp": datetime.now().isoformat()
            })
        
        result = {
            "status": "ok",
            "tool": "monitor_latency",
            "mesh_id": mesh_id,
            "source_peer": source_peer,
            "measurements": results
        }
        return [TextContent(type="text", text=json.dumps(result))]
    
    elif name == "get_network_status":
        mesh_id = arguments.get("mesh_id")
        
        mesh = MESHES.get(mesh_id)
        if not mesh:
            return [TextContent(type="text", text=json.dumps({"error": f"Mesh not found: {mesh_id}"}))]
        
        # Calculate status for each peer
        peer_status = {}
        for pid, peer in mesh["peers"].items():
            last_hs = peer.get("last_handshake", "never")
            if last_hs != "never":
                try:
                    hs_time = datetime.fromisoformat(last_hs.replace("Z", "+00:00"))
                    age = (datetime.now() - hs_time).total_seconds()
                    status = "online" if age < 180 else "stale"
                except:
                    status = "unknown"
            else:
                status = "offline"
            peer_status[pid] = {"name": peer["name"], "status": status, "last_handshake": last_hs, "endpoint": peer.get("endpoint")}
        
        online = sum(1 for s in peer_status.values() if s["status"] == "online")
        total = len(peer_status)
        
        result = {
            "status": "ok",
            "tool": "get_network_status",
            "mesh_id": mesh_id,
            "mesh_name": mesh["name"],
            "network": mesh["network"],
            "port": mesh["port"],
            "total_peers": total,
            "online_peers": online,
            "peer_status": peer_status,
            "checked_at": datetime.now().isoformat()
        }
        return [TextContent(type="text", text=json.dumps(result))]
    
    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def serve():
        reader, writer = await stdio_server()
        await app.run(reader, writer)
    
    asyncio.run(serve())