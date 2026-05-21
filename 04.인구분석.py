import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ---------------------------
# 한글 폰트 설정
# ---------------------------
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ---------------------------
# 데이터 불러오기
# ---------------------------
df = pd.read_csv("population.csv", encoding='utf-8')

st.title("경기도 인구 분석")

# ---------------------------
# 컬럼 확인
# ---------------------------
st.write("데이터 미리보기")
st.dataframe(df.head())

# ---------------------------
# 행정구 선택
# ---------------------------
district_col = df.columns[0]

selected_district = st.selectbox(
    "행정구를 선택하세요",
    df[district_col].unique()
)

# ---------------------------
# 선택된 데이터
# ---------------------------
selected_data = df[df[district_col] == selected_district]

# ---------------------------
# 나이 관련 컬럼 찾기
# ---------------------------
age_columns = []

for col in df.columns:
    if "세" in col:
        age_columns.append(col)

# ---------------------------
# 데이터 준비
# ---------------------------
ages = []
population = []

for col in age_columns:
    try:
        age = col.replace("세", "").replace(" ", "")
        ages.append(age)

        value = selected_data.iloc[0][col]

        if isinstance(value, str):
            value = value.replace(",", "")

        population.append(int(value))

    except:
        pass

# ---------------------------
# 그래프 그리기
# ---------------------------
fig, ax = plt.subplots(figsize=(12, 6))

# 회색 배경
fig.patch.set_facecolor('lightgray')
ax.set_facecolor('lightgray')

# 빨간색 꺾은선 그래프
ax.plot(
    ages,
    population,
    color='red',
    linewidth=2
)

# 제목
ax.set_title("경기도 인구수", fontsize=20)

# 축 제목
ax.set_xlabel("나이")
ax.set_ylabel("인구수")

# x축 글자 회전
plt.xticks(rotation=45)

st.pyplot(fig)
