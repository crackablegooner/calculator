import streamlit as st
import math, cmath, statistics, numpy as np
import sympy as sp
import plotly.graph_objs as go

# ──────────────────────────────────────────
# 공통 설정 & 세션 메모리 ------------------------------------
st.set_page_config("올인원 계산기 🧮", page_icon="🧮", layout="centered")

if "memory" not in st.session_state:    # M+, M-, MR용
    st.session_state.memory = 0.0

# ──────────────────────────────────────────
# 1) 기본/삼각/쌍곡/팩토리얼/제곱근 ---------------------------
def basic_trig_hypo():
    st.header("① 일반 · 삼각 · 쌍곡 · 팩토리얼 · 제곱근")

    mode = st.selectbox(
        "카테고리",
        ["사칙/모듈러/지수/로그", "삼각함수", "쌍곡함수", "팩토리얼", "n 제곱근"]
    )

    if mode == "사칙/모듈러/지수/로그":
        op = st.selectbox("연산",
                          ["+", "-", "×", "÷", "%", "^", "log"])
        if op == "log":
            x = st.number_input("x (양수)", 1.0)
            base = st.number_input("밑 (양수, 1 제외)", 10.0)
            if st.button("계산"):
                try:
                    st.success(f"log_{base}({x}) = {math.log(x, base)}")
                except ValueError:
                    st.error("x, 밑 모두 양수 · 밑 ≠ 1")
        else:
            a = st.number_input("a", 0.0); b = st.number_input("b", 0.0)
            if st.button("계산"):
                try:
                    res = {
                        "+": a + b, "-": a - b, "×": a * b,
                        "÷": a / b, "%": a % b, "^": a ** b
                    }[op]
                    st.success(f"결과: {res}")
                except ZeroDivisionError:
                    st.error("0으로 나눌 수 없습니다.")

    elif mode == "삼각함수":
        ang = st.number_input("각도 입력", 0.0)
        unit = st.radio("단위", ["Degree", "Radian"])
        rad = math.radians(ang) if unit == "Degree" else ang
        func = st.selectbox("함수", ["sin", "cos", "tan"])
        if st.button("계산"):
            val = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[func](rad)
            st.success(f"{func}({ang}{'°' if unit=='Degree' else ''}) = {val}")

    elif mode == "쌍곡함수":
        x = st.number_input("x", 0.0)
        func = st.selectbox("함수", ["sinh", "cosh", "tanh"])
        if st.button("계산"):
            val = {"sinh": math.sinh, "cosh": math.cosh,
                   "tanh": math.tanh}[func](x)
            st.success(f"{func}({x}) = {val}")

    elif mode == "팩토리얼":
        n = st.number_input("정수 n (0 이상, 170 이하 권장)", 0, step=1)
        if st.button("계산"):
            if n < 0 or float(n) != int(n):
                st.error("0 이상의 정수를 입력하세요.")
            else:
                st.success(f"{int(n)}! = {math.factorial(int(n))}")

    elif mode == "n 제곱근":
        a = st.number_input("숫자 a", 1.0)
        n = st.number_input("근 차수 n (양수)", 2.0)
        if st.button("계산"):
            try:
                st.success(f"{n}√{a} = {a ** (1/n)}")
            except Exception as e:
                st.error(e)

# ──────────────────────────────────────────
# 2) 통계 ----------------------------------------------------
def statistics_block():
    st.header("② 통계(평균·분산·표준편차)")
    nums_str = st.text_area("쉼표(,)로 구분해 숫자 입력", "1, 2, 3, 4, 5")
    try:
        nums = [float(x) for x in nums_str.split(",") if x.strip() != ""]
        if len(nums) == 0:
            st.warning("숫자를 입력하세요.")
            return
        st.write(f"데이터: {nums}")
        st.success(f"• 평균: {statistics.mean(nums)}")
        if len(nums) > 1:
            st.success(f"• 분산: {statistics.variance(nums)}")
            st.success(f"• 표준편차: {statistics.stdev(nums)}")
        else:
            st.info("분산·표준편차는 2개 이상 필요")
    except ValueError:
        st.error("숫자만 , 로 구분해 입력하세요.")

# ──────────────────────────────────────────
# 3) 단위 변환 ----------------------------------------------
def unit_conversion():
    st.header("③ 단위 변환")

    categories = {
        "길이": {
            "m": 1, "cm": 1e-2, "mm": 1e-3, "km": 1e3, "inch": 0.0254, "ft": 0.3048
        },
        "무게": {
            "kg": 1, "g": 1e-3, "lb": 0.453592
        },
        "온도": ["°C", "°F", "K"]
    }

    cat = st.selectbox("카테고리", list(categories.keys()))

    if cat != "온도":
        units = categories[cat]
        val = st.number_input("값", 0.0)
        u_from = st.selectbox("from", units.keys())
        u_to   = st.selectbox("to", units.keys())
        if st.button("변환"):
            base = val * units[u_from]          # 기준 단위(m or kg)
            res  = base / units[u_to]
            st.success(f"{val} {u_from} = {res} {u_to}")
    else:
        val = st.number_input("값", 0.0)
        u_from = st.selectbox("from", categories["온도"])
        u_to   = st.selectbox("to", categories["온도"])
        if st.button("변환"):
            # 섭씨로 변환
            c = {"°C": val,
                 "°F": (val - 32) * 5/9,
                 "K" : val - 273.15}[u_from]
            res = {"°C": c,
                   "°F": c * 9/5 + 32,
                   "K" : c + 273.15}[u_to]
            st.success(f"{val} {u_from} = {res} {u_to}")

# ──────────────────────────────────────────
# 4) 복소수 -----------------------------------------------
def complex_calc():
    st.header("④ 복소수 계산")
    a = st.text_input("복소수 A (예: 1+2j)", "1+2j")
    b = st.text_input("복소수 B (예: 3-4j)", "3-4j")
    op = st.selectbox("연산", ["+", "-", "×", "÷", "|A|", "conj(A)"])
    if st.button("계산"):
        try:
            A, B = complex(a), complex(b)
            if op == "+": res = A + B
            elif op == "-": res = A - B
            elif op == "×": res = A * B
            elif op == "÷": res = A / B
            elif op == "|A|": res = abs(A)
            elif op == "conj(A)": res = A.conjugate()
            st.success(f"결과: {res}")
        except Exception as e:
            st.error(f"입력 오류: {e}")

# ──────────────────────────────────────────
# 5) 그래프 그리기 -----------------------------------------
def graph_plot():
    st.header("⑤ 그래프 그리기 f(x)")
    expr = st.text_input("함수식 (변수: x)", "sin(x)")
    xmin, xmax = st.slider("x 범위", -10.0, 10.0, (-5.0, 5.0))
    if st.button("그리기"):
        x = sp.symbols('x')
        try:
            f = sp.sympify(expr)
            f_lamb = sp.lambdify(x, f, 'numpy')
            xs = np.linspace(xmin, xmax, 400)
            ys = f_lamb(xs)
            fig = go.Figure(go.Scatter(x=xs, y=ys, mode='lines'))
            fig.update_layout(height=400, margin=dict(l=20,r=20,t=30,b=20))
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"식 오류: {e}")

# ──────────────────────────────────────────
# 6) 다항식 미분·적분 --------------------------------------
def poly_calc():
    st.header("⑥ 다항식 미분 · 적분")
    coeffs = st.text_input("계수 리스트 (높은 차수→낮은 차수, 예: 1 0 -3 4)", "1 0 -3 4")
    action = st.radio("연산", ["미분", "적분(부정)"])
    if st.button("계산"):
        try:
            nums = [float(c) for c in coeffs.split()]
            x = sp.symbols('x')
            poly = sum(c * x**p for p, c in
                       zip(range(len(nums)-1, -1, -1), nums))
            res = sp.diff(poly) if action == "미분" else sp.integrate(poly)
            st.success(f"다항식: {sp.expand(poly)}")
            st.success(f"{action} 결과: {sp.expand(res)} + C" if action=="적분(부정)"
                       else f"{action} 결과: {sp.expand(res)}")
        except Exception as e:
            st.error(f"입력 오류: {e}")

# ──────────────────────────────────────────
# 7) 메모리 (M+, M-, MR, MC) -------------------------------
def memory_panel():
    st.header("⑦ 메모리")
    st.write(f"현재 메모리: **{st.session_state.memory}**")
    val = st.number_input("값", 0.0, key="mem_val")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("M+"):
        st.session_state.memory += val
    if col2.button("M-"):
        st.session_state.memory -= val
    if col3.button("MR"):
        st.success(f"Memory Recall: {st.session_state.memory}")
    if col4.button("MC"):
        st.session_state.memory = 0.0

# ──────────────────────────────────────────
# MAIN MENU ------------------------------------------------
menu = st.sidebar.radio(
    "기능 선택",
    ["① 일반/삼각/…", "② 통계", "③ 단위 변환",
     "④ 복소수", "⑤ 그래프", "⑥ 다항식", "⑦ 메모리"]
)

if menu == "① 일반/삼각/…":   basic_trig_hypo()
elif menu == "② 통계":        statistics_block()
elif menu == "③ 단위 변환":   unit_conversion()
elif menu == "④ 복소수":      complex_calc()
elif menu == "⑤ 그래프":      graph_plot()
elif menu == "⑥ 다항식":      poly_calc()
elif menu == "⑦ 메모리":      memory_panel()
