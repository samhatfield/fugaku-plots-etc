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

color_1 = colors[0]
color_2 = colors[1]
color_3 = colors[2]

data = pd.read_csv("data.csv")
data["Truncation"] = [int(res[3:]) for res in data["Resolution"]]
data["Resolution (km)"] = [ceil(km_from_tco(tco)) for tco in data["Truncation"]]
data["Inverse (SP)"] = (data["I1 (ref)"] + data["I2 (ref)"])/2.0
data["Inverse (HP)"] = (data["I1 (hgemm)"] + data["I2 (hgemm)"])/2.0
data["Direct (SP)"] = (data["D1 (ref)"] + data["D2 (ref)"])/2.0
data["Direct (HP)"] = (data["D1 (hgemm)"] + data["D2 (hgemm)"])/2.0

fig, axes = plt.subplots(nrows=2, sharex=True, gridspec_kw={"height_ratios": [2, 1]},
                         figsize=(6,6))
axes[0].plot(data["Truncation"], data["Inverse (SP)"], color=color_1,
             linestyle="--", label="FP32, inverse")
axes[0].plot(data["Truncation"], data["Inverse (HP)"], color=color_2,
             linestyle="--", label="FP16, inverse")
axes[0].plot(data["Truncation"], data["Direct (SP)"], color=color_1,
             linestyle=":", label="FP32, direct")
axes[0].plot(data["Truncation"], data["Direct (HP)"], color=color_2,
             linestyle=":", label="FP16, direct")

axes[1].plot(data["Truncation"], data["Inverse (SP)"]/data["Inverse (HP)"],
             color="black", linestyle="--", label="Inverse")
axes[1].plot(data["Truncation"], data["Direct (SP)"]/data["Direct (HP)"],
             color="black", linestyle=":", label="Direct")

axes[1].set_ylim([1.0, 3.0])

axes[0].set_ylabel("Time per GEMM call (ms)")
axes[1].set_ylabel("FP16 acceleration")
axes[1].set_xlabel("Spectral truncation")

axes[0].grid(False)
axes[1].grid(axis="x")

axes[0].legend(loc=(0.2,0.6), frameon=False)
axes[1].legend(frameon=False, ncol=2)

ax2 = axes[0].twiny()
ax2.set_xlim(axes[0].get_xlim())
ax2.set_xticks(data["Truncation"])
ax2.set_xticklabels([f"{tco} km" for tco in data["Resolution (km)"]])

plt.savefig("spectral-transform-dwarf-hgemm.png", dpi=200, bbox_inches="tight")
plt.savefig("spectral-transform-dwarf-hgemm.pdf", dpi=200, bbox_inches="tight")