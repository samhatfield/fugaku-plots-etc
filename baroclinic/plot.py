import numpy as np
import matplotlib.pyplot as plt
from cmcrameri import cm
import matplotlib

matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['font.sans-serif'] = "Droid Sans"

data = np.load("data.npz")

ref_data = data["ref"]
hgemm_data = data["hgemm"]

fig, axes = plt.subplots(ncols=2, figsize=(16,4))
fig.tight_layout(pad=-1.0)

cmap = cm.vik
vmin, vmax = -0.0001, 0.0001

axes[0].imshow(ref_data, cmap=cmap, vmin=vmin, vmax=vmax)
axes[1].imshow(hgemm_data, cmap=cmap, vmin=vmin, vmax=vmax)

axes[0].set_title("Reference (FP32)")
axes[1].set_title("FP16 experiment")

for ax in axes:
    ax.axis("off")

plt.savefig("baroclinic.png", bbox_inches="tight")
plt.savefig("baroclinic.pdf", bbox_inches="tight")