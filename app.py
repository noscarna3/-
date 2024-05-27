import streamlit as st

# 사용자 정보를 저장할 딕셔너리 (학생 이름과 비밀번호)
user_info = {
    'student1': 'pass1',
    'student2': 'pass2',
    'student3': 'pass3',
    '이승민': '1234'
}

# 세션 상태 초기화
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'wrong_questions' not in st.session_state:
    st.session_state.wrong_questions = []
if 'page' not in st.session_state:
    st.session_state.page = 'auth'

# 페이지 선택
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["인증", "문제 풀기", "점수 확인"])

if page == "인증":
    st.session_state.page = 'auth'
elif page == "문제 풀기":
    st.session_state.page = 'quiz'
elif page == "점수 확인":
    st.session_state.page = 'score'

# 문제와 정답
questions = {
    "1. Streamlit은 어떤 언어로 작성되었나요?": "Python",
    "2. Streamlit에서 페이지를 나누는 데 사용되는 함수는?": "st.sidebar()",
    "3. Streamlit의 슬라이더 컴포넌트는?": "st.slider()",
    "4. Streamlit 앱을 실행하는 명령어는?": "streamlit run",
    "5. Streamlit의 캐싱 함수는?": "st.cache()"
}

if st.session_state.page == 'auth':
    st.title("사용자 인증")
    
    student_name = st.text_input("학생 이름을 입력하세요")
    password = st.text_input("비밀번호를 입력하세요", type='password')
    
    if st.button("로그인"):
        if student_name in user_info and password == user_info[student_name]:
            st.session_state.authenticated = True
            st.session_state.student_name = student_name
            st.success(f"{student_name}님, 인증에 성공했습니다!")
        else:
            st.session_state.authenticated = False
            st.error("학생 이름 또는 비밀번호가 잘못되었습니다.")
            
elif st.session_state.page == 'quiz':
    if st.session_state.authenticated:
        st.title("객관식 문제")
        
        responses = []
        for question, answer in questions.items():
            response = st.radio(question, 
                                ["Python", "Java", "C++", "JavaScript"] if question == "1. Streamlit은 어떤 언어로 작성되었나요?" 
                                else ["st.page()", "st.sidebar()", "st.selectbox()", "st.write()"] if question == "2. Streamlit에서 페이지를 나누는 데 사용되는 함수는?" 
                                else ["st.slider()", "st.range()", "st.scrollbar()", "st.progress()"] if question == "3. Streamlit의 슬라이더 컴포넌트는?" 
                                else ["streamlit start", "streamlit run", "streamlit execute", "streamlit launch"] if question == "4. Streamlit 앱을 실행하는 명령어는?" 
                                else ["st.cache()", "st.memo()", "st.save()", "st.remember()"])
            responses.append((question, response))
        
        if st.button("제출"):
            score = 0
            wrong_questions = []
            for question, response in responses:
                if response == questions[question]:
                    score += 1
                else:
                    wrong_questions.append(question)
            st.session_state.score = score
            st.session_state.wrong_questions = wrong_questions
            st.success("문제를 제출했습니다.")
    else:
        st.warning("먼저 인증을 완료해주세요.")
        
elif st.session_state.page == 'score':
    if st.session_state.authenticated:
        st.title("점수 확인")
        if st.session_state.score > 0:
            st.write(f"{st.session_state.student_name}님의 점수는 {st.session_state.score}점 입니다.")
            if st.session_state.wrong_questions:
                st.write("틀린 문제는 다음과 같습니다:")
                for question in st.session_state.wrong_questions:
                    st.write(f"- {question}")
        else:
            st.warning("먼저 문제를 풀어주세요.")
    else:
        st.warning("먼저 인증을 완료해주세요.")
