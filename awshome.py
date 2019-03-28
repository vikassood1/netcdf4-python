

import netCDF4
import numpy as np
import pandas as pd



f = netCDF4.Dataset('/Users/vsood/Downloads/prods_op_mogreps-uk_20140717_03_11_015.nc', 'r')
for cube in f.variables.keys():
    if len(f.variables[cube].shape) > 1:
        print(cube)


# In[99]:


air_visibility = f.variables['visibility_in_air']
wind_speed = f.variables['wind_speed_of_gust']
fog_area = f.variables['fog_area_fraction']
air_temperature = f.variables['air_temperature_2']
snowfall_rate = f.variables['stratiform_snowfall_rate']
snowfall_amount = f.variables['stratiform_snowfall_amount']
rainfall_rate = f.variables['stratiform_rainfall_rate']
rainfall_amount = f.variables['stratiform_rainfall_amount']
x_wind = f.variables['x_wind']
x_wind_0 = f.variables['x_wind_0']
x_wind_1 = f.variables['x_wind_1']
y_wind = f.variables['y_wind']
y_wind_0 = f.variables['y_wind_0']
y_wind_1 = f.variables['y_wind_1']


# In[156]:


aviation_cubes = [air_visibility, wind_speed, fog_area, air_temperature, 
                 snowfall_rate,  rainfall_rate, x_wind, x_wind_0, x_wind_1, 
                 y_wind, y_wind_0,y_wind_1]


# In[143]:


def create_arrays(dataset, dim_tuple, size):
    main_dim, *rest_of_dims = dim_tuple
    main_dim_data = dataset.variables[main_dim][:]
    for i in range(len(rest_of_dims)):
        rest_of_dims[i] = dataset.variables[rest_of_dims[i]][:]
    return np.vstack(np.meshgrid(main_dim_data, *rest_of_dims)).reshape(size, -1).T


# In[157]:


for cube in aviation_cubes:
    size = cube.size
    dims = cube.dimensions
    print("cube: {}, size = {}, dims = {}".format(cube.name, size, dims))
    cube_data = cube[:].reshape(size,1) # reshaping all forecast data into a single columnß
    cube_data = create_arrays(f, dims, size)
    print(cube_data.size)
    print(cube_data.shape)



# ## We can reshape the array into a single column


reshaped_air_temp = air_temperature[:].reshape(692124,1)



time = f.variables['time_0'][:]
print(type(time))
lat = f.variables['grid_latitude'][:]
long = f.variables['grid_longitude'][:]





new_array = np.vstack(np.meshgrid(time,lat,long)).reshape(3, -1).T




df = pd.concat([pd.DataFrame(new_array), pd.DataFrame(reshaped_air_temp) - 273.15],axis=1)
df.to_csv('/Users/vsood/Downloads/new_array.csv')

