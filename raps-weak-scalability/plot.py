import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from math import pi, ceil
import matplotlib


def km_from_tco(tco):
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

fig, axes = plt.subplots(figsize=(6,4))
axes.plot(data["Truncation"], data["SDPD"])

axes.grid(False)

xlims = [0, 1400]
ylims = [200, 350]

axes.plot(xlims, [240, 240], '--')
axes.text(xlims[1]+40, 240, "Operational target\n(10 days in 1 hour)", verticalalignment="center")

axes.plot([1279, 1279], ylims, ':')
axes.text(1279, 365, "Operational resolution", horizontalalignment="center")

axes.set_xlim(xlims)
axes.set_ylim(ylims)

ax2 = axes.twiny()
ax2.grid(False)
ax2.set_xlim(xlims)
ax2.set_xticks(data["Truncation"])
ax2.set_xticklabels([f"{tco} km" for tco in data["Resolution (km)"]])

for nodes, trunc, sdpd in zip(data["Nodes"], data["Truncation"], data["SDPD"]):
    text = f"{nodes}\nnode" if nodes == 1 else f"{nodes}\nnodes"
    axes.text(trunc, sdpd+7, text, horizontalalignment="center", backgroundcolor="white",
              bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='none'))

axes.set_xlabel("Spectral truncation")
axes.set_ylabel("Simulated days per day")

plt.savefig("raps-weak-scalability.png", dpi=200, bbox_inches="tight")
plt.savefig("raps-weak-scalability.pdf", dpi=200, bbox_inches="tight")