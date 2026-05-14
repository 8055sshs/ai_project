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
st.title("🌍 MBTI & 국가 분석 대시보드")
st.markdown(
    """
    ✔ 국가 선택 → 해당 국가의 MBTI 비율 확인  
    ✔ MBTI 선택 → 해당 유형 비율이 높은 국가 TOP10 확인
    """
)

# -----------------------------------
# 탭 생성
# -----------------------------------
tab1, tab2 = st.tabs([
    "🌎 국가별 MBTI 보기",
    "🧠 MBTI별 국가 보기"
])

# ==================================================
# TAB 1
# 국가 선택 -> MBTI 비율
# ==================================================
with tab1:

    st.subheader("🌎 국가별 MBTI 비율")

    countries = sorted(df["Country"].unique())

    selected_country = st.selectbox(
        "국가 선택",
        countries
    )

    # 데이터 추출
    country_df = df[df["Country"] == selected_country]

    mbti_cols = [
        col for col in df.columns
        if col != "Country"
    ]

    values = country_df[mbti_cols].iloc[0]

    chart_df = pd.DataFrame({
        "MBTI": mbti_cols,
        "Ratio": values.values
    })

    # 정렬
    chart_df = chart_df.sort_values(
        by="Ratio",
        ascending=False
    ).reset_index(drop=True)

    # 색상
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

    # 그래프
    fig1 = go.Figure()

    fig1.add_trace(
        go.Bar(
            x=chart_df["MBTI"],
            y=chart_df["Ratio"],

            marker=dict(
                color=colors
            ),

            text=chart_df["Ratio"].round(3),
            textposition="outside",

            hovertemplate=
            "<b>%{x}</b><br>" +
            "비율: %{y:.3f}<extra></extra>"
        )
    )

    fig1.update_layout(
        template="plotly_white",
        height=600,

        title=f"{selected_country} MBTI 비율",

        xaxis_title="MBTI",
        yaxis_title="비율",

        showlegend=False
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ==================================================
# TAB 2
# MBTI 선택 -> 국가 TOP10
# ==================================================
with tab2:

    st.subheader("🧠 MBTI별 국가 TOP10")

    mbti_list = [
        col for col in df.columns
        if col != "Country"
    ]

    selected_mbti = st.selectbox(
        "MBTI 선택",
        sorted(mbti_list)
    )

    # 데이터 가공
    mbti_df = df[[
        "Country",
        selected_mbti
    ]].copy()

    mbti_df.columns = [
        "Country",
        "Ratio"
    ]

    mbti_df = mbti_df.sort_values(
        by="Ratio",
        ascending=False
    ).head(10)

    # 색상
    colors2 = []

    for i in range(len(mbti_df)):
        if i == 0:
            colors2.append("#FF3B30")
        else:
            colors2.append(
                blue_gradient[(i - 1) % len(blue_gradient)]
            )

    # 그래프
    fig2 = go.Figure()

    fig2.add_trace(
        go.Bar(
            y=mbti_df["Country"],
            x=mbti_df["Ratio"],

            orientation="h",

            marker=dict(
                color=colors2
            ),

            text=mbti_df["Ratio"].round(3),
            textposition="outside",

            hovertemplate=
            "<b>%{y}</b><br>" +
            "비율: %{x:.3f}<extra></extra>"
        )
    )

    fig2.update_layout(
        template="plotly_white",
        height=700,

        title=f"{selected_mbti} 비율 TOP10 국가",

        xaxis_title="비율",
        yaxis_title="국가",

        yaxis=dict(
            autorange="reversed"
        ),

        showlegend=False
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )
