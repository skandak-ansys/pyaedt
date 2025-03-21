"""
HFSS 3D Layout: parametric via analysis
---------------------------------------
This example shows how you can use HFSS 3D Layout to create and solve a
parametric via analysis.
"""

###############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports.
import pyaedt
import os

###############################################################################
# Set non-graphical mode
# ~~~~~~~~~~~~~~~~~~~~~~
# Set non-graphical mode. 
# You can set ``non_graphical`` either to ``True`` or ``False``.

non_graphical = True

###############################################################################
# Launch AEDT
# ~~~~~~~~~~~
# Launch AEDT 2023 R2 in graphical mode.

h3d = pyaedt.Hfss3dLayout(specified_version="2023.2", new_desktop_session=True, non_graphical=non_graphical)

###############################################################################
# Set up variables
# ~~~~~~~~~~~~~~~~
# Set up all parametric variables to use in the layout.

h3d["viatotrace"] = "5mm"
h3d["viatovia"] = "10mm"
h3d["w1"] = "1mm"
h3d["sp"] = "0.5mm"
h3d["len"] = "50mm"

###############################################################################
# Add stackup layers
# ~~~~~~~~~~~~~~~~~~
# Add stackup layers.

h3d.modeler.layers.add_layer(layername="GND", layertype="signal", thickness="0", isnegative=True)
h3d.modeler.layers.add_layer(layername="diel", layertype="dielectric", thickness="0.2mm", material="FR4_epoxy")
h3d.modeler.layers.add_layer(layername="TOP", layertype="signal", thickness="0.035mm", elevation="0.2mm")

###############################################################################
# Create signal net and ground planes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a signal net and ground planes.

h3d.modeler.create_line(layername="TOP", center_line_list=[[0, 0], ["len", 0]], lw="w1", netname="microstrip", name="microstrip")
h3d.modeler.create_rectangle(layername="TOP", origin=[0, "-w1/2-sp"], dimensions=["len", "-w1/2-sp-20mm"])
h3d.modeler.create_rectangle(layername="TOP", origin=[0, "w1/2+sp"], dimensions=["len", "w1/2+sp+20mm"])

###############################################################################
# Create vias
# ~~~~~~~~~~~
# Create vias with parametric positions.

h3d.modeler.create_via(x="viatovia", y="-viatotrace", name="via1")
h3d.modeler.create_via(x="viatovia", y="viatotrace", name="via2")
h3d.modeler.create_via(x="2*viatovia", y="-viatotrace")
h3d.modeler.create_via(x="2*viatovia", y="viatotrace")
h3d.modeler.create_via(x="3*viatovia", y="-viatotrace")
h3d.modeler.create_via(x="3*viatovia", y="viatotrace")

###############################################################################
# Create circuit ports
# ~~~~~~~~~~~~~~~~~~~~
# Create circuit ports.

h3d.create_edge_port("microstrip", 0)
h3d.create_edge_port("microstrip", 2)

###############################################################################
# Create setup and sweep
# ~~~~~~~~~~~~~~~~~~~~~~
# Create a setup and a sweep.

setup = h3d.create_setup()
h3d.create_linear_count_sweep(
    setupname=setup.name,
    unit="GHz",
    freqstart=3,
    freqstop=7,
    num_of_freq_points=1001,
    sweepname="sweep1",
    sweep_type="Interpolating",
    interpolation_tol_percent=1,
    interpolation_max_solutions=255,
    save_fields=False,
    use_q3d_for_dc=False,
)

###############################################################################
# Solve and plot results
# ~~~~~~~~~~~~~~~~~~~~~~
# Solve and plot the results.

h3d.analyze()
traces = h3d.get_traces_for_plot(first_element_filter="Port1")
h3d.post.create_report(traces, variations=h3d.available_variations.nominal_w_values_dict)

###############################################################################
# Create report outside AEDT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a report using Matplotlib.

traces = h3d.get_traces_for_plot(first_element_filter="Port1", category="S")

solutions = h3d.post.get_solution_data(expressions=traces)
solutions.plot(math_formula="db20")

###############################################################################
# Close AEDT
# ~~~~~~~~~~
# After the simulation completes, you can close AEDT or release it using the
# :func:`pyaedt.Desktop.release_desktop` method.
# All methods provide for saving the project before closing.

h3d.release_desktop()
