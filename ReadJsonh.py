from graphviz import Digraph


def print_tree(data, indent=0, is_last=True, prefix=""):
    """
    递归打印树状结构。
    :param data: 需要打印的字典或列表
    :param indent: 当前缩进层级（整型）
    :param is_last: 在该层级，是否是最后一个元素，用于绘制树形分支
    :param prefix: 上层传递下来的前缀符号，用于树形分支连接
    """

    # 根据是否是最后一个节点，选择不同的树形连接符号
    branch = "└── " if is_last else "├── "

    # 如果 data 是字典
    if isinstance(data, dict):
        items = list(data.items())
        # 在打印字典时，先打印出当前 key 的层级分支；之后再对 value 进行递归
        # 但是，这里要注意我们自己本身没有 key，需要外面传 key；或者把 key 放在上层管理
        # 为简化，下面写法仅在列表或父字典遍历时输出 key
        for idx, (key, value) in enumerate(items):
            # 判断是否是此层级最后一个元素
            is_last_child = (idx == len(items) - 1)

            # 打印前缀 + 分支符号 + key
            print(prefix + branch + str(key) + ":")

            # 下层的前缀（带“竖线”还是空格）需要根据是否是最后节点来决定
            sub_prefix = prefix + ("    " if is_last_child else "│   ")

            # 递归打印 value
            print_tree(value, indent + 1, is_last_child, sub_prefix)

    # 如果 data 是列表
    elif isinstance(data, list):
        for i in range(len(data)):
            is_last_child = (i == len(data) - 1)
            # 这里给每个列表元素都打印一个 “[index]” 之类的标识
            print(prefix + branch + f"[{i}]")
            # 递归
            sub_prefix = prefix + ("    " if is_last_child else "│   ")
            print_tree(data[i], indent + 1, is_last_child, sub_prefix)

    # 如果 data 既不是字典也不是列表，就直接打印数据值
    else:
        # 这里的 branch 只在节点第一次打印时体现；为了兼顾多行，需要再缩进一下
        print(prefix + branch + str(data))


# ----- 以下是将你的原始数据作为 Python 字典示例 -----
data = {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [10.0, 50.0]
    },
    "properties": {
        "layers": [
            {
                "name": "bdod",
                "unit_measure": {
                    "d_factor": 100,
                    "mapped_units": "cg/cm³",
                    "target_units": "kg/dm³",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 84,
                            "Q0.5": 135,
                            "Q0.95": 164,
                            "mean": 129,
                            "uncertainty": 6
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 100,
                            "Q0.5": 139,
                            "Q0.95": 167,
                            "mean": 135,
                            "uncertainty": 5
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 107,
                            "Q0.5": 144,
                            "Q0.95": 170,
                            "mean": 143,
                            "uncertainty": 4
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 117,
                            "Q0.5": 152,
                            "Q0.95": 178,
                            "mean": 149,
                            "uncertainty": 4
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 114,
                            "Q0.5": 155,
                            "Q0.95": 181,
                            "mean": 152,
                            "uncertainty": 4
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 117,
                            "Q0.5": 158,
                            "Q0.95": 187,
                            "mean": 154,
                            "uncertainty": 4
                        }
                    }
                ]
            },
            {
                "name": "cec",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "mmol(c)/kg",
                    "target_units": "cmol(c)/kg",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 62,
                            "Q0.5": 202,
                            "Q0.95": 646,
                            "mean": 282,
                            "uncertainty": 29
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 40,
                            "Q0.5": 150,
                            "Q0.95": 457,
                            "mean": 189,
                            "uncertainty": 28
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 32,
                            "Q0.5": 132,
                            "Q0.95": 434,
                            "mean": 168,
                            "uncertainty": 30
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 44,
                            "Q0.5": 136,
                            "Q0.95": 449,
                            "mean": 175,
                            "uncertainty": 30
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 32,
                            "Q0.5": 130,
                            "Q0.95": 435,
                            "mean": 171,
                            "uncertainty": 31
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 27,
                            "Q0.5": 132,
                            "Q0.95": 351,
                            "mean": 162,
                            "uncertainty": 25
                        }
                    }
                ]
            },
            {
                "name": "cfvo",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "cm³/dm³",
                    "target_units": "cm³/100cm³",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 0,
                            "Q0.5": 80,
                            "Q0.95": 430,
                            "mean": 132,
                            "uncertainty": 54
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 20,
                            "Q0.5": 80,
                            "Q0.95": 290,
                            "mean": 109,
                            "uncertainty": 34
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 20,
                            "Q0.5": 100,
                            "Q0.95": 440,
                            "mean": 149,
                            "uncertainty": 42
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 10,
                            "Q0.5": 130,
                            "Q0.95": 470,
                            "mean": 186,
                            "uncertainty": 35
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 10,
                            "Q0.5": 190,
                            "Q0.95": 750,
                            "mean": 234,
                            "uncertainty": 39
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 0,
                            "Q0.5": 230,
                            "Q0.95": 750,
                            "mean": 258,
                            "uncertainty": 33
                        }
                    }
                ]
            },
            {
                "name": "clay",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "g/kg",
                    "target_units": "%",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 5,
                            "Q0.5": 255,
                            "Q0.95": 825,
                            "mean": 317,
                            "uncertainty": 32
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 8,
                            "Q0.5": 306,
                            "Q0.95": 873,
                            "mean": 354,
                            "uncertainty": 28
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 6,
                            "Q0.5": 245,
                            "Q0.95": 862,
                            "mean": 320,
                            "uncertainty": 35
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 6,
                            "Q0.5": 241,
                            "Q0.95": 851,
                            "mean": 318,
                            "uncertainty": 35
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 6,
                            "Q0.5": 241,
                            "Q0.95": 860,
                            "mean": 314,
                            "uncertainty": 35
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 6,
                            "Q0.5": 249,
                            "Q0.95": 863,
                            "mean": 319,
                            "uncertainty": 34
                        }
                    }
                ]
            },
            {
                "name": "nitrogen",
                "unit_measure": {
                    "d_factor": 100,
                    "mapped_units": "cg/kg",
                    "target_units": "g/kg",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 60,
                            "Q0.5": 268,
                            "Q0.95": 2500,
                            "mean": 550,
                            "uncertainty": 91
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 100,
                            "Q0.5": 160,
                            "Q0.95": 330,
                            "mean": 180,
                            "uncertainty": 14
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 30,
                            "Q0.5": 100,
                            "Q0.95": 300,
                            "mean": 117,
                            "uncertainty": 27
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 11,
                            "Q0.5": 56,
                            "Q0.95": 201,
                            "mean": 92,
                            "uncertainty": 34
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 10,
                            "Q0.5": 38,
                            "Q0.95": 130,
                            "mean": 57,
                            "uncertainty": 32
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 10,
                            "Q0.5": 30,
                            "Q0.95": 111,
                            "mean": 45,
                            "uncertainty": 34
                        }
                    }
                ]
            },
            {
                "name": "ocd",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "dg/dm³",
                    "target_units": "hg/m³",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 116,
                            "Q0.5": 393,
                            "Q0.95": 935,
                            "mean": 452,
                            "uncertainty": 21
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 103,
                            "Q0.5": 188,
                            "Q0.95": 396,
                            "mean": 221,
                            "uncertainty": 16
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 54,
                            "Q0.5": 140,
                            "Q0.95": 364,
                            "mean": 166,
                            "uncertainty": 22
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 32,
                            "Q0.5": 60,
                            "Q0.95": 141,
                            "mean": 72,
                            "uncertainty": 18
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 16,
                            "Q0.5": 44,
                            "Q0.95": 100,
                            "mean": 53,
                            "uncertainty": 19
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 13,
                            "Q0.5": 26,
                            "Q0.95": 59,
                            "mean": 32,
                            "uncertainty": 18
                        }
                    }
                ]
            },
            {
                "name": "ocs",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "t/ha",
                    "target_units": "kg/m²",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "0-30cm",
                        "values": {
                            "Q0.05": 20,
                            "Q0.5": 38,
                            "Q0.95": 79,
                            "mean": 44,
                            "uncertainty": 16
                        }
                    }
                ]
            },
            {
                "name": "phh2o",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "pH*10",
                    "target_units": "-",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 46,
                            "Q0.5": 70,
                            "Q0.95": 81,
                            "mean": 68,
                            "uncertainty": 5
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 53,
                            "Q0.5": 71,
                            "Q0.95": 83,
                            "mean": 70,
                            "uncertainty": 4
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 53,
                            "Q0.5": 71,
                            "Q0.95": 83,
                            "mean": 70,
                            "uncertainty": 4
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 49,
                            "Q0.5": 71,
                            "Q0.95": 85,
                            "mean": 69,
                            "uncertainty": 5
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 49,
                            "Q0.5": 72,
                            "Q0.95": 85,
                            "mean": 69,
                            "uncertainty": 5
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 48,
                            "Q0.5": 71,
                            "Q0.95": 86,
                            "mean": 69,
                            "uncertainty": 5
                        }
                    }
                ]
            },
            {
                "name": "sand",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "g/kg",
                    "target_units": "%",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 47,
                            "Q0.5": 113,
                            "Q0.95": 616,
                            "mean": 185,
                            "uncertainty": 50
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 44,
                            "Q0.5": 107,
                            "Q0.95": 578,
                            "mean": 170,
                            "uncertainty": 50
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 42,
                            "Q0.5": 113,
                            "Q0.95": 617,
                            "mean": 189,
                            "uncertainty": 51
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 39,
                            "Q0.5": 111,
                            "Q0.95": 635,
                            "mean": 192,
                            "uncertainty": 54
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 38,
                            "Q0.5": 112,
                            "Q0.95": 624,
                            "mean": 191,
                            "uncertainty": 52
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 35,
                            "Q0.5": 114,
                            "Q0.95": 624,
                            "mean": 193,
                            "uncertainty": 52
                        }
                    }
                ]
            },
            {
                "name": "silt",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "g/kg",
                    "target_units": "%",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 36,
                            "Q0.5": 536,
                            "Q0.95": 920,
                            "mean": 497,
                            "uncertainty": 16
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 36,
                            "Q0.5": 493,
                            "Q0.95": 918,
                            "mean": 475,
                            "uncertainty": 18
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 38,
                            "Q0.5": 495,
                            "Q0.95": 930,
                            "mean": 491,
                            "uncertainty": 18
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 39,
                            "Q0.5": 492,
                            "Q0.95": 933,
                            "mean": 490,
                            "uncertainty": 18
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 36,
                            "Q0.5": 511,
                            "Q0.95": 931,
                            "mean": 495,
                            "uncertainty": 18
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 36,
                            "Q0.5": 495,
                            "Q0.95": 931,
                            "mean": 488,
                            "uncertainty": 18
                        }
                    }
                ]
            },
            {
                "name": "soc",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "dg/kg",
                    "target_units": "g/kg",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 91,
                            "Q0.5": 239,
                            "Q0.95": 905,
                            "mean": 374,
                            "uncertainty": 34
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 94,
                            "Q0.5": 153,
                            "Q0.95": 298,
                            "mean": 172,
                            "uncertainty": 13
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 28,
                            "Q0.5": 107,
                            "Q0.95": 271,
                            "mean": 125,
                            "uncertainty": 23
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 15,
                            "Q0.5": 40,
                            "Q0.95": 168,
                            "mean": 60,
                            "uncertainty": 38
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 5,
                            "Q0.5": 25,
                            "Q0.95": 90,
                            "mean": 37,
                            "uncertainty": 34
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 3,
                            "Q0.5": 18,
                            "Q0.95": 53,
                            "mean": 24,
                            "uncertainty": 28
                        }
                    }
                ]
            },
            {
                "name": "wv0010",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "(10-2 cm³/cm³)*10",
                    "target_units": "10-2 cm³/cm³",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 320,
                            "Q0.5": 479,
                            "Q0.95": 704,
                            "mean": 489,
                            "uncertainty": 8
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 262,
                            "Q0.5": 407,
                            "Q0.95": 562,
                            "mean": 414,
                            "uncertainty": 7
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 256,
                            "Q0.5": 389,
                            "Q0.95": 554,
                            "mean": 390,
                            "uncertainty": 8
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 235,
                            "Q0.5": 387,
                            "Q0.95": 501,
                            "mean": 384,
                            "uncertainty": 7
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 224,
                            "Q0.5": 377,
                            "Q0.95": 508,
                            "mean": 368,
                            "uncertainty": 8
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 184,
                            "Q0.5": 358,
                            "Q0.95": 480,
                            "mean": 350,
                            "uncertainty": 8
                        }
                    }
                ]
            },
            {
                "name": "wv0033",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "(10-2 cm³/cm³)*10",
                    "target_units": "10-2 cm³/cm³",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 213,
                            "Q0.5": 388,
                            "Q0.95": 514,
                            "mean": 381,
                            "uncertainty": 8
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 213,
                            "Q0.5": 332,
                            "Q0.95": 467,
                            "mean": 333,
                            "uncertainty": 8
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 201,
                            "Q0.5": 325,
                            "Q0.95": 460,
                            "mean": 321,
                            "uncertainty": 8
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 189,
                            "Q0.5": 322,
                            "Q0.95": 452,
                            "mean": 318,
                            "uncertainty": 8
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 146,
                            "Q0.5": 313,
                            "Q0.95": 434,
                            "mean": 307,
                            "uncertainty": 9
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 135,
                            "Q0.5": 319,
                            "Q0.95": 423,
                            "mean": 308,
                            "uncertainty": 9
                        }
                    }
                ]
            },
            {
                "name": "wv1500",
                "unit_measure": {
                    "d_factor": 10,
                    "mapped_units": "(10-2 cm³/cm³)*10",
                    "target_units": "10-2 cm³/cm³",
                    "uncertainty_unit": ""
                },
                "depths": [
                    {
                        "range": {"top_depth": 0, "bottom_depth": 5, "unit_depth": "cm"},
                        "label": "0-5cm",
                        "values": {
                            "Q0.05": 62,
                            "Q0.5": 177,
                            "Q0.95": 280,
                            "mean": 172,
                            "uncertainty": 12
                        }
                    },
                    {
                        "range": {"top_depth": 5, "bottom_depth": 15, "unit_depth": "cm"},
                        "label": "5-15cm",
                        "values": {
                            "Q0.05": 67,
                            "Q0.5": 180,
                            "Q0.95": 278,
                            "mean": 176,
                            "uncertainty": 12
                        }
                    },
                    {
                        "range": {"top_depth": 15, "bottom_depth": 30, "unit_depth": "cm"},
                        "label": "15-30cm",
                        "values": {
                            "Q0.05": 59,
                            "Q0.5": 173,
                            "Q0.95": 270,
                            "mean": 163,
                            "uncertainty": 12
                        }
                    },
                    {
                        "range": {"top_depth": 30, "bottom_depth": 60, "unit_depth": "cm"},
                        "label": "30-60cm",
                        "values": {
                            "Q0.05": 42,
                            "Q0.5": 146,
                            "Q0.95": 284,
                            "mean": 149,
                            "uncertainty": 17
                        }
                    },
                    {
                        "range": {"top_depth": 60, "bottom_depth": 100, "unit_depth": "cm"},
                        "label": "60-100cm",
                        "values": {
                            "Q0.05": 42,
                            "Q0.5": 151,
                            "Q0.95": 290,
                            "mean": 153,
                            "uncertainty": 16
                        }
                    },
                    {
                        "range": {"top_depth": 100, "bottom_depth": 200, "unit_depth": "cm"},
                        "label": "100-200cm",
                        "values": {
                            "Q0.05": 41,
                            "Q0.5": 150,
                            "Q0.95": 283,
                            "mean": 151,
                            "uncertainty": 16
                        }
                    }
                ]
            }
        ]
    },
    "query_time_s": 24.218835830688477
}

# ----- 调用函数，打印树状结构 -----
print_tree(data)
