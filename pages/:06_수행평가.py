import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

# --------------------
# 데이터 불러오기
# --------------------
@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir.parent / "mbti_country.csv"

    if not csv_path.exists():
        st.error(f"파일을 찾을 수 없습니다.\n경로: {csv_path}")
        st.stop()

    return pd.read_csv(csv_path)

df = load_data()

# --------------------
# 제목
# --------------------
st.title("🌍 국가별 MBTI 비율 분석")

# --------------------
# 국가 선택
# --------------------
countries = sorted(df["Country"].unique())

selected_country = st.selectbox(
    "국가를 선택하세요",
    countries
)

country_df = (
    df[df["Country"] == selected_country]
    .sort_values("Percentage", ascending=False)
)

# --------------------
# 색상 설정
# --------------------
colors = []

for i in range(len(country_df)):
    if i == 0:
        colors.append("#ff0000")  # 1등 빨강
    else:
        opacity = max(0.25, 1 - i * 0.05)
        colors.append(f"rgba(0,100,255,{opacity})")

# --------------------
# Plotly 그래프
# --------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=country_df["MBTI"],
        y=country_df["Percentage"],
        marker_color=colors,
        text=country_df["Percentage"].round(1),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>비율: %{y}%<extra></extra>"
    )
)

fig.update_layout(
    title=f"{selected_country} MBTI 비율",
    template="plotly_white",
    height=650,
    xaxis_title="MBTI",
    yaxis_title="비율 (%)",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------
# TOP5
# --------------------
st.subheader("🏆 TOP 5 MBTI")

top5 = country_df.head(5)

for rank, (_, row) in enumerate(top5.iterrows(), start=1):
    st.write(
        f"{rank}위 | {row['MBTI']} | {row['Percentage']:.1f}%"
    )

# --------------------
# 원본 데이터
# --------------------
with st.expander("전체 데이터 보기"):
    st.dataframe(
        country_df,
        use_container_width=True
    )
