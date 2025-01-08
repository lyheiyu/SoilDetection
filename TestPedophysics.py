from pedophysics.simulate import Soil
from pedophysics.predict.bulk_ec import BulkEC
#
# # 创建土壤对象，设置已知属性
# soil_sample = Soil(
#     sand=70,  # 砂含量百分比
#     silt=20,  # 粉砂含量百分比
#     clay=10,  # 粘土含量百分比
#     water=0.25,  # 体积含水量
#     temperature=298.15  # 温度（开尔文）
# )
#
# # 预测土壤的体积电导率
# bulk_ec = BulkEC(soil_sample)
# print(f"bulk_ec: {bulk_ec} S/m")
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Get notebook and parent dir
current_dir = os.path.dirname(os.path.abspath('__file__'))
parent_dir = os.path.dirname(current_dir)

# Set path to pedophysics module
pedophysics_code_path = os.path.join(parent_dir)
sys.path.insert(0, pedophysics_code_path)

# Import Pedophysics module
from pedophysics.simulate import Soil
from pedophysics import predict
from pedophysics.predict import *

from pedophysics.pedophysical_models.bulk_ec import Rhoades
from pedophysics.pedophysical_models.bulk_perm import Hilhorst

# Set pandas display option
pd.set_option('max_colwidth', None)

sample1 = Soil(water = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4],
               porosity = 0.4)

print(sample1.water)
print(sample1.porosity)
print(sample1.water_ec)
print(sample1)

sample2 = Soil( bulk_ec = [0.01, 0.02, 0.025, np.nan, 0.030, 0.040],
                clay = 10,
                porosity = 0.4,
                water_ec = 0.5)

sample2_water = predict.Water(sample2)
sample2.df.to_csv('test.csv',index=False)
print('sample2_water', sample2_water)
print('sample2.info.water', sample2.info.water)
print('sample2.info.bulk_ec', sample2.info.bulk_ec)

####################################################### PLOT ############################################

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
fig.set_figheight(5.5)
fig.set_figwidth(10)
ss=150
ax.scatter(sample2.bulk_ec, sample2_water*100, color='blue', alpha=0.8, s=ss, label = "sample2")
ax.set_xlim(0, 0.05)
ax.set_ylim(0, 35)
ax.set_xlabel('given bulk_ec [S/m]', fontsize = 18)
ax.set_ylabel('predicted water [%]', fontsize = 18)
ax.tick_params(axis='y', labelsize=14)
ax.tick_params(axis='x', labelsize=14)
ax.grid(True)
ax.legend(loc='upper right', fontsize = 14)

plt.savefig('Fig10')
plt.show()


sample3 = Soil(bulk_ec = [0.01, 0.02, 0.025, np.nan, 0.030, 0.040],
                clay = [11, 8, 12, 10, 15, 7],
                porosity = 0.4,
                water_ec = 0.5)

sample3_water = predict.Water(sample3)
print('sample3_water', sample3_water)

####################################################### PLOT ############################################

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
fig.set_figheight(5.5)
fig.set_figwidth(10)

ax.scatter(sample2.bulk_ec, sample2.df.water*100, color='blue', alpha=0.8, s=ss, label = "sample2")
ax.scatter(sample3.bulk_ec, sample3.df.water*100, color='red', alpha=0.8, s=ss, label = "sample3")

ax.set_xlim(0, 0.05)
ax.set_ylim(0, 35)
ax.set_xlabel('given bulk_ec [S/m]', fontsize = 18)
ax.set_ylabel('predicted water [%]', fontsize = 18)
ax.tick_params(axis='y', labelsize=14)
ax.tick_params(axis='x', labelsize=14)
ax.grid(True)
ax.legend(loc='upper right', fontsize = 14)

plt.savefig('Fig11')
plt.show()