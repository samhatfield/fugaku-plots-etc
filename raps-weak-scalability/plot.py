import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from math import pi, ceil
import matplotlib


def km_from_tco(tco):
    # The convention is to refer to TCo1279 as 9 km, but the equation below gives 8 km
    # For this resolution we manually set it to 9 km
    if tco == 1279:
        return 9.0
    else:
        return 2.0*pi*6400.0/float(4*(tco+1))


sb.set_style("whitegrid")

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['font.sans-serif'] = "Droid Sans"
matplotlib.rc('axes', axisbelow=True)

color_1 = colors[0]
color_2 = colors[1]
color_3 = colors[2]

data = pd.read_csv("data.csv")
data["Truncation"] = [int(res[3:]) for res in data["Resolution"]]
data["Resolution (km)"] = [ceil(km_from_tco(tco)) for tco in data["Truncation"]]

fig, axes = plt.subplots(figsize=(8,4))
axes.plot(data["Truncation"], data["SDPD"], 'x-')

axes.grid(False)

xlims = [0, 2580]
ylims = [100, 350]

axes.plot(xlims, [240, 240], '--')
axes.text(xlims[1]+40, 240, "Operational target\n(10 days in 1 hour)", verticalalignment="center")

axes.plot([1279, 1279], ylims, ':')
axes.text(1279, 385, "Operational\nresolution", horizontalalignment="center")

axes.set_xlim(xlims)
axes.set_ylim(ylims)

axes.set_xticks(data["Truncation"])
axes.set_xticklabels([f"TCo{tco}" for tco in data["Truncation"]])

ax2 = axes.twiny()
ax2.grid(False)
ax2.set_xlim(xlims)
ax2.set_xticks(data["Truncation"])
ax2.set_xticklabels([f"{tco} km" for tco in data["Resolution (km)"]])

for i, (nodes, trunc, sdpd) in enumerate(zip(data["Nodes"], data["Truncation"], data["SDPD"])):
    if i == 0:
        text = f"{nodes}\nnode" if nodes == 1 else f"{nodes}\nnodes"
    else:
        text = f"{nodes}"

    # The text for 1279 needs to be visible above the green-dashed line so the alpha is set to 1.0
    # for that datapoint alone
    alpha = 1.0 if trunc == 1279 else 0.0

    axes.text(trunc, sdpd+13, text, horizontalalignment="center", backgroundcolor="white",
              bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='none', alpha=alpha))

axes.set_xlabel("Spectral truncation")
axes.set_ylabel("Simulated days per day")

plt.savefig("raps-weak-scalability.png", dpi=200, bbox_inches="tight")
plt.savefig("raps-weak-scalability.pdf", dpi=200, bbox_inches="tight")
