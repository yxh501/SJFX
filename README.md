# 基于Python的电商用户行为数据分析与可视化大屏系统

## 📌 项目简介
本项目基于阿里巴巴天池公开的电商用户行为数据集（UserBehavior），使用 Python 技术栈完成了从数据清洗、商业模型分析到多维数据可视化及交互式大屏搭建的端到端流程。主要应用模型包括：RFM用户分层模型、转化漏斗分析、帕累托/ABC分类、波士顿矩阵及购物篮关联规则。

## 📂 目录结构
- `run_all.py` : 核心数据处理与 10 张静态图表生成脚本。
- `app.py` : 基于 Streamlit 与 Plotly 的交互式可视化大屏源码。
- `figures/` : 存放由 Python 代码生成的全部高清图表（150dpi）。
- （注：原始数据 `UserBehavior.csv` 体积过大，未包含在仓库中，请从阿里天池官网下载）。

## 🛠️ 技术栈
- 数据处理：Pandas, NumPy
- 数据可视化：Matplotlib, Seaborn, Plotly
- 交互式大屏：Streamlit

## 🚀 复现步骤
1. 克隆本仓库到本地：`git clone https://github.com/yxh501/SJFX.git`
2. 安装依赖库：`pip install pandas numpy matplotlib seaborn streamlit plotly`
3. 将下载好的 `UserBehavior.csv` 放入根目录。
4. 运行数据分析与图表生成：`python run_all.py`
5. 启动交互式大屏：`streamlit run app.py`

## 🔗 数据来源与合规声明
- 数据源：阿里巴巴天池 - UserBehavior 用户行为数据集
- URL：https://tianchi.aliyun.com/dataset/dataDetail?dataId=649
- 获取方式：官方公开下载 (非爬虫获取)
- License：面向公众开放的免费学术研究数据集

## 👨‍🎓 作者信息
- 姓名：余鑫豪
- 学校：嘉兴大学 数据科学学院
