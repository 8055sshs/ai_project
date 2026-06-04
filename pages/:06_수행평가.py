import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="전국 카페 분석",
    page_icon="☕",
    layout="wide"
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        "전국카페표준데이터.csv",
        encoding="cp949"
    )

df = load_data()

# -----------------------------
# 제목
# -----------------------------
st.title("☕ 전국 카페 데이터 분석 대시보드")
st.markdown("---")

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("필터")

sido_list = ["전체"] + sorted(df["시도명"].dropna().unique())

selected_sido = st.sidebar.selectbox(
    "시도 선택",
    sido_list
)

if selected_sido == "전체":
    filtered_df = df.copy()
else:
    filtered_df = df[df["시도명"] == selected_sido]

sigungu_list = ["전체"] + sorted(
    filtered_df["시군구명"].dropna().unique()
)

selected_sigungu = st.sidebar.selectbox(
    "시군구 선택",
    sigungu_list
)

if selected_sigungu != "전체":
    filtered_df = filtered_df[
        filtered_df["시군구명"] == selected_sigungu
    ]

# -----------------------------
# KPI
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "전체 카페 수",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "시도 수",
        filtered_df["시도명"].nunique()
    )

with col3:
    st.metric(
        "시군구 수",
        filtered_df["시군구명"].nunique()
    )

st.markdown("---")

# -----------------------------
# 시도별 카페 수
# -----------------------------
st.subheader("📊 시도별 카페 수")

count_sido = (
    filtered_df
    .groupby("시도명")
    .size()
    .reset_index(name="카페수")
    .sort_values("카페수", ascending=False)
)

fig1 = px.bar(
    count_sido,
    x="시도명",
    y="카페수",
    text="카페수",
    height=500
)

fig1.update_layout(
    xaxis_title="시도",
    yaxis_title="카페 수"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -----------------------------
# 상위 10개 시군구
# -----------------------------
st.subheader("🏆 카페가 많은 시군구 TOP 10")

top10 = (
    filtered_df
    .groupby("시군구명")
    .size()
    .reset_index(name="카페수")
    .sort_values("카페수", ascending=False)
    .head(10)
)

fig2 = px.bar(
    top10,
    x="카페수",
    y="시군구명",
    orientation="h",
    text="카페수",
    height=600
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------
# 지도
# -----------------------------
st.subheader("🗺️ 카페 위치 지도")

map_df = filtered_df.dropna(
    subset=["위도", "경도"]
)

if len(map_df) > 3000:
    map_df = map_df.sample(3000)

fig_map = px.scatter_map(
    map_df,
    lat="위도",
    lon="경도",
    hover_name="사업장명",
    zoom=5,
    height=700
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# -----------------------------
# 검색
# -----------------------------
st.subheader("🔍 카페 검색")

keyword = st.text_input(
    "카페 이름 입력"
)

if keyword:
    search_df = filtered_df[
        filtered_df["사업장명"]
        .str.contains(keyword, na=False)
    ]

    st.write(f"검색 결과 : {len(search_df)}개")

    st.dataframe(
        search_df[
            [
                "사업장명",
                "시도명",
                "시군구명",
                "소재지도로명주소"
            ]
        ],
        use_container_width=True
    )

# -----------------------------
# 원본 데이터
# -----------------------------
st.subheader("📄 데이터")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -----------------------------
# 다운로드
# -----------------------------
csv = filtered_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    "⬇️ CSV 다운로드",
    csv,
    "cafe_data.csv",
    "text/csv"
)
