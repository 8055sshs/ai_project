# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="MBTI 국가 분석",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# -----------------------------------
# 제목
# -----------------------------------
st.title("🌍 MBTI별 국가 비율 분석")
st.markdown("MBTI를 선택하면 해당 유형 비율이 높은 국가를 확인할 수 있어요.")

# -----------------------------------
# MBTI 선택
# -----------------------------------
mbti_list = [col for col in df.columns if col != "Country"]

selected_mbti = st.selectbox(
    "MBTI 선택",
    sorted(mbti_list)
)

# -----------------------------------
# 상위 국가 개수 선택
# -----------------------------------
top_n = st.slider(
    "상위 국가 개수",
    min_value=5,
    max_value=10,
    value=5
)

# -----------------------------------
# 데이터 가공
# -----------------------------------
chart_df = df[["Country", selected_mbti]].copy()

chart_df.columns = ["Country", "Ratio"]

# 높은 순 정렬
chart_df = chart_df.sort_values(
    by="Ratio",
    ascending=False
)

# 상위 N개 선택
chart_df = chart_df.head(top_n)

# -----------------------------------
# 색상 설정
# 1등 = 빨간색
# 나머지 = 파란색 그라데이션
# -----------------------------------
blue_gradient = [
    "#0B3D91",
    "#1456C3",
    "#1E6DE0",
    "#3B82F6",
    "#60A5FA",
    "#93C5FD",
    "#BFDBFE",
    "#DBEAFE"
]

colors = []

for i in range(len(chart_df)):
    if i == 0:
        colors.append("#FF3B30")
    else:
        colors.append(
            blue_gradient[(i - 1) % len(blue_gradient)]
        )

# -----------------------------------
# Plotly 그래프 생성
# -----------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        y=chart_df["Country"],
        x=chart_df["Ratio"],
        orientation="h",

        marker=dict(
            color=colors,
            line=dict(
                color="white",
                width=1
            )
        ),

        text=chart_df["Ratio"].round(3),
        textposition="outside",

        hovertemplate=
        "<b>%{y}</b><br>" +
        "비율: %{x:.3f}<extra></extra>"
    )
)

# -----------------------------------
# 그래프 스타일
# -----------------------------------
fig.update_layout(
    title=f"{selected_mbti} 비율 TOP {top_n} 국가",
    template="plotly_white",

    height=650,

    font=dict(
        size=16
    ),

    title_font=dict(
        size=28
    ),

    xaxis=dict(
        title="비율",
        showgrid=True
    ),

    yaxis=dict(
        title="국가",
        autorange="reversed"
    ),

    margin=dict(
        l=40,
        r=40,
        t=80,
        b=40
    ),

    showlegend=False
)

# -----------------------------------
# 그래프 출력
# -----------------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# TOP 국가 카드
# -----------------------------------
st.subheader(f"🏆 {selected_mbti} TOP 국가")

cols = st.columns(top_n)

for idx, (_, row) in enumerate(chart_df.iterrows()):
    with cols[idx]:
        if idx == 0:
            st.success(
                f"🥇 {row['Country']}\n\n{row['Ratio']:.3f}"
            )
        elif idx == 1:
            st.info(
                f"🥈 {row['Country']}\n\n{row['Ratio']:.3f}"
            )
        elif idx == 2:
            st.warning(
                f"🥉 {row['Country']}\n\n{row['Ratio']:.3f}"
            )
        else:
            st.metric(
                row["Country"],
                f"{row['Ratio']:.3f}"
            )

# -----------------------------------
# 데이터 테이블
# -----------------------------------
with st.expander("📋 데이터 보기"):
    st.dataframe(
        chart_df,
        use_container_width=True
    )
