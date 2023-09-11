#%%
import plant
print(plant.plant.luemxq)

# %%
plant.plant.lueco2tm(0.01)
print(plant.plant.luemxq)

#%%
import environment
print(environment.environment.ptran)
environment.environment.penman(2.0)
print(environment.environment.ptran)

# %%
environment.parameters_site.lat = 60
for d in range(100):
    environment.environment.ddayl(d)
    print(environment.environment.dayl)

# %%
