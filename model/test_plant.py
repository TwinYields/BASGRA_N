#%%
import basgra
print(basgra.plant.luemxq)

# %%
basgra.plant.lueco2tm(0.01)
print(basgra.plant.luemxq)

# %%
import basgra
basgra.parameters_site.lat = 60
for d in range(100):
    basgra.environment.ddayl(d)
    print(basgra.environment.dayl)

# %%
