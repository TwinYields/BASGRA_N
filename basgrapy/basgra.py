#%%
# Try to implement basgra model main loop using Python
# Based on BASGRA.f90
import numpy as np
import pandas as pd
import basgra as bg
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
# Calendars #TODO implement calendars

# %%
# Initial constants for plant state variables 93
# BASGRA.f90 line
CLV        = bg.parameters_plant.clvi
CLVD       = bg.parameters_plant.clvdi
CRES       = bg.parameters_plant.cresi
CRT        = bg.parameters_plant.crti
CST        = bg.parameters_plant.csti
CSTUB      = bg.parameters_plant.cstubi
LAI        = bg.parameters_plant.laii
LT50       = bg.parameters_plant.lt50i
NRT        = bg.parameters_plant.ncr * bg.parameters_plant.crti
K = bg.parameters_plant.k
LAII = bg.parameters_plant.laii
NCSHI      = bg.parameters_plant.ncshmax * (1-np.exp(-K*LAII)) / (K*LAII)
NSH        = NCSHI  * (bg.parameters_plant.clvi+bg.parameters_plant.csti)
PHEN       = bg.parameters_plant.pheni
ROOTD      = bg.parameters_plant.rootdm
TILG1      = bg.parameters_plant.tiltoti *       bg.parameters_plant.frtilgi *    bg.parameters_plant.frtilgg1i
TILG2      = bg.parameters_plant.tiltoti *       bg.parameters_plant.frtilgi * (1-bg.parameters_plant.frtilgg1i)
TILV       = bg.parameters_plant.tiltoti * (1. - bg.parameters_plant.frtilgi)
VERN       = 1
YIELD      = 0
YIELD_LAST = 0
YIELD_TOT  = 0

Nfert_TOT  = 0
DM_MAX     = 0

#%%

#! Initial constants for soil state variables
CLITT      = bg.parameters_site.clitt0
CSOMF      = bg.parameters_site.csom0 * bg.parameters_site.fcsomf0
CSOMS      = bg.parameters_site.csom0 * (1-bg.parameters_site.fcsomf0)
DRYSTOR    = bg.parameters_site.drystori
Fdepth     = bg.parameters_site.fdepthi
NLITT      = bg.parameters_site.clitt0 / bg.parameters_site.cnlitt0
NSOMF      = (bg.parameters_site.csom0 *    bg.parameters_site.fcsomf0)  / bg.parameters_site.cnsomf0
NSOMS      = (bg.parameters_site.csom0 * (1-bg.parameters_site.fcsomf0)) / bg.parameters_site.cnsoms0
NMIN       = bg.parameters_site.nmin0
O2         = bg.parameters_site.fgas * bg.parameters_plant.rootdm * bg.parameters_site.fo2mx * 1000./22.4
Sdepth     = bg.parameters_site.sdepthi
TANAER     = bg.parameters_site.tanaeri
WAL        = 1000. * bg.parameters_plant.rootdm * bg.parameters_site.wci
WAPL       = bg.parameters_site.wapli
WAPS       = bg.parameters_site.wapsi
WAS        = bg.parameters_site.wasi
WETSTOR    = bg.parameters_site.wetstori

#%%
# Intermediate and rate variables, init to 0 as needed
Frate = 0
FREEZEPL = np.zeros(1)

INFIL = PackMelt = poolDrain = poolInfil = pSnow = reFreeze = 0.0
SnowMelt = THAWPS = wRemain = 0.0


# %%
# From line
# do day = 1, NDAYS
bgs = basgra.soil

day = 0
doy = bge.doyi[day]

bge.ddayl(doy)
bge.set_weather_day(day, DRYSTOR, 0, doy)

bgs.soilwatercontent(Fdepth, ROOTD, WAL)
bgs.physics(bge.davtmp, Fdepth, ROOTD, Sdepth, WAS, Frate)
bge.microclimate(doy, DRYSTOR, Fdepth, Frate, LAI, Sdepth, bgs.tsurf, WAPL, WAPS,
                WETSTOR, FREEZEPL[0],INFIL,PackMelt,poolDrain,poolInfil,pSnow,reFreeze,
                SnowMelt,THAWPS,wRemain)

# %%
