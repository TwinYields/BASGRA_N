#%%
import pandas as pd
import numpy as np
import bglib as bg
# %%
# %%
# Set params and weather based on /Users/mpastell/BASGRA_N/run_BASGRA_Saerheim_2000_09_Grindstad.Rdf

parcol = 14
df_params = pd.read_table("../parameters/parameters.txt")
params = df_params.iloc[:, 14].to_numpy()
p = np.zeros(120) #params dim must be 120
p[:len(params)] = params

bg.set_params(p)
assert bg.parameters_plant.claiv == p[9] # Check

#%%
# Weather
weather = pd.read_table("../weather/weather_00_Saerheim_format_bioforsk.txt")
year_start = 2000
doy_start = 112
wm = weather.query(f"YR == {year_start}").query(f"doy > {doy_start-1}")

bge = bg.environment

n = wm.shape[0]
NWEATHER = 8
matrix_weather = np.zeros((bge.nmaxdays, NWEATHER))
matrix_weather[0:n,0] = wm.YR
matrix_weather[0:n,1] = wm.doy
matrix_weather[0:n,2] = wm.GR
matrix_weather[0:n,3] = wm["T"]
matrix_weather[0:n,4] = wm["T"]
matrix_weather[0:n,5] = np.exp(17.27*wm["T"]/(wm["T"]+239)) * 0.6108 * wm.RH / 100
matrix_weather[0:n,6] = wm.RAINI
matrix_weather[0:n,7] = wm.WNI

#%%
MATRIX_WEATHER = matrix_weather

bge.yeari  = MATRIX_WEATHER[:,0]
bge.doyi   = MATRIX_WEATHER[:,1]
bge.gri    = MATRIX_WEATHER[:,2]
bge.tmmni  = MATRIX_WEATHER[:,3]
bge.tmmxi  = MATRIX_WEATHER[:,4]
bge.vpi   = MATRIX_WEATHER[:,5]
bge.raini = MATRIX_WEATHER[:,6]
bge.wni   = MATRIX_WEATHER[:,7]

#%%
bg.bglib.init()

#%%
#while
import copy

out = []
for i in range(n):
    bg.bglib.step()
    print(bg.bglib.dm_max)
    #print(bg.bglib.lai)
    d = dict(dm_max  = bg.bglib.dm_max,
         lai = bg.bglib.lai,
         day = bg.bglib.day,
         doy = bg.bglib.doy
         )
    out.append(copy.deepcopy(d))

# %%
import matplotlib.pyplot as plt
df = pd.DataFrame(out)
fig, (ax1, ax2) = plt.subplots(2,1, layout="tight" )
ax1.plot(df["doy"], df["dm_max"])
ax1.set_title("dm_max")
ax2.plot(df["doy"], df["lai"])
ax2.set_title("lai")

plt.show()
# %%
