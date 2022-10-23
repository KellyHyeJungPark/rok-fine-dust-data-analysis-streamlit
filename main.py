import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_agg import RendererAgg
import requests
from streamlit_lottie import st_lottie
from streamlit_folium import st_folium
import folium
import koreanize_matplotlib
from PIL import Image
from glob import glob

st.set_page_config(layout="wide")

# Lottie Icon

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets6.lottiefiles.com/packages/lf20_EyJRUV.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json, speed=1, height=150, key="initial")

# Preparation to display plot

matplotlib.use("agg")
_lock = RendererAgg.lock

# Grid Setup?

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

# Title

row0_1.title("South Korea Fine Dust Concentration Analysis")

with row0_2:
    st.write("")

row0_2.subheader(
    "멋사 AI스쿨 7기 CHILL팀 미세먼지 데이터 분석"
)

# Row No. 1 => Introduction

row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

with row1_1:
    st.markdown(
        "**'조용한 살인자', 미세먼지.**"
    )
    st.markdown(
        "세계보건기구(WHO)는 한 해에 미세먼지로 기대수명보다 일찍 사망하는 사람이 약 700만명에 이른다고 발표했습니다. 국민건강과 생명을 직접적으로 위협하는 미세먼지는 이제 온 국민의 관심사이자 국가적 재난의 문제로 대두되고 있습니다."
    )
    st.markdown(
        "매일 창문을 열어 하늘을 보며 오늘은 하늘이 얼마나 깨끗한 지를 체크하게 되는 요즘, 미세먼지는 이제 우리의 일상이 되었습니다. 특히 환절기에 관련 기사를 많이 찾아볼 수 있는데, 미세먼지의 발생 요인과 미세먼지가 우리 생활과 건강에 얼마나 많은 영향을 끼치는지에 대해 알아보고자 주제로 선정하게 되었습니다."
    )

# Row No. 2 => Topic Selection

row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))
with row2_1:
    topic = st.selectbox(
        "대한민국 미세먼지 관련 주제를 선택하여 주세요.👇",
        [
            "국내 미세먼지 농도",
            "미세먼지와 건강",
            "국외 요인 (중국)",
            "국내 요인",
            "기상 관측 데이터"
        ]
    )

# Import Data

file_dict = {
    "국내 미세먼지 농도" : "misemise",
    "미세먼지와 건강" : "mise_health",
    "국외 요인 (중국)" : "misemise_china",
    "국내 요인" : "misemise_korea",
    "기상 관측 데이터" : "misemise_weather"
}

def get_topic_data(topic_name):
    file_name = f"data/{file_dict[topic_name]}.csv"
    data = pd.read_csv(file_name, encoding='cp949')
    return data

# Display Topic

line1_spacer1, line1_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))

with line1_1:
    st.markdown("***")
    st.header("**{}**".format(topic))
    with st.expander("Analysis 보기 👉"):
        if topic == "국내 미세먼지 농도":
            st.markdown(
                "☑️ 국내 미세먼지 및 초미세먼지에 대한 데이터는 2015년부터 2021년까지 제공되어 있습니다."
            )
            st.markdown(
                "☑️ 월별 평균 농도 분석 시 7~9월인 여름이 다른 시기에 비해 상대적으로 낮은 수치를 보이며, 연도별로 분석 시 최근 미세먼지 및 초미세먼지 농도가 매년 낮아지고 있는 것을 볼 수 있습니다."
            )
            st.markdown(
                "☑️ 미세먼지 및 초미세먼지 농도는 전북 익산시, 충북 청주시, 경기 여수 순으로 가장 높고 인구 밀도가 높은 지역도 상대적으로 높은 수치를 보입니다."
            )
        elif topic == "미세먼지와 건강":
            st.markdown(
                "☑️ **천식 데이터**: 흔히 말하는 알레르기 3대 질환에는 코 속에 나타나는 비염, 기관지에 나타나는 천식, 피부에 나타나는 아토피 피부염이 있다. 미세먼지와 초미세먼지의 농도가 증가할수록 아토피 피부염과 천식 질환 발생률은 높아지는 경향을 보였고, 알레르기 비염 발생률은 반대로 낮아지는 경향을 보였다."
            )
            st.markdown(
                "☑️ **사망 데이터**: 미세먼지로 인해 얻게되는 가장 대표적인 질병으로는 크게 호흡기 질환, 심혈관 질환, 피부 질환 등이 있다. 미세먼지와 초미세먼지 모두 농도가 증가할수록 호흡질환, 순환질환과 피부질환 사망자 수가 낮아지는 경향을 보였다. 조금 더 구체적인 질병과 미세먼지 그리고 초미세먼지의 관계를 살펴보면 아래와 같다. 미세먼지와 초미세먼지 모두 농도가 증가할수록 뇌혈관 질환, 만성 하기도 질환(기관지염, 천식)과 협심증 사망자 수가 증가하는 경향을 보인 반면, 농도가 증가할수록 암, 폐렴과 폐암으로 인한 사망자 수는 낮아지는 것으로 나타났다."
            )
            
        elif topic == "국외 요인 (중국)":
            st.markdown(
                "☑️ 중국과 한국 모두 2015년 부터 미세먼지가 감소하고 있다. 또한 중국의 초미세먼지는 변동폭이 한국 대비 매우 심한 것을 알 수 있었다."
            )
            st.markdown(
                "☑️ 그러나 중국과 한국 미세먼지 사이 유의미한 상관관계를 찾아내지 못 했다. 중국의 환경 요인이 미세먼지에 미치는 영향은 밝혀내지 못 했다. 따라서 '중국이 한국의 미세먼지에 큰 영향을 미칠 것이다.'라는 가설을 증명하는데 실패했다."
            )
        elif topic == "국내 요인":
            st.markdown(
                "☑️ 미세먼지를 많이 배출하는 내륙지역은 경상북도, 충청남도, 경기도, 전라남도로 밝혀졌고, 비산먼지와 제조업 연소의 배출이 주로 발견됐다."
            )
            st.markdown(
                "☑️ 비산먼지는 자동차 주행거리와 관련을 보였고, 제조업 연소는 석탄의 에너지 소비량이 많은 1차철강제조업과 관계가 있었다."
            )
        elif topic == "기상 관측 데이터":
            st.markdown(
                "☑️ **기온, 지면온도**와 미세먼지는 약한 음의 상관관계"
            )
            st.markdown(
                "☑️ **강수량**과 미세먼지는 약한 음의 상관관계"
            )
            st.markdown(
                "☑️ **적설량**은 겨울에만 봤을 때는 미세먼지와 음의 관계"
            )
            st.markdown(
                "☑️ **풍속**과 미세먼지는 약한 음의 상관관계"
            )
            st.markdown(
                "☑️ **습도**와 미세먼지는 약한 음의 상관관계"
            )
            st.markdown(
                "☑️ **운량**과 미세먼지는 약한 음의 상관관계"
            )
            st.markdown(
                "☑️ **현지기압**과 미세먼지는 약한 양의 상관관계"
            )
            st.markdown(
                "☑️ **증기압**과 미세먼지는 약한 음의 상관관계"
            )

    st.markdown("")

# Load Data

data = get_topic_data(topic)

# Display Data Set

row3_space1, row3_1, row3_space2 = st.columns(
    (0.1, 1, 0.1)
)

with row3_1, _lock:
    st.subheader("DataSet")
    data_load_state = st.text('Loading data...⏳')
    with st.expander("DataSet 보기 👉"):
        if topic == "미세먼지와 건강":
            st.markdown("진료율")
            st.dataframe(data)

            data3 = pd.read_csv("data/mise_health_disease.csv", encoding='cp949')
            st.markdown("사망 수")
            st.dataframe(data3)
        else:
            st.dataframe(data)
    data_load_state.text("")

line2_spacer1, line2_1, line2_spacer2 = st.columns((0.1, 3.2, 0.1))

with line2_1:
    st.header("")

# Visualization (Different Based on Topics)
row4_space1, row4_1, row4_space2 = st.columns(
    (0.1, 1, 0.1)
)

with row4_1, _lock:
    st.subheader("Data Visualization")
    viz_load_state = st.text('Please Wait! Visualization Loading...⏳')
    ####################################
    # Topic No.1
    if topic == "국내 미세먼지 농도":
        with st.expander("Visualization 보기 👉"):
            # Default Variables
            x_val = "연도"
            x_label = "Year"
            y_val = "PM10"
            y_label = "PM10 Concentration"

            # Personalized Settings Options
            settings = st.checkbox('설정 바꾸기')
            if settings:
                st.sidebar.markdown("X-축")
                time = st.sidebar.checkbox('시간별')
                if time:
                    selected_time = st.sidebar.selectbox("",
                        [
                            "연도",
                            "월",
                            "일"
                        ]
                    )
                    x_val = selected_time
                    x_label = {"연도":"Year", "월":"Month", "일":"Day"}[selected_time]

                selected_y = st.sidebar.selectbox("Y-축",
                        [
                            "PM10",
                            "PM25"
                        ]
                    )
                y_val = selected_y
                y_label = {"PM10":"Fine Dust PM10", "PM25":"Ultra Fine Dust PM2.5"}[selected_y]
            
            # Graph Visualization => Seaborn
            st.markdown("미세먼지 농도")
            fig, ax = plt.subplots()
            sns.barplot(
                    data=data, x=x_val, y=y_val, errorbar=None, palette="RdPu"
                )
            ax.set_title("")
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            st.pyplot(fig)

            fig2, ax2 = plt.subplots()
            sns.lineplot(
                    data=data, x=x_val, y=y_val, color="red"
                )
            ax2.set_title("")
            ax2.set_xlabel(x_label)
            ax2.set_ylabel(y_label)
            st.pyplot(fig2)

            # Top 20 Locations
            st.markdown("미세먼지 농도가 가장 높은 지역 20")
            st.bar_chart(data.groupby(['지역'])['PM10','PM25'].mean().sort_values(['PM10','PM25'], ascending=False).head(20))

        # Folium Visualization
        with st.expander("Folium Visualization 보기 👉"):
            file_name = "data/misemise_folium.csv"
            data_fol = pd.read_csv(file_name, encoding='cp949')

            m = folium.Map(location=[36,127],tiles='openstreetmap', zoom_start=7)

            choropleth = folium.Choropleth(
                geo_data='data/sigshp.json', # 경계선 좌표값이 담긴 데이터
                data=data_fol, # Series or DataFrame 넣으면 된다
                columns=('시군구', 'PM10'), # DataFrame의 어떤 columns을 넣을지
                key_on='feature.id', # id 값을 가져오겠다; feature.id : feature 붙여줘야 함 (folium의 정해진 형식)
                fill_color='YlOrRd',
                fill_opacity=0.7, # 색 투명도
                line_opacity=0.5, # 선 투명도
                legend_name='미세먼지 농도 ㎍/m^3' # 범례
            ).add_to(m)
            
            st.data = st_folium(m)
        viz_load_state.text("")
    ####################################
    # Topic No.2
    elif topic == "미세먼지와 건강":
        with st.expander("Visualization 보기 👉"):

            data2 = data.drop(columns=['아토피피부염','알레르기비염'])
            data2 = data2.melt(id_vars=['연도','천식'],var_name='종류',value_name='농도')
            data["연도"] = data["연도"].astype("str")

            # Graph Visualization => Seaborn
            fig, ax1 = plt.subplots(1,1, sharex=True)
            sns.barplot(
                    ax=ax1, data=data2, x='연도', y='농도', hue='종류', palette=['yellow','orange'], errorbar=None
                )
            ax2 = ax1.twinx()
            sns.lineplot(
                    ax=ax2, data=data, x='연도', y='천식', color="red"
                )
            ax2.set_ylim(0, 12)
            st.pyplot(fig)

            # Correlation Visualization => Seaborn
            corr = data.corr()
            mask = np.triu(np.ones_like(corr))
            fig2, ax3 = plt.subplots()
            sns.heatmap(corr, annot=True, fmt=".2f", cmap = "coolwarm", vmin=-1, vmax=1, mask=mask)
            st.pyplot(fig2)

            # Additional Visualization
            data4 = data3.drop(columns=['각종 암','뇌혈관 질환','순환 질환','폐렴','폐암','피부 질환','협심증','호흡 질환'])
            data4 = data4.melt(id_vars=['연도','만성 하기도 질환'],var_name='종류',value_name='농도')
            data3["연도"] = data3["연도"].astype("str")

            fig3, ax4 = plt.subplots(1,1, sharex=True)
            sns.barplot(
                    ax=ax4, data=data4, x='연도', y='농도', hue='종류', palette=['yellow','orange'], errorbar=None
                )
            ax5 = ax4.twinx()
            sns.lineplot(
                    ax=ax5, data=data3, x='연도', y='만성 하기도 질환', color="red"
                )
            ax5.set_ylim(0,700)
            st.pyplot(fig3)

            df_c = data3.corr()
            mask2 = np.triu(np.ones_like(df_c))
            fig3 = plt.figure(figsize=(10, 6))
            sns.heatmap(df_c, annot=True, fmt=".2f", cmap = "coolwarm", vmin=-1, vmax=1, mask=mask2);
            st.pyplot(fig3)
        viz_load_state.text("")
    ####################################
    # Topic No.3
    elif topic == "국외 요인 (중국)":
        with st.expander("Visualization 보기 👉"):
            file_name = glob("image/china/*.png")
            for fn in file_name:
                image = Image.open(fn)
                st.image(image)
        viz_load_state.text("")
    ####################################
    # Topic No.4
    elif topic == "국내 요인":
        with st.expander("Visualization 보기 👉"):
            file_name = glob("image/korea/*.png")
            for fn in file_name:
                image = Image.open(fn)
                st.image(image)
        viz_load_state.text("")    
    ####################################
    # Topic No.5
    elif topic == "기상 관측 데이터":
        with st.expander("Visualization 보기 👉"):
            file_name = glob("image/weather/*.png")
            for fn in file_name:
                image = Image.open(fn)
                st.image(image)
        viz_load_state.text("")

# Footers

line3_spacer1, line3_1, line3_spacer2 = st.columns((0.1, 3.2, 0.1))

with line3_1:
    st.header("")

row5_space1, row5_1, row5_space2 = st.columns(
    (0.1, 3.2, 0.1)
)

with row5_1:
    st.markdown("***")
    st.markdown(
        "멋쟁이사자처럼 AI 스쿨 7기 미드프로젝트"
    )
    st.markdown(
        "7 CHILL 팀 - 미세먼지 데이터 분석"
    )
    st.markdown(
        "김의준, 박혜정, 강기화, 권태윤, 장우석"
    )
    st.markdown(
        "2022년 10월 19일 ~ 23일"
    )