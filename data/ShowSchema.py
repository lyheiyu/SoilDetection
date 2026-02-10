import networkx as nx
import matplotlib.pyplot as plt
# 初始化有向图
G = nx.DiGraph()

# 添加实体节点
entities = [
    "Cropfield", "EnvironmentalData", "Sensor", "SensorMeasurement",
    "ExperimentalPlot", "SocioEconomicData", "SoilHealthMeasure",
    "SoilSample", "SoilAnalysis", "Analysis", "RemoteSensing", "InterpretedData"
]
G.add_nodes_from(entities)

# 添加关系（边）
relations = [
    ("SoilSample", "Cropfield"),
    ("SoilSample", "ExperimentalPlot"),
    ("Analysis", "SoilSample"),
    ("Analysis", "SoilAnalysis"),
    ("SensorMeasurement", "Sensor"),
    ("SensorMeasurement", "ExperimentalPlot"),
    ("ExperimentalPlot", "SoilHealthMeasure"),
    ("RemoteSensing", "Cropfield"),
    ("InterpretedData", "RemoteSensing"),
    ("InterpretedData", "Analysis"),
]

G.add_edges_from(relations)

# 可视化
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5, iterations=50)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, arrows=True)
plt.title("SOILCRATES Data Platform ER Diagram")
plt.show()
