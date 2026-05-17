import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import platform


# 한글 폰트 설정 함수 (OS별 대응)
def set_korean_font():
    system_name = platform.system()
    if system_name == "Windows":
        plt.rc('font', family='Malgun Gothic')
    elif system_name == "Darwin":  # Mac
        plt.rc('font', family='AppleGothic')
    else:  # Linux/Docker 등
        plt.rc('font', family='NanumGothic')

    # 마이너스 기호(-) 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False


def load_data(uploaded_file):
    """업로드된 파일을 데이터프레임으로 변환"""
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")
        return None


def display_heatmap(df):
    """상관계수 히트맵 시각화"""
    st.subheader("📊 상관계수 히트맵")

    # 한글 폰트 적용
    set_korean_font()

    # 수치형 데이터만 추출
    numeric_df = df.select_dtypes(include=['float64', 'int64'])

    if numeric_df.empty:
        st.warning("분석할 수치 데이터가 없습니다.")
        return

    corr = numeric_df.corr()

    # 히트맵 그리기
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='RdBu_r', center=0, ax=ax)
    ax.set_title("주가 종합 상관관계 분석")

    st.pyplot(fig)


def main():
    st.title("📈 주가 상관관계 분석기")

    # 1. 파일 업로드
    st.subheader("📂 파일 업로드")
    uploaded_file = st.file_uploader("CSV 또는 TXT 파일을 업로드하세요.", type=["csv", "txt"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        if df is not None:
            # 2. 파일 내용 보기
            st.subheader("📋 데이터 미리보기")
            st.dataframe(df.head())

            # 3. 히트맵 표시
            display_heatmap(df)


if __name__ == "__main__":
    main()