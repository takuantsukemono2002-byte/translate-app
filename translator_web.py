import streamlit as st
from deep_translator import GoogleTranslator

# ページ設定
st.set_page_config(
    page_title="Google翻訳ツール",
    page_icon="🌐",
    layout="wide"
)

# セッション状態の初期化（言語入れ替えと結果保持のため）
if 'source_lang_index' not in st.session_state:
    st.session_state.source_lang_index = 0  # デフォルト: 自動検出
if 'target_lang_index' not in st.session_state:
    st.session_state.target_lang_index = 1  # デフォルト: 日本語（後で調整）
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""

# タイトル
st.title("🌐 Google翻訳ツール")
st.markdown("---")

# 言語リストの取得
@st.cache_resource
def get_supported_languages():
    try:
        translator = GoogleTranslator()
        langs_dict = translator.get_supported_languages(as_dict=True)
        # 'auto' を先頭に追加
        return {"自動検出 (auto)": "auto", **langs_dict}
    except Exception:
        return {"自動検出 (auto)": "auto", "english": "en", "japanese": "ja"}

supported_languages = get_supported_languages()
lang_names = list(supported_languages.keys())

# 日本語の初期インデックスを探す
if 'first_run' not in st.session_state:
    try:
        st.session_state.target_lang_index = lang_names.index("japanese")
    except ValueError:
        st.session_state.target_lang_index = 1
    st.session_state.first_run = False

# 言語入れ替え関数
def swap_languages():
    # 自動検出(index 0)の場合は入れ替えを制限するか、固定言語にする
    current_source = st.session_state.source_lang_index
    current_target = st.session_state.target_lang_index
    
    # 入れ替え実行
    st.session_state.source_lang_index = current_target
    st.session_state.target_lang_index = current_source

# レイアウト: 2列
col_input, col_output = st.columns(2)

with col_input:
    st.subheader("📝 翻訳元テキスト")
    input_text = st.text_area(
        "入力",
        height=250,
        placeholder="翻訳したい文章を入力してください...",
        label_visibility="collapsed"
    )

with col_output:
    st.subheader("✨ 翻訳結果")
    st.text_area(
        "結果",
        value=st.session_state.translated_text,
        height=250,
        disabled=True,
        label_visibility="collapsed"
    )

# 言語選択とアクション
st.markdown("---")
c1, c2, c3, c4 = st.columns([2, 0.5, 2, 1.5])

with c1:
    source_lang_name = st.selectbox(
        "元言語",
        lang_names,
        key="source_lang_index"
    )

with c2:
    st.markdown("<br>", unsafe_allow_html=True) # 位置調整
    st.button("⇄", on_click=swap_languages, help="言語を入れ替える", use_container_width=True)

with c3:
    target_lang_name = st.selectbox(
        "翻訳先言語",
        lang_names,
        key="target_lang_index"
    )

with c4:
    st.markdown("<br>", unsafe_allow_html=True) # 位置調整
    translate_button = st.button("🚀 翻訳実行", use_container_width=True, type="primary")

# 翻訳ロジック
if translate_button:
    if not input_text.strip():
        st.warning("テキストを入力してください")
    else:
        try:
            with st.spinner("翻訳中..."):
                source_code = supported_languages[source_lang_name]
                target_code = supported_languages[target_lang_name]
                
                translator = GoogleTranslator(source=source_code, target=target_code)
                result = translator.translate(input_text)
                
                # セッション状態を更新して再描画
                st.session_state.translated_text = result
                st.rerun()
                
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# フッター
st.markdown("---")
st.caption("Powered by deep-translator & Streamlit")
