import streamlit as st
import pandas as pd
import math
import random
import base64
import os
import streamlit.components.v1 as components

# ----------------------------------------------------------------
# 1. 페이지 기본 설정 및 커스텀 CSS (여의도 테마 & Glassmorphism)
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Professional 회계 대시보드", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
import base64

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# 깃헙 연동 및 배포(Streamlit Cloud)를 위해 스크립트 기준 절대 경로로 변경
script_dir = os.path.dirname(os.path.abspath(__file__))
bg_image_path = os.path.join(script_dir, 'static', 'yeouido_background.png')
bg_b64 = get_base64_of_bin_file(bg_image_path)

# Custom CSS 주입 (프리미엄 여의도 테마)
st.markdown(f"""
    <style>
    /* 전체 배경 초기화 (깔끔한 라이트/다크 그레이톤) */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
        background-color: #F8FAFC !important;
    }}
    
    /* 헤더 투명화 및 클릭 방해 방지 */
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
        pointer-events: none !important;
    }}
    [data-testid="stHeader"] * {{
        pointer-events: auto;
    }}
    
    /* 사이드바 글래스모피즘 (다크) */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(10px);
    }}
    [data-testid="stSidebar"] * {{
        color: rgba(255,255,255,0.9) !important;
    }}

    /* 메인 컨텐츠 영역 디자인 복원 (깔끔한 카드 스타일) */
    .block-container {{
        background: #FFFFFF;
        border-radius: 0px;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}

    /* 메인 타이틀 폰트 및 여백 */
    .main-title {{
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
    }}
    .sub-title {{
        font-size: 1.15rem;
        color: #475569;
        margin-bottom: 2rem;
        font-weight: 500;
    }}
    /* 메트릭(결과값) 강조 */
    [data-testid="stMetricValue"] {{
        font-size: 2.5rem !important;
        color: #0F172A !important;
        font-weight: 800 !important;
    }}
    /* 버튼 호버 애니메이션 */
    .stButton>button {{
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
        background-color: #1E3A8A;
        color: white;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(30, 58, 138, 0.3);
        background-color: #1E40AF;
        color: white;
    }}
    /* 탭 디자인 고급화 및 상단 우측 고정 (White Navbar) */
    @keyframes fadeInHero {{
        0% {{ opacity: 0; transform: translateY(20px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes popupSlide {{
        0% {{ transform: translateX(-150%); opacity: 0; }}
        10% {{ transform: translateX(0); opacity: 1; }}
        80% {{ transform: translateX(0); opacity: 1; }}
        100% {{ transform: translateX(-150%); opacity: 0; }}
    }}
    
    @keyframes fadeInContent {{
        0% {{ opacity: 0; transform: translateY(15px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    
    [data-baseweb="tab-panel"] {{
        animation: fadeInContent 0.6s ease-out forwards;
    }}
    
    [data-testid="stTabs"] {{
        /* z-index 버그 해결을 위해 position 제거 */
    }}
    [data-baseweb="tab-list"] {{
        gap: clamp(5px, 1.5vw, 20px);
        position: fixed;
        top: 1.2rem;
        right: clamp(1rem, 5vw, 15vw);
        z-index: 99990 !important;
        pointer-events: auto !important;
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        max-width: 65vw; /* 로고와 겹침 방지 */
    }}
    /* 웹킷 스크롤바 숨김 (가로 스크롤이 생겨도 깔끔하게) */
    [data-baseweb="tab-list"]::-webkit-scrollbar {{
        display: none;
    }}
    [data-baseweb="tab"] {{
        border-radius: 0 !important;
        padding: 5px clamp(2px, 0.8vw, 10px);
        background-color: transparent !important;
        border: none !important;
        color: #334155 !important;
        font-weight: 700;
        font-size: clamp(0.75rem, 1vw, 1.05rem);
        white-space: nowrap !important;
    }}
    [data-baseweb="tab"]:hover {{
        color: #1E3A8A !important;
    }}
    [data-baseweb="tab"][aria-selected="true"] {{
        color: #0F172A !important;
    }}
    div[data-baseweb="tab-border"] {{
        display: none !important;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: #0F172A !important;
    }}
    /* 컨테이너 보더 수정 */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: rgba(0,0,0,0.1) !important;
        background-color: rgba(255,255,255,0.6);
        border-radius: 12px;
    }}
    </style>
""", unsafe_allow_html=True)
hero_html = f"""
<!-- 흰색 고정 네비게이션 바 -->
<div style="position: fixed; top: 0; left: 0; width: 100vw; height: 4.5rem; background-color: white; z-index: 99990; box-shadow: 0 2px 10px rgba(0,0,0,0.05); pointer-events: none;"></div>
<!-- 좌측 상단 로고 -->
<div style="position: fixed; top: 1.2rem; left: 5vw; z-index: 99991; font-size: 1.5rem; font-weight: 900; color: #1E3A8A; letter-spacing: 1px; pointer-events: none;">
JH ACCOUNTING
</div>

<div style="background-image: linear-gradient(rgba(15, 23, 42, 0.7), rgba(15, 23, 42, 0.7)), url('data:image/png;base64,{bg_b64}'); background-size: cover; background-position: center; width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; margin-top: -1rem; padding: 8rem 2rem 5rem 2rem; margin-bottom: 3rem; box-shadow: 0 10px 25px rgba(0,0,0,0.2); color: white; text-align: center;">
<div style="font-size: clamp(2.5rem, 5vw, 4.5rem); font-weight: 900; margin-bottom: 1rem; text-shadow: 0 4px 6px rgba(0,0,0,0.3); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-top: 1rem; animation: fadeInHero 1.5s ease-out forwards;">
당신의 회계를 더 효율적으로
</div>
<div style="font-size: 1.25rem; font-weight: 400; color: rgba(255,255,255,0.85); margin-bottom: 2rem;">
대한민국 금융의 중심, 여의도 스탠다드의 강력한 실무 재무 툴킷.
</div>
</div>

<!-- 사이드바 유도 팝업 토스트 (좌측) -->
<div style="position: fixed; top: 6rem; left: 1.5rem; z-index: 999999; background: rgba(15, 23, 42, 0.95); color: white; padding: 1rem 1.5rem; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15); animation: popupSlide 7s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; font-size: 0.95rem; font-weight: 500; pointer-events: none; backdrop-filter: blur(10px);">
    💡 <b>Tip:</b> 화면 왼쪽 〉버튼을 누르면 프리미엄 계산기를 쓸 수 있습니다!
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)


# ----------------------------------------------------------------
# 2. 사이드바 - 상시 단순 계산기
# ----------------------------------------------------------------
with st.sidebar:
    st.header("🧮 프리미엄 재무 계산기")
    st.caption("공학용 기능 및 계산 히스토리 지원")
    
    calc_html_path = os.path.join(script_dir, 'calculator-1.html')
    with open(calc_html_path, "r", encoding="utf-8") as f:
        calc_html = f.read()
        
    components.html(calc_html, height=850, scrolling=True)

# ----------------------------------------------------------------
# 3. 메인 화면 탭(Tabs) 레이아웃 구성
# ----------------------------------------------------------------
tab1, tab_pva, tab2, tab3, tab4, tab5 = st.tabs([
    "현재가치(PV) 계산", 
    "연금 현재가치(PVA) 계산",
    "감가상각비 계산", 
    "사채 발행금액 계산", 
    "퇴직연금 시뮬레이터",
    "실전 재무 퀴즈"
])

# ==========================================
# TAB 1: 현재가치(PV) 계산기
# ==========================================
with tab1:
    st.subheader("📉 자산 현재가치(PV) 산출")
    st.write("미래의 현금흐름을 현재가치로 할인하여 평가합니다.")
    
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            fv = st.number_input("미래가치 (FV)", value=1000000, step=10000)
        with col2:
            r_percent = st.number_input("할인율 (%, r)", value=5.0, step=0.1)
            r = r_percent / 100
        with col3:
            n = st.number_input("기간 (년, n)", value=1, step=1)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("PV 산출 실행", type="primary"):
            pv = fv / ((1 + r) ** n)
            st.success("계산이 완료되었습니다.")
            st.metric(label="자산의 현재가치 (Present Value)", value=f"₩ {pv:,.0f}")

# ==========================================
# TAB 1.5: 연금 현재가치(PVA) 계산기
# ==========================================
with tab_pva:
    st.subheader("💵 연금 현재가치(PVA) 산출")
    st.write("매기 일정한 금액(연금)이 발생할 때, 그 전체 현금흐름의 현재가치를 평가합니다.")
    
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            pmt = st.number_input("매기 수령액 (PMT)", value=1000000, step=10000, key="pva_pmt")
        with col2:
            r_percent_pva = st.number_input("할인율 (%, r)", value=5.0, step=0.1, key="pva_r")
            r_pva = r_percent_pva / 100
        with col3:
            n_pva = st.number_input("기간 (년, n)", value=10, step=1, key="pva_n")
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("PVA 산출 실행", type="primary", key="btn_pva"):
            if r_pva == 0:
                pva = pmt * n_pva
            else:
                pva = pmt * ((1 - (1 + r_pva) ** -n_pva) / r_pva)
            st.success("계산이 완료되었습니다.")
            st.metric(label="연금의 현재가치 (Present Value of Annuity)", value=f"₩ {pva:,.0f}")

# ==========================================
# TAB 2: 감가상각비 계산기
# ==========================================
with tab2:
    st.subheader("🏭 유형자산 감가상각비 계산")
    
    with st.container(border=True):
        method = st.selectbox("감가상각 방법 선택", [
            "정액법 (Straight-line)", 
            "정률법 (Declining balance)",
            "연수합계법 (Sum-of-the-years'-digits)",
            "생산량 비례법 (Units-of-production)"
        ])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cost = st.number_input("취득원가 (₩)", value=10000000, step=1000000)
        with col2:
            salvage = st.number_input("잔존가치 (₩)", value=1000000, step=100000)
        with col3:
            if method == "생산량 비례법 (Units-of-production)":
                total_units = st.number_input("총 추정 생산량", value=10000, step=1000)
            else:
                life = st.number_input("내용연수 (년)", value=5, step=1)
                
        if method == "생산량 비례법 (Units-of-production)":
            production_input = st.text_input(
                "연도별 당기 생산량 (쉼표로 구분하여 순서대로 입력해 주세요)", 
                "2000, 3000, 4000, 1000"
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("감가상각 상각표 생성", type="primary"):
            data = []
            book_value = cost
            
            if method == "정액법 (Straight-line)":
                annual_depreciation = (cost - salvage) / life
                st.info(f"💡 정액법 기준 매년 감가상각비: **₩ {annual_depreciation:,.0f}**")
                for year in range(1, life + 1):
                    book_value -= annual_depreciation
                    data.append({"연도": f"{year}년차", "감가상각비": int(annual_depreciation), "장부금액(기말)": int(book_value)})
                    
            elif method == "정률법 (Declining balance)":
                if salvage <= 0:
                    st.error("정률법 계산을 위해서는 잔존가치가 0보다 커야 합니다.")
                else:
                    rate = 1 - math.pow(salvage / cost, 1 / life)
                    st.info(f"💡 자동 계산된 상각률: **{rate*100:.2f}%**")
                    for year in range(1, life + 1):
                        depreciation = book_value * rate
                        book_value -= depreciation
                        data.append({"연도": f"{year}년차", "감가상각비": int(depreciation), "장부금액(기말)": int(book_value)})
                        
            elif method == "연수합계법 (Sum-of-the-years'-digits)":
                sum_years = life * (life + 1) / 2
                for year in range(1, life + 1):
                    fraction = (life - year + 1) / sum_years
                    depreciation = (cost - salvage) * fraction
                    book_value -= depreciation
                    data.append({"연도": f"{year}년차", "감가상각비": int(depreciation), "장부금액(기말)": int(book_value)})
                    
            elif method == "생산량 비례법 (Units-of-production)":
                try:
                    productions = [int(p.strip()) for p in production_input.split(',')]
                    unit_depreciation = (cost - salvage) / total_units
                    for i, prod in enumerate(productions):
                        year = i + 1
                        depreciation = prod * unit_depreciation
                        book_value -= depreciation
                        data.append({"연도": f"{year}년차", "당기 생산량": prod, "감가상각비": int(depreciation), "장부금액(기말)": int(book_value)})
                except ValueError:
                    st.error("연도별 생산량은 숫자와 쉼표(,)로만 정확히 입력해 주세요.")

            if data:
                df = pd.DataFrame(data)
                
                with st.container(border=True):
                    st.write("#### 📊 감가상각 상각표")
                    st.dataframe(df, use_container_width=True)
                    
                    st.write("#### 📈 감가상각비 및 장부금액 추세")
                    col_chart1, col_chart2 = st.columns(2)
                    with col_chart1:
                        st.caption("연도별 감가상각비 (막대 그래프)")
                        st.bar_chart(df.set_index("연도")["감가상각비"])
                    with col_chart2:
                        st.caption("연도별 장부금액(기말) (꺾은선 그래프)")
                        st.line_chart(df.set_index("연도")["장부금액(기말)"])

# ==========================================
# TAB 3: 사채 발행금액 및 상각표 계산기
# ==========================================
with tab3:
    st.subheader("📑 사채 발행금액 및 유효이자율 상각표")
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            face_value = st.number_input("액면가액 (₩)", value=10000000, step=1000000, key="bond_face")
            coupon_rate_pct = st.number_input("액면이자율 (%)", value=5.0, step=0.5, key="bond_coupon")
        with col2:
            market_rate_pct = st.number_input("시장이자율 (유효이자율) (%)", value=6.0, step=0.5, key="bond_market")
            life_bond = st.number_input("만기 (년)", value=3, step=1, key="bond_life")
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("사채 발행 분석 실행", type="primary"):
            r = market_rate_pct / 100
            n = life_bond
            coupon_interest = face_value * (coupon_rate_pct / 100)
            
            pv_principal = face_value / ((1 + r) ** n)
            if r == 0: pv_interest = coupon_interest * n
            else: pv_interest = coupon_interest * ((1 - (1 + r) ** -n) / r)
                
            issuance_price = pv_principal + pv_interest
            
            with st.container(border=True):
                st.metric(label="💰 최초 사채 발행가액", value=f"₩ {issuance_price:,.0f}")
                
                if coupon_rate_pct > market_rate_pct:
                    st.success("상태: **할증발행(Premium)** (액면이자율 > 시장이자율)")
                elif coupon_rate_pct < market_rate_pct:
                    st.warning("상태: **할인발행(Discount)** (액면이자율 < 시장이자율)")
                else:
                    st.info("상태: **액면발행(Par)** (액면이자율 = 시장이자율)")
                
            amortization_data = []
            book_value = issuance_price
            
            amortization_data.append({
                "연도": "발행일", "기초 장부금액": "-", "유효이자 (이자비용)": "-", 
                "액면이자 (지급액)": "-", "상각액": "-", "기말 장부금액": int(book_value)
            })
            
            for year in range(1, int(n) + 1):
                beginning_bv = book_value
                interest_expense = beginning_bv * r
                amortization = abs(interest_expense - coupon_interest)
                
                if coupon_rate_pct < market_rate_pct: book_value += amortization
                elif coupon_rate_pct > market_rate_pct: book_value -= amortization
                    
                if year == int(n):
                    amortization += (face_value - book_value)
                    book_value = face_value
                    if coupon_rate_pct < market_rate_pct: interest_expense = coupon_interest + amortization
                    else: interest_expense = coupon_interest - amortization

                amortization_data.append({
                    "연도": f"{year}년차", "기초 장부금액": int(beginning_bv),
                    "유효이자 (이자비용)": int(interest_expense), "액면이자 (지급액)": int(coupon_interest),
                    "상각액": int(amortization), "기말 장부금액": int(book_value)
                })
                
            df_amort = pd.DataFrame(amortization_data)
            
            with st.container(border=True):
                st.write("#### 📅 유효이자율법 사채 상각표")
                st.dataframe(df_amort, use_container_width=True)
                st.write("#### 📉 기말 장부금액 변동 추이")
                chart_df = df_amort.iloc[1:].set_index("연도")["기말 장부금액"]
                st.line_chart(chart_df)

# ==========================================
# TAB 4: 퇴직금 및 퇴직연금(DB/DC) 시뮬레이터
# ==========================================
with tab4:
    st.subheader("💼 퇴직금 및 퇴직연금(DB/DC) 시뮬레이터")
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### 🗓️ 기본 정보")
            join_date = st.date_input("입사일 (또는 기산일)", pd.to_datetime("2020-01-01"))
            retire_date = st.date_input("퇴사(예정)일", pd.to_datetime("2030-12-31"))
            
        with col2:
            st.markdown("##### 💰 급여 및 투자 정보")
            monthly_salary = st.number_input("퇴직 직전 평균 월급여 (₩)", value=3000000, step=100000)
            dc_yield_pct = st.number_input("DC형 예상 연평균 운용수익률 (%)", value=5.0, step=0.5)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("시뮬레이션 실행 🚀", type="primary"):
            total_days = (retire_date - join_date).days
            working_years = total_days / 365.25 
            
            if working_years < 1:
                st.error("🚨 근속 기간이 1년 미만이라 퇴직금 지급 대상이 아닙니다!")
            else:
                db_severance_pay = monthly_salary * working_years
                r = dc_yield_pct / 100
                n = int(working_years)
                
                if r > 0: dc_severance_pay = monthly_salary * (((1 + r)**working_years - 1) / r)
                else: dc_severance_pay = monthly_salary * working_years
                
                with st.container(border=True):
                    st.markdown("#### 📊 시뮬레이션 결과")
                    col_res1, col_res2, col_res3 = st.columns(3)
                    with col_res1: st.metric(label="총 근속연수", value=f"{working_years:.1f}년")
                    with col_res2: st.metric(label="🏢 DB형 (법정 퇴직금)", value=f"₩ {db_severance_pay:,.0f}")
                    with col_res3: st.metric(label=f"📈 DC형 (수익률 {dc_yield_pct}%)", value=f"₩ {dc_severance_pay:,.0f}")
                
                with st.container(border=True):
                    st.write("#### 📈 근속 연수에 따른 자산 성장 추이 비교")
                    growth_data = []
                    for year in range(1, n + 1):
                        db_val = monthly_salary * year
                        if r > 0: dc_val = monthly_salary * (((1 + r)**year - 1) / r)
                        else: dc_val = monthly_salary * year
                            
                        growth_data.append({
                            "근속연수": f"{year}년차",
                            "DB형 (예상액)": int(db_val),
                            "DC형 (운용 결과)": int(dc_val)
                        })
                        
                    df_growth = pd.DataFrame(growth_data)
                    st.line_chart(df_growth.set_index("근속연수"))
                    st.info("💡 **가이드:** 임금상승률이 높을 것으로 예상되면 **DB형**이, 본인의 투자 수익률이 임금상승률을 상회할 것으로 예상되면 **DC형**이 유리합니다.")

# ==========================================
# TAB 5: 실전 재무/회계 무한 트레이닝
# ==========================================
with tab5:
    st.subheader("📝 실전 재무/회계 트레이닝 존")
    st.write("수치가 무작위로 변경되는 실전형 퀴즈입니다. 직접 계산하며 실무 감각을 키워보세요.")

    def reset_quiz():
        st.session_state.generate_new = True
        if "user_ans_input" in st.session_state:
            st.session_state.user_ans_input = ""

    if 'generate_new' not in st.session_state:
        st.session_state.generate_new = True

    if st.session_state.generate_new:
        problem_type = random.choice(["감가상각비", "사채발행"])
        
        if problem_type == "감가상각비":
            cost = random.randint(50, 200) * 100000
            salvage = random.randint(5, 20) * 100000
            life = random.choice([3, 5, 10])
            method = random.choice(["정액법", "연수합계법"])
            target_year = random.randint(1, life)
            
            if method == "정액법": ans = (cost - salvage) / life
            else:
                sum_years = life * (life + 1) / 2
                fraction = (life - target_year + 1) / sum_years
                ans = (cost - salvage) * fraction
                
            st.session_state.correct_ans = int(ans)
            st.session_state.q_text = f"""
**[(주)한국 - 유형자산 감가상각]**
* **취득원가:** {cost:,.0f}원
* **잔존가치:** {salvage:,.0f}원
* **내용연수:** {life}년
* **상각방법:** {method}

위 조건일 때, **제{target_year}기(년차)에 인식할 감가상각비**는 얼마입니까? (소수점 이하 버림)
"""
        else:
            face = random.randint(10, 100) * 1000000 
            coupon = random.choice([4, 5, 6, 8, 10]) 
            market = random.choice([4, 5, 6, 8, 10, 12]) 
            life = random.choice([2, 3, 5])
            bond_question_type = random.choice(["발행가액", "이자비용"])
            
            r = market / 100
            coupon_interest = face * (coupon / 100)
            pv_principal = face / ((1 + r) ** life)
            
            if r == 0: pv_interest = coupon_interest * life
            else: pv_interest = coupon_interest * ((1 - (1 + r) ** -life) / r)
                
            issuance_price = pv_principal + pv_interest
            
            if bond_question_type == "발행가액":
                ans = issuance_price
                question_detail = "**사채의 최초 발행가액(현재가치)**은 얼마입니까?"
            else:
                ans = issuance_price * r
                question_detail = "**1차 연도 말에 포괄손익계산서에 인식할 이자비용**은 얼마입니까?"
            
            st.session_state.correct_ans = int(ans)
            st.session_state.q_text = f"""
**[(주)대한 - 사채 발행 및 이자비용]**
* **액면가액:** {face:,.0f}원
* **만기:** {life}년
* **액면이자율:** 연 {coupon}%
* **시장이자율(유효이자율):** 연 {market}%

위 조건으로 사채를 발행했을 때, {question_detail} (소수점 이하 버림)
"""
        st.session_state.generate_new = False

    with st.container(border=True):
        st.markdown("#### 🎯 오늘의 훈련 문제")
        st.info(st.session_state.q_text)
        
        user_input = st.text_input("정답 입력 (숫자만 기입해 주세요):", key="user_ans_input")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("정답 확인 ✔️", type="primary", use_container_width=True):
                cleaned_input = user_input.replace(",", "").replace(" ", "").strip()
                if cleaned_input == str(st.session_state.correct_ans):
                    st.success("🎉 완벽합니다! 실전 회계 계산을 정확하게 해내셨습니다.")
                elif not cleaned_input:
                    st.warning("정답을 먼저 입력해 주십시오.")
                else:
                    st.error(f"❌ 틀렸습니다. 정답은 **{st.session_state.correct_ans:,}**원 입니다. 다시 한번 계산해 보세요!")
                    
        with col_btn2:
            st.button("새로운 문제 생성 🔄", on_click=reset_quiz, use_container_width=True)
