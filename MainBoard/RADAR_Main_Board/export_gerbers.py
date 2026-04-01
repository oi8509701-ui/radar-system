#!/usr/bin/env python3
import pcbnew

pcb = pcbnew.LoadBoard("/Users/mac/PLFM_RADAR_NEWS/MainBoard/RADAR_Main_Board/RADAR_Main_Board_auto.kicad_pcb")

# Create Gerber directory
from pathlib import Path
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
plot_options.SetEnhanceContrast(1.0)
plot_options.SetAutoScale(False)

# Layers
layers = [
    (pcbnew.F_Cu, "F_Cu"),
    (pcbnew.In1_Cu, "In1"),
    (pcbnew.In2_Cu, "In2"),
    (pcbnew.In3_Cu, "In3"),
    (pcbnew.In4_Cu, "In4"),
    (pcbnew.In5_Cu, "In5"),
    (pcbnew.In6_Cu, "In6"),
    (pcbnew.In7_Cu, "In7"),
    (pcbnew.In8_Cu, "In8"),
    (pcbnew.B_Cu, "B_Cu"),
    (pcbnew.F_SilkS, "F_SilkS"),
    (pcbnew.B_SilkS, "B_SilkS"),
    (pcbnew.F_Mask, "F_Mask"),
    (pcbnew.B_Mask, "B_Mask"),
    (pcbnew.Edge_Cuts, "Edge_Cuts"),
]

print("\nPlotting layers:")
for layer_id, suffix in layers:
    plot_controller.SetLayer(layer_id)
    plot_controller.OpenPlotfile(suffix, pcbnew.PLOT_FORMAT_GERBER, suffix)
    if plot_controller.PlotLayer():
        print(f"  ✓ {suffix}")

# Drill file
print("\nExporting drill file...")
drill_writer = pcbnew.EXCELLON_WRITER(pcb)
drill_writer.SetMapFileFormat(pcbnew.PLOT_FORMAT_PDF)
drill_writer.SetFormat(False)
drill_writer.SetGenerateDrillFile(pcbnew.PCB_PLOT_PARAMS.GERBER_DRILL_FILE_TYPE_EXCELLON)
drill_writer.CreateDrillandMapFilesAt(str(gerber_dir))

print("\n✅ Gerbers exported to:", gerber_dir)
