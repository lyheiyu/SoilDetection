import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import ParameterEstimator
from pgmpy.estimators import MaximumLikelihoodEstimator
import pandas as pd
from pgmpy.estimators import HillClimbSearch, BicScore
# analysis soil data afrian_soil_data.csv
# Load data
data = pd.read_csv('afrian_soil_data.csv')
#
# data = {
#     'm757.896': [3, 2, 1, 0, 3, 2, 1, 0],
#     'm800.123': [1.5, 2.3, 3.1, 4.0, 1.2, 2.1, 3.0, 4.1],
#     '3497': [5, 6, 7, 8, 9, 10, 11, 12]  # 模拟问题列
# }
# anaylsis soil data
# Create DataFrame




X = pd.DataFrame(data)

# 离散化连续数据
X['m800.123'] = pd.qcut(X['m800.123'], q=4, labels=False)

# 处理问题列
X['3497'] = pd.qcut(X['3497'], q=4, labels=False)  # 将连续数据分桶
X['3497'] = X['3497'].astype('category')  # 转换为类别型

# 检查每一列
for col in X.columns:
    print(f"Column: {col}, Unique values: {X[col].unique()}")

# 使用 HillClimbSearch
hc = HillClimbSearch(X)
best_model = hc.estimate(scoring_method=BicScore(X))

# 打印网络结构
print(best_model.edges())



# 创建有向图
G = nx.DiGraph()

# 添加节点和边
G.add_edges_from([
    ('Precipitation', 'Soil_Erosion'),
    ('Slope', 'Soil_Erosion'),
    ('Soil_Erosion', 'Soil_Acidification')
])

# 调整边
G.remove_edge('Slope', 'Soil_Erosion')
G.add_edge('Soil_Organic_Matter', 'Soil_Erosion')

# 可视化网络
nx.draw(G, with_labels=True, node_size=2000, node_color='lightblue')
plt.show()
