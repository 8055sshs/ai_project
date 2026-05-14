# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="Countries MBTI Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -----------------------------
# 타이틀
# -----------------------------
st.title("🌍 국가별 MBTI 비율 대시보드")
st.markdown("국가를 선택하면 MBTI 비율을 인터랙티브하게 확인할 수 있어요.")

# -----------------------------
# 국가 선택
# -----------------------------
countries = sorted(df["Country"].unique())

selected_country = st.selectbox(
    "국가 선택",
    countries
)

# -----------------------------
# 선택 국가 데이터
# -----------------------------
country_data = df[df["Country"] == selected_country]

mbti_cols = [col for col in df.columns if col != "Country"]

values = country_data[mbti_cols].iloc[0]

chart_df = pd.DataFrame({
    "MBTI": mbti_cols,
    "Ratio": values.values
})

# 내림차순 정렬
chart_df = chart_df.sort_values(
    by="Ratio",
    ascending=False
).reset_index(drop=True)

# -----------------------------
# 색상 설정
# 1등 = 빨간색
# 나머지 = 파란색 그라데이션
# -----------------------------
colors = []

blue_gradient = [
    "#0B3D91",
    "#1456C3",
    "#1E6DE0",
    "#3B82F6",
    "#60A5FA",
    "#93C5FD",
    "#BFDBFE",
    "#DBEAFE",
]

for i in range(len(chart_df)):
    if i == 0:
        colors.append("#FF3B30")  # 1등 빨간색
    else:
        colors.append(
            blue_gradient[(i - 1) % len(blue_gradient)]
        )

# -----------------------------
# Plotly 그래프
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_df["MBTI"],
        y=chart_df["Ratio"],
        marker_color=colors,
        text=chart_df["Ratio"].round(3),
        textposition="outside",
        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.3f}<extra></extra>"
    )
)

fig.update_layout(
    title=f"{selected_country} MBTI 비율",
    template="plotly_white",
    height=600,
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    hovermode="x unified",
    font=dict(
        size=16
    ),
    title_font=dict(
        size=24
    ),
    xaxis=dict(
        tickangle=0
    ),
    showlegend=False
)

# -----------------------------
# 그래프 출력
# -----------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# TOP 3 표시
# -----------------------------
st.subheader("🏆 가장 높은 MBTI TOP 3")

top3 = chart_df.head(3)

for idx, row in top3.iterrows():
    st.markdown(
        f"""
        **{idx+1}위**
        - MBTI: `{row['MBTI']}`
        - 비율: `{row['Ratio']:.3f}`
        """
    )

# -----------------------------
# 전체 데이터 보기
# -----------------------------
with st.expander("전체 데이터 보기"):
    st.dataframe(chart_df, use_container_width=True)
