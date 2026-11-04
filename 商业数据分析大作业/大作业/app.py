import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. 页面设置
# ==========================================
st.set_page_config(page_title="电商用户行为分析大屏", layout="wide")
st.title("🛒 电商用户行为交互式分析大屏")

# ==========================================
# 2. 数据读取（加入缓存，加快刷新速度）
# ==========================================
@st.cache_data
def load_data():
    # 注意：这里的路径请确保与 run_all.py 里的路径一致
    file_path = r"C:\Users\Administrator\Desktop\数据文件\UserBehavior.csv" 
    # 为了大屏跑得快，我们读取 20 万条数据即可
    df = pd.read_csv(file_path, names=["user_id","item_id","category_id","behavior_type","timestamp"], skiprows=5000000, nrows=200000)
    
    # 数据清洗
    df['time'] = pd.to_datetime(df['timestamp'], unit='s')
    df['date'] = df['time'].dt.date
    df['hour'] = df['time'].dt.hour
    map_behavior = {"pv":"浏览","fav":"收藏","cart":"加购","buy":"购买"}
    df['behavior_name'] = df['behavior_type'].map(map_behavior)
    return df

# 加载数据
df = load_data()

# ==========================================
# 3. 侧边栏筛选组件（2个交互组件）
# ==========================================
st.sidebar.header("🎛️ 筛选控制台")

# 组件1：行为类型多选
selected_behaviors = st.sidebar.multiselect(
    "选择行为类型",
    options=df['behavior_name'].unique(),
    default=df['behavior_name'].unique()
)

# 组件2：日期范围滑动条
date_list = sorted(df['date'].unique())
selected_dates = st.sidebar.select_slider(
    "选择日期范围",
    options=date_list,
    value=(date_list[0], date_list[-1])
)

# 数据过滤逻辑（实现图表随筛选动态联动）
filtered_df = df[
    (df['behavior_name'].isin(selected_behaviors)) & 
    (df['date'] >= selected_dates[0]) & 
    (df['date'] <= selected_dates[1])
]

# ==========================================
# 4. 顶部 KPI 指标卡片（4个指标组件）
# ==========================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("总独立用户数 (UV)", f"{filtered_df['user_id'].nunique():,}")
col2.metric("总行为记录数 (PV)", f"{len(filtered_df):,}")

buy_df = filtered_df[filtered_df['behavior_type'] == 'buy']
col3.metric("购买用户数", f"{buy_df['user_id'].nunique():,}")

# 动态计算转化率
uv_total = filtered_df['user_id'].nunique()
uv_buy = buy_df['user_id'].nunique()
conversion = (uv_buy / uv_total * 100) if uv_total > 0 else 0
col4.metric("购买转化率", f"{conversion:.2f}%")

st.markdown("---")

# ==========================================
# 5. 动态交互图表区
# ==========================================
# 第一排：漏斗图 + 活跃时段图
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("📊 用户行为转化漏斗")
    funnel_data = filtered_df.groupby("behavior_name")["user_id"].nunique().reset_index()
    # 确保漏斗顺序正确
    funnel_data['behavior_name'] = pd.Categorical(funnel_data['behavior_name'], categories=["浏览", "收藏", "加购", "购买"], ordered=True)
    funnel_data = funnel_data.sort_values('behavior_name')
    
    fig_funnel = px.funnel(funnel_data, x='user_id', y='behavior_name', 
                           color='behavior_name', color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig_funnel, use_container_width=True)

with row1_col2:
    st.subheader("⏰ 24小时用户活跃趋势")
    hour_data = filtered_df.groupby("hour")["user_id"].nunique().reset_index()
    fig_line = px.line(hour_data, x='hour', y='user_id', markers=True, 
                       title="各小时独立活跃用户数", color_discrete_sequence=['#F18F01'])
    fig_line.update_layout(xaxis_title="小时", yaxis_title="独立用户数")
    st.plotly_chart(fig_line, use_container_width=True)

# 第二排：柱状图 + 明细表
row2_col1, row2_col2 = st.columns([1.5, 1])

with row2_col1:
    st.subheader("🏆 Top 10 热门购买品类")
    if not buy_df.empty:
        cat_data = buy_df.groupby("category_id")["user_id"].count().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(cat_data, x='category_id', y='user_id', 
                         title="品类购买量 Top 10", color='user_id', color_continuous_scale='Viridis')
        fig_bar.update_layout(xaxis_title="品类 ID", yaxis_title="购买次数")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("当前筛选条件下没有购买数据")

with row2_col2:
    st.subheader("📋 数据明细表 (Top 100)")
    # 组件：明细表
    st.dataframe(filtered_df[['user_id', 'item_id', 'behavior_name', 'time']].head(100), use_container_width=True)

# 底部提示
st.info("💡 提示：请在左侧侧边栏修改筛选条件，上方所有的 KPI 指标和图表都会实时联动更新。")