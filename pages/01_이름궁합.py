import streamlit as st
import re

# 고정 이름 설정
FIXED_NAME = "이동혁"

st.set_page_config(page_title="이동혁 이름궁합 (획수 피라미드)", page_icon="❤️")

st.title("❤️ 이름 궁합 테스트 (획수 피라미드)")
st.write(f"한쪽 이름은 **{FIXED_NAME}**로 고정되어 있습니다.")
st.write("상대방 이름을 입력한 후 '궁합 계산하기' 버튼을 눌러 결과를 확인하세요.")

# 한글 초/중/종성 목록과 획수 데이터 (인덱스 매칭)
CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
CHO_STROKES  = [2,4,2,3,6,5,4,4,8,2,4,1,3,6,4,3,4,5,3]

JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JUN_STROKES    = [2,3,3,4,2,3,3,4,2,3,4,3,3,2,3,4,3,3,1,2,1]

JONGSUNG_LIST = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
# 종성 획수 계산: 초성+중성 분해하거나 초성 획수만
JONG_STROKES = {}
for jong in JONGSUNG_LIST:
    if jong == '':
        JONG_STROKES[jong] = 0
    elif jong in CHOSUNG_LIST:
        JONG_STROKES[jong] = CHO_STROKES[CHOSUNG_LIST.index(jong)]
    else:
        # 합성 종성 (두 글자)
        first, second = jong[0], jong[1]
        # 자모 음가별 획수: 초성이면 CHO, 중성이면 JUN
        stroke_count = 0
        if first in CHOSUNG_LIST:
            stroke_count += CHO_STROKES[CHOSUNG_LIST.index(first)]
        if second in JUNGSUNG_LIST:
            stroke_count += JUN_STROKES[JUNGSUNG_LIST.index(second)]
        JONG_STROKES[jong] = stroke_count

# 한 글자 획수 합산 함수
def count_strokes(hangul_char: str) -> int:
    if not re.match(r"[가-힣]", hangul_char):
        return 0
    code = ord(hangul_char) - ord('가')
    cho_idx  = code // (21 * 28)
    jung_idx = (code % (21 * 28)) // 28
    jong_idx = code % 28

    return CHO_STROKES[cho_idx] + JUN_STROKES[jung_idx] + JONG_STROKES[JONGSUNG_LIST[jong_idx]]

# 두 이름 섞기 (한 글자씩 번갈아)
def interleave(name1: str, name2: str) -> list:
    merged = []
    max_len = max(len(name1), len(name2))
    for i in range(max_len):
        if i < len(name1): merged.append(name1[i])
        if i < len(name2): merged.append(name2[i])
    return merged

# 피라미드 합산
def pyramid_sum(nums: list) -> list:
    levels = [nums]
    while len(levels[-1]) > 2:
        curr = levels[-1]
        next_level = []
        for i in range(len(curr) - 1):
            s = curr[i] + curr[i+1]
            if s >= 10:
                next_level.extend([s // 10, s % 10])
            else:
                next_level.append(s)
        levels.append(next_level)
    return levels

# 입력 UI
other_name = st.text_input("상대방 이름 입력:")
if st.button("궁합 계산하기"):
    if not other_name:
        st.warning("상대방 이름을 입력해주세요.")
    else:
        # 섞기 & 획수 계산
        sequence = interleave(FIXED_NAME, other_name)
        strokes = [count_strokes(ch) for ch in sequence]
        levels = pyramid_sum(strokes)
        final = levels[-1]
        score = final[0] * 10 + final[1]

        st.subheader(f"🔮 {FIXED_NAME} ❤️ {other_name} 궁합 점수: {score}점")
        st.write("---")
        st.write("#### 📊 피라미드 레벨별 값:")
        for lvl in levels:
            st.write(lvl)

        # 결과 알림
        if score >= 80:
            st.success("✨ 찰떡궁합! 두 분은 운명적이에요! ✨")
            st.balloons()
        elif score >= 50:
            st.info("😊 괜찮은 궁합이에요. 서로 노력해보세요!")
        else:
            st.error("😅 더 알아가고 이해가 필요할 수도 있어요.")

st.markdown("---")
st.caption("*주의: 오락용 결과입니다. 과학적 근거는 없습니다.*")


