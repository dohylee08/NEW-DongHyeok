import streamlit as st
import re

st.set_page_config(page_title="이름 궁합 테스트", page_icon="💖")

st.title("💖 이름 자음/모음 궁합 테스트")
st.write("두 사람의 이름으로 자음과 모음 수를 비교하여 궁합 점수를 알려드립니다!")

# 한글 자음/모음 추출용 정규식
CHOSUNG_LIST = [chr(c) for c in range(ord('가'), ord('힣')+1)]

def extract_jamos(name):
    CHOSUNG = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
    JUNGSUNG = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
    JONGSUNG = [""] + list("ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")

    chosung_list = []
    jungsung_list = []
    jongsung_list = []

    for ch in name:
        if re.match('[가-힣]', ch):
            code = ord(ch) - ord('가')
            chosung = code // (21 * 28)
            jungsung = (code % (21 * 28)) // 28
            jongsung = code % 28

            chosung_list.append(CHOSUNG[chosung])
            jungsung_list.append(JUNGSUNG[jungsung])
            jongsung_list.append(JONGSUNG[jongsung])
        else:
            continue

    return chosung_list, jungsung_list, jongsung_list

def calculate_score(name1, name2):
    c1, j1, _ = extract_jamos(name1)
    c2, j2, _ = extract_jamos(name2)

    # 자음, 모음 개수 비교 후 비율로 점수 환산
    consonant_match = len(set(c1) & set(c2))
    vowel_match = len(set(j1) & set(j2))

    score = (consonant_match * 20 + vowel_match * 15 + 50)
    if score > 100:
        score = 100
    return score, consonant_match, vowel_match

name1 = st.text_input("첫 번째 이름 입력")
name2 = st.text_input("두 번째 이름 입력")

if st.button("궁합 보기"):
    if name1 and name2:
        score, consonant_match, vowel_match = calculate_score(name1, name2)

        st.subheader(f"❤️ {name1} ❤️ {name2} ❤️ 궁합 점수는...")
        st.success(f"👉 **{score}점** 입니다!")
        st.write(f"공통 자음 수: **{consonant_match}개**, 공통 모음 수: **{vowel_match}개**")
        
        if score >= 80:
            st.balloons()
            st.write("✨ 아주 좋은 궁합이에요! 잘 어울리는 두 분! ✨")
        elif score >= 60:
            st.write("😊 나쁘지 않은 궁합이에요. 서로 노력하면 멋진 관계가 될 수 있어요!")
        else:
            st.write("😅 조금 다른 스타일일 수도 있겠네요. 하지만 이름으로 인연이 정해지는 건 아니니까요!")
    else:
        st.warning("두 이름 모두 입력해주세요!")

st.markdown("---")
st.caption("본 궁합 테스트는 재미로 보는 것이며 과학적 근거는 없습니다 😉")
