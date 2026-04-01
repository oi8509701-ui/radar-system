# KiCad MCP Server for AERIS-10N Project

**MCP (Model Context Protocol) Server** for integration with AI assistants and KiCad PCB projects.

---

## 📋 Overview

This MCP server provides tools for:
- Parsing KiCad PCB (`.kicad_pcb`) and schematic (`.kicad_sch`) files
- Extracting information about layers, footprints, tracks, vias
- Listing Gerber files for production
- Getting project structure and board information

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Installation

```bash
cd /Users/mac/PLFM_RADAR_NEWS/kicad-mcp-server

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if needed)
pip install mcp>=0.9.0 sexpdata>=0.0.3
```

### Running the Server

```bash
# Start MCP server
python server.py
```

The server will start and listen for MCP protocol messages via stdio.

---

## 🛠️ Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| **list_project_boards** | List all PCB boards in the PLFM_RADAR project | — |
| **parse_pcb** | Parse KiCad PCB file and get information | `pcb_path`: path to `.kicad_pcb` |
| **parse_schematic** | Parse KiCad schematic and list components | `sch_path`: path to `.kicad_sch` |
| **list_gerber** | List all Gerber files for a PCB | `project_dir`: board directory |
| **get_board_info** | Get detailed information about a board | `board_name`: MainBoard, PowerBoard, etc. |

---

## 📖 Usage Examples

### Example 1: List All Project Boards

**Request:**
```json
{
  "name": "list_project_boards",
  "arguments": {}
}
```

**Response:**
```json
{
  "root": "/Users/mac/PLFM_RADAR_NEWS",
  "boards": [
    {
      "name": "MainBoard",
      "path": "/Users/mac/PLFM_RADAR_NEWS/MainBoard",
      "schematic": "/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board.kicad_sch",
      "pcb": "/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board.kicad_pcb",
      "gerber_count": 12
    },
    {
      "name": "PowerBoard",
      ...
    }
  ]
}
```

---

### Example 2: Parse PCB File

**Request:**
```json
{
  "name": "parse_pcb",
  "arguments": {
    "pcb_path": "/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board.kicad_pcb"
  }
}
```

**Response:**
```json
{
  "success": true,
  "path": "/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board.kicad_pcb",
  "layers": [
    {"name": "F.Cu", "type": "signal"},
    {"name": "B.Cu", "type": "signal"},
    ...
  ],
  "footprints": [
    {"footprint": "XC7A50T-2FTG256", "x": 100.5, "y": 200.3},
    ...
  ],
  "tracks": 1234,
  "vias": 567,
  "dimensions": {
    "width": 150.5,
    "height": 100.2,
    "min_x": 0,
    "min_y": 0
  }
}
```

---

### Example 3: Get Board Information

**Request:**
```json
{
  "name": "get_board_info",
  "arguments": {
    "board_name": "MainBoard"
  }
}
```

**Response:**
```json
{
  "board": "MainBoard",
  "path": "/Users/mac/PLFM_RADAR_NEWS/MainBoard",
  "pcb_info": {...},
  "schematic_info": {...},
  "gerber_count": 12
}
```

---

### Example 4: List Gerber Files

**Request:**
```json
{
  "name": "list_gerber",
  "arguments": {
    "project_dir": "/Users/mac/PLFM_RADAR_NEWS/MainBoard"
  }
}
```

**Response:**
```json
{
  "success": true,
  "directory": "/Users/mac/PLFM_RADAR_NEWS/MainBoard/Production/Gerber",
  "files": [
    {"name": "F_Cu.gtl", "path": "...", "size": 12345},
    {"name": "B_Cu.gbl", "path": "...", "size": 10234},
    ...
  ],
  "count": 12
}
```

---

## 🔌 Integration with AI Assistants

The MCP server can be connected to AI assistants via the standard MCP protocol:

```python
# Example using MCP SDK
from mcp import Client

async with Client() as client:
    # List available tools
    tools = await client.list_tools()
    
    # Call a tool
    result = await client.call_tool(
        name="parse_pcb",
        arguments={"pcb_path": "/path/to/file.kicad_pcb"}
    )
    
    print(result)
```

---

## 📁 Project Structure

```
kicad-mcp-server/
├── server.py                    # Main MCP server
├── kicad_antenna_server.py      # MCP server for antenna generation
├── requirements.txt             # Python dependencies
├── venv/                        # Virtual environment
├── generate_*.py                # PCB generators
└── README_antenna.md            # Antenna server documentation
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **mcp** | ≥0.9.0 | MCP protocol implementation |
| **sexpdata** | ≥0.0.3 | S-expression parser (KiCad format) |

---

## 🔧 Development

### Adding New Tools

1. Add tool definition in `handle_list_tools()`:
```python
types.Tool(
    name="your_new_tool",
    description="Description of your tool",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "..."}
        },
        "required": ["param1"]
    }
)
```

2. Implement handler in `handle_call_tool()`:
```python
elif name == "your_new_tool":
    param1 = arguments.get("param1")
    result = your_function(param1)
    return [types.TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]
```

---

## 🐛 Troubleshooting

### Server doesn't start

```bash
# Check Python version
python --version  # Should be 3.9+

# Check dependencies
pip list | grep mcp
pip list | grep sexpdata

# Reinstall if needed
pip install mcp>=0.9.0 sexpdata>=0.0.3
```

### Tool returns error

- Check file paths are correct
- Ensure KiCad files are valid
- Check file permissions

---

## 📝 License

Part of the AERIS-10N open-source radar project.

---

## 🔗 Related Documentation

- [Main Project README](../README.md)
- [Antenna MCP Server](README_antenna.md)
- [QWEN.md](../QWEN.md) - Full project documentation

---

**Last Updated:** 2026-03-31  
**Version:** 0.1.0
