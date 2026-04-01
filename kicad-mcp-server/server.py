#!/usr/bin/env python3
"""
MCP Server для работы с KiCad / PLFM_RADAR проектом
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import re

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import sexpdata

# Создаём экземпляр сервера
server = Server("kicad-mcp-server")

# Путь к проекту PLFM_RADAR
PLFM_RADAR_ROOT = "/Users/mac/PLFM_RADAR_NEWS"


def parse_kicad_pcb(pcb_path: str) -> Dict[str, Any]:
    """
    Парсит KiCad PCB файл и возвращает информацию
    """
    try:
        with open(pcb_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Извлекаем базовую информацию
        info = {
            "success": True,
            "path": pcb_path,
            "layers": [],
            "footprints": [],
            "tracks": 0,
            "vias": 0,
            "dimensions": {}
        }
        
        # Парсим слои
        layer_matches = re.findall(r'\(layer\s+"([^"]+)"\s+(\w+)', content)
        info["layers"] = [{"name": m[0], "type": m[1]} for m in layer_matches[:20]]
        
        # Парсим футпринты
        fp_matches = re.findall(r'\(footprint\s+"([^"]+)"\s+\(at\s+([-\d.]+)\s+([-\d.]+)\)', content)
        info["footprints"] = [
            {"footprint": m[0], "x": float(m[1]), "y": float(m[2])}
            for m in fp_matches[:50]
        ]
        
        # Считаем треки
        info["tracks"] = len(re.findall(r'\(segment\s+\(start', content))
        
        # Считаем via
        info["vias"] = len(re.findall(r'\(via\s+\(at', content))
        
        # Извлекаем размеры платы
        edge_matches = re.findall(r'\(gr_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\)', content)
        if edge_matches:
            coords = [(float(m[0]), float(m[1])) for m in edge_matches] + [(float(m[2]), float(m[3])) for m in edge_matches]
            x_vals = [c[0] for c in coords]
            y_vals = [c[1] for c in coords]
            info["dimensions"] = {
                "width": max(x_vals) - min(x_vals),
                "height": max(y_vals) - min(y_vals),
                "min_x": min(x_vals),
                "min_y": min(y_vals)
            }
        
        return info
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def parse_kicad_sch(sch_path: str) -> Dict[str, Any]:
    """
    Парсит KiCad схему и возвращает компоненты
    """
    try:
        with open(sch_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        components = []
        
        # Парсим символы (компоненты)
        symbol_pattern = r'\(symbol\s+\(lib_id\s+"([^"]+)"\)\s+\(at\s+([-\d.]+)\s+([-\d.]+)\).*?\(property\s+"Reference"\s+"([^"]+)"\).*?\(property\s+"Value"\s+"([^"]+)"\)'
        
        for match in re.finditer(symbol_pattern, content, re.DOTALL):
            components.append({
                "lib_id": match.group(1),
                "x": float(match.group(2)),
                "y": float(match.group(3)),
                "reference": match.group(4),
                "value": match.group(5)
            })
        
        return {
            "success": True,
            "path": sch_path,
            "components": components,
            "total_count": len(components)
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_gerber_files(project_dir: str) -> Dict[str, Any]:
    """
    Список Gerber файлов в проекте
    """
    try:
        gerber_dir = Path(project_dir) / "Production" / "Gerber"
        if not gerber_dir.exists():
            gerber_dir = Path(project_dir) / "Gerber"
        
        if not gerber_dir.exists():
            return {"success": False, "error": f"Gerber directory not found: {project_dir}"}
        
        gerber_files = []
        for f in gerber_dir.glob("*.g*"):
            gerber_files.append({
                "name": f.name,
                "path": str(f),
                "size": f.stat().st_size
            })
        
        return {
            "success": True,
            "directory": str(gerber_dir),
            "files": gerber_files,
            "count": len(gerber_files)
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_project_structure(root_path: str = PLFM_RADAR_ROOT) -> Dict[str, Any]:
    """
    Получает структуру проекта PLFM_RADAR
    """
    try:
        structure = {
            "root": root_path,
            "boards": []
        }
        
        board_dirs = [
            "MainBoard",
            "PowerBoard",
            "PowerAmplifierBoard",
            "FrequencySynthesizerBoard"
        ]
        
        for board_dir in board_dirs:
            board_path = Path(root_path) / board_dir
            if board_path.exists():
                board_info = {
                    "name": board_dir,
                    "path": str(board_path),
                    "schematic": None,
                    "pcb": None,
                    "gerber_count": 0
                }
                
                # Ищем файлы
                for f in board_path.glob("*.kicad_sch"):
                    board_info["schematic"] = str(f)
                for f in board_path.glob("*.kicad_pcb"):
                    board_info["pcb"] = str(f)
                
                # Считаем Gerber
                gerber_path = board_path / "Production" / "Gerber"
                if gerber_path.exists():
                    board_info["gerber_count"] = len(list(gerber_path.glob("*.g*")))
                
                structure["boards"].append(board_info)
        
        return structure
    
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Список всех доступных инструментов MCP
    """
    return [
        types.Tool(
            name="list_project_boards",
            description="List all PCB boards in the PLFM_RADAR project",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="parse_pcb",
            description="Parse KiCad PCB file and get information about layers, footprints, tracks",
            inputSchema={
                "type": "object",
                "properties": {
                    "pcb_path": {
                        "type": "string",
                        "description": "Path to the .kicad_pcb file"
                    }
                },
                "required": ["pcb_path"]
            }
        ),
        types.Tool(
            name="parse_schematic",
            description="Parse KiCad schematic file and list all components",
            inputSchema={
                "type": "object",
                "properties": {
                    "sch_path": {
                        "type": "string",
                        "description": "Path to the .kicad_sch file"
                    }
                },
                "required": ["sch_path"]
            }
        ),
        types.Tool(
            name="list_gerber",
            description="List all Gerber files for a PCB project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_dir": {
                        "type": "string",
                        "description": "Path to the board directory (e.g., MainBoard/)"
                    }
                },
                "required": ["project_dir"]
            }
        ),
        types.Tool(
            name="get_board_info",
            description="Get detailed information about a specific board",
            inputSchema={
                "type": "object",
                "properties": {
                    "board_name": {
                        "type": "string",
                        "description": "Board name (MainBoard, PowerBoard, etc.)"
                    }
                },
                "required": ["board_name"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, 
    arguments: Optional[Dict[str, Any]] = None
) -> list[types.TextContent]:
    """
    Обрабатывает вызовы инструментов
    """
    
    if name == "list_project_boards":
        result = get_project_structure()
        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
    
    elif name == "parse_pcb":
        pcb_path = arguments.get("pcb_path")
        result = parse_kicad_pcb(pcb_path)
        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
    
    elif name == "parse_schematic":
        sch_path = arguments.get("sch_path")
        result = parse_kicad_sch(sch_path)
        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
    
    elif name == "list_gerber":
        project_dir = arguments.get("project_dir")
        result = list_gerber_files(project_dir)
        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
    
    elif name == "get_board_info":
        board_name = arguments.get("board_name")
        board_path = Path(PLFM_RADAR_ROOT) / board_name
        
        if not board_path.exists():
            return [types.TextContent(
                type="text",
                text=f"Board not found: {board_name}"
            )]
        
        # Получаем информацию о PCB
        pcb_info = None
        for pcb in board_path.glob("*.kicad_pcb"):
            pcb_info = parse_kicad_pcb(str(pcb))
            break
        
        # Получаем информацию о схеме
        sch_info = None
        for sch in board_path.glob("*.kicad_sch"):
            sch_info = parse_kicad_sch(str(sch))
            break
        
        # Считаем Gerber
        gerber_count = 0
        gerber_path = board_path / "Production" / "Gerber"
        if gerber_path.exists():
            gerber_count = len(list(gerber_path.glob("*.g*")))
        
        info = {
            "board": board_name,
            "path": str(board_path),
            "pcb_info": pcb_info,
            "schematic_info": sch_info,
            "gerber_count": gerber_count
        }
        
        return [types.TextContent(
            type="text",
            text=json.dumps(info, indent=2, ensure_ascii=False)
        )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """
    Запускает MCP сервер
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="kicad-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
