import streamlit as st
import math

st.set_page_config(page_title="다기능 계산기", page_icon="🧮", layout="centered")

def main():
    st.title("🧮 다기능 계산기")

    operations = {
        "덧셈 (+)"   : "+",
        "뺄셈 (-)"   : "-",
        "곱셈 (×)"   : "*",
        "나눗셈 (÷)" : "/",
        "모듈러 (%)" : "%",
        "지수 (^)"   : "^",
        "로그 (log)" : "log"
    }

    op_label = st.selectbox("연산을 선택하세요", list(operations.keys()))
    op = operations[op_label]

    # 로그는 입력 형식이 다릅니다
    if op == "log":
        x = st.number_input("로그를 취할 값 (양수)", value=1.0, step=1.0)
        base = st.number_input("밑 (양수, 1이 아님)", value=10.0, step=1.0)

        if st.button("계산"):
            try:
                result = math.log(x, base)
                st.success(f"log_{base:g}({x:g}) = {result}")
            except ValueError:
                st.error("x와 밑(base)은 둘 다 양수이고, 밑은 1이 아니어야 합니다.")
    else:
        a = st.number_input("숫자 A", value=0.0, step=1.0)
        b = st.number_input("숫자 B", value=0.0, step=1.0)

        if st.button("계산"):
            try:
                if op == "+":   result = a + b
                if op == "-":   result = a - b
                if op == "*":   result = a * b
                if op == "/":   result = a / b          # 0으로 나누면 예외 발생
                if op == "%":   result = a % b
                if op == "^":   result = a ** b

                st.success(f"결과: {result}")
            except ZeroDivisionError:
                st.error("0으로 나눌 수 없습니다.")
            except Exception as e:
                st.error(f"오류: {e}")

if __name__ == "__main__":
    main()
