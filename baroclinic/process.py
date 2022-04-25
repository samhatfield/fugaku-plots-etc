import xarray as xr
import numpy as np

# GRIB code for vorticity
var = "var138"

# Location of raw NetCDF files
data_dir = "/ec/res4/hpcperm/nash/fugaku_store/tco399/baroclinic"

# Actual NetCDF files for the reference and the one using HGEMM Legendre transforms
ref = "ICMSHhloa_vo_500hPa_ref.nc"
hgemm = "ICMSHhloa_vo_500hPa_hgemm_10.nc"

# Load last timestep of both datasets, squeezing the singleton time dimension, and convert to Numpy
# array
ref_data = xr.open_dataset(f"{data_dir}/{ref}")[var].isel(time=-1).squeeze().data
hgemm_data = xr.open_dataset(f"{data_dir}/{hgemm}")[var].isel(time=-1).squeeze().data

# Save to disk
np.savez("data.npz", ref=ref_data, hgemm=hgemm_data)
