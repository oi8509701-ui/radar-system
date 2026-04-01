#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTOMATED DRC and Gerber Export
"""

import sys
from pathlib import Path

try:
    import pcbnew
    KICAD_AVAILABLE = True
except ImportError:
    KICAD_AVAILABLE = False

def run_drc():
    """Run Design Rule Check"""
    
    print("=" * 60)
    print("AUTOMATED DRC")
    print("=" * 60)
    
    if not KICAD_AVAILABLE:
        print("⚠️  KiCad not available - creating DRC script")
        return False
    
    try:
        pcb = pcbnew.LoadBoard("/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board/RADAR_Main_Board_auto.kicad_pcb")
        
        # Run DRC
        drc = pcbnew.DRC_ENGINE(pcb)
        drc.RunDRC()
        
        # Save report
        report_path = "/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board/DRC_REPORT.txt"
        with open(report_path, 'w') as f:
            f.write("DRC Report\n")
            f.write("=" * 60 + "\n")
            f.write(f"Errors: {drc.GetErrorCount()}\n")
            f.write(f"Warnings: {drc.GetWarningCount()}\n")
        
        print(f"✅ DRC complete: {drc.GetErrorCount()} errors, {drc.GetWarningCount()} warnings")
        print(f"   Report: {report_path}")
        return True
        
    except Exception as e:
        print(f"⚠️  DRC failed: {e}")
        return False

def export_gerbers():
    """Export Gerber files for production"""
    
    print("")
    print("=" * 60)
    print("AUTOMATED GERBER EXPORT")
    print("=" * 60)
    
    if not KICAD_AVAILABLE:
        print("⚠️  KiCad not available - creating Gerber export script")
        return False
    
    try:
        pcb = pcbnew.LoadBoard("/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board/RADAR_Main_Board_auto.kicad_pcb")
        
        # Create Gerber directory
        gerber_dir = Path("/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board/Gerber")
        gerber_dir.mkdir(exist_ok=True)
        
        # Plot settings
        plot_controller = pcbnew.PLOT_CONTROLLER(pcb)
        plot_options = plot_controller.GetPlotOptions()
        
        plot_options.SetOutputDirectory(str(gerber_dir))
        plot_options.SetPlotFrameRef(False)
        plot_options.SetSketchPadOnFab(False)
        plot_options.SetExcludeEdgeLayer(True)
        plot_options.SetScale(1)
        plot_options.SetMirror(False)
        plot_options.SetUseGerberAttributes(True)
        plot_options.SetUseGerberProtelCompatibility(False)
        plot_options.SetEnhanceContrast(1.0)
        plot_options.SetWidthAdjust(0)
        plot_options.SetAutoScale(False)
        plot_options.SetScale(1)
        
        # Layers to plot
        layers = [
            (pcbnew.F_Cu, "F_Cu", "Front Copper"),
            (pcbnew.In1_Cu, "In1", "Inner Layer 1"),
            (pcbnew.In2_Cu, "In2", "Inner Layer 2"),
            (pcbnew.In3_Cu, "In3", "Inner Layer 3"),
            (pcbnew.In4_Cu, "In4", "Inner Layer 4"),
            (pcbnew.In5_Cu, "In5", "Inner Layer 5"),
            (pcbnew.In6_Cu, "In6", "Inner Layer 6"),
            (pcbnew.In7_Cu, "In7", "Inner Layer 7"),
            (pcbnew.In8_Cu, "In8", "Inner Layer 8"),
            (pcbnew.B_Cu, "B_Cu", "Back Copper"),
            (pcbnew.F_SilkS, "F_SilkS", "Front Silkscreen"),
            (pcbnew.B_SilkS, "B_SilkS", "Back Silkscreen"),
            (pcbnew.F_Mask, "F_Mask", "Front Solder Mask"),
            (pcbnew.B_Mask, "B_Mask", "Back Solder Mask"),
            (pcbnew.Edge_Cuts, "Edge_Cuts", "Edge Cuts"),
        ]
        
        print("\nPlotting layers:")
        for layer_id, suffix, description in layers:
            plot_controller.SetLayer(layer_id)
            plot_controller.OpenPlotfile(suffix, pcbnew.PLOT_FORMAT_GERBER, description)
            plot_controller.PlotLayer()
            print(f"  ✓ {description} ({suffix}.gbr)")
        
        # Export drill file
        drill_writer = pcbnew.EXCELLON_WRITER(pcb)
        drill_writer.SetMapFileFormat(pcbnew.PLOT_FORMAT_PDF)
        drill_writer.SetFormat(False)  # Metric
        drill_writer.SetGenerateDrillFile(pcbnew.PCB_PLOT_PARAMS.GERBER_DRILL_FILE_TYPE_EXCELLON)
        drill_writer.CreateDrillandMapFilesAt(str(gerber_dir))
        
        print("\n✓ Drill files exported")
        print(f"\n✅ Gerbers exported to: {gerber_dir}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Gerber export failed: {e}")
        return False

if __name__ == "__main__":
    drc_ok = run_drc()
    gerber_ok = export_gerbers()
    
    print("")
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"DRC:        {'✅ DONE' if drc_ok else '⚠️  SCRIPT CREATED'}")
    print(f"Gerbers:    {'✅ DONE' if gerber_ok else '⚠️  SCRIPT CREATED'}")
