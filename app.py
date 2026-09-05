import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 環境変数の読み込み
load_dotenv()

# テーマの選択肢を用意
theme_1 = "プロトレーナー"
theme_2 = "ITキャリアカウンセラー"

def get_llm_response(messages_history, selected_theme):
    """
    LLMからの回答を取得する処理
    """
    # モデルのオブジェクトを用意
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

    # 選択テーマに応じて使用するプロンプトのシステムメッセージを分岐
    if selected_theme == theme_1:
        system_message = """
            あなたは経験豊富な親切なプロのパーソナルトレーナーです。フィットネス、筋力トレーニング、有酸素運動、ストレッチ、食事管理、ダイエット、スポーツ科学に関する豊富な知識を持っています。

            あなたの役割は、初心者から上級者まで幅広いユーザーに適した運動方法や食事法を提案し、正しいフォームや注意点を指導することです。無理な運動を推奨せず、個々の健康状態や目標に応じたアドバイスを行い、ユーザーを励ましながら分かりやすく具体的に指導してください。

            回答には、できるだけ具体的な説明を加え、必要に応じてステップバイステップのガイドを提供してください。医学的な診断は行わず、健康に不安がある場合は医師への相談を促してください。
        """
    else:
        system_message = """
            あなたはIT業界に精通した論理的で温かいキャリアカウンセラーです。IT業界でのキャリア形成、プログラミング学習、転職活動、スキルアップ、エンジニアのキャリアパスに関する深い知識を持っています。

            あなたの役割は、ユーザーがIT分野で成長・キャリアアップするための具体的なアドバイスを提供し、プログラミング学習方法や転職活動のポイントをわかりやすく説明することです。実用的なアクションプランを提示し、個々の悩みや状況に寄り添ったサポートを行ってください。

            法的・決定的なキャリア保証は行わず、個人の選択を尊重しながら主体的なキャリア形成を支援してください。
        """
    
    # システムメッセージを先頭に追加してプロンプトを作成
    input_messages = [SystemMessage(content=system_message)] + messages_history

    # LLMからの回答取得
    response = llm.invoke(input_messages)

    return response.content


# 案内文の表示
st.title("専門家AI相談チャット")
st.write("プロトレーナーとITキャリアカウンセラーに相談できるAIチャットアプリです。相談したいテーマを選択し、質問を入力してください。")

# --- セッション状態の初期化 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = None


# --- 1. テーマの未選択時（初期画面） ---
if st.session_state.selected_theme is None:
    selected_theme = st.radio(
        "【ご相談したい専門家を選択してください】",
        [theme_1, theme_2]
    )
    
    if st.button("この専門家に相談を開始する", type="primary"):
        st.session_state.selected_theme = selected_theme
        st.rerun()

# --- 2. テーマ選択後（チャット画面） ---
else:
    current_theme = st.session_state.selected_theme
    
    # 決定されたテーマを表示（選択の変更不可）
    st.success(f"現在の相談相手: **{current_theme}**")
    st.caption("※専門家を変更したい場合は、ページを再読み込み（リセット）してください。")
    st.divider()

    # 過去の会話履歴の表示
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)

    # 相談内容を入力するチャット欄
    if prompt := st.chat_input(f"{current_theme}に質問を入力..."):
        # ユーザーの質問を表示＆履歴に追加
        st.chat_message("user").write(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))

        # LLMからの回答取得
        with st.chat_message("assistant"):
            with st.spinner("専門家AIが回答を作成中..."):
                response_text = get_llm_response(st.session_state.messages, current_theme)
                st.write(response_text)

        # AIの回答を履歴に追加
        st.session_state.messages.append(AIMessage(content=response_text))