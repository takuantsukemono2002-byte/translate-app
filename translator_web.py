import streamlit as st
from deep_translator import GoogleTranslator
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import io

# ページ設定
st.set_page_config(
    page_title="翻訳ツール Pro",
    page_icon="🌐",
    layout="centered"  # スマホで見やすくするためにcenteredに変更
)

# カスタムCSSでUIをスマホ向けに調整
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 3em;
        font-size: 1.1em !important;
        margin-top: 10px;
    }
    .stTextArea textarea {
        font-size: 1.1em !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    /* スマホでの余白調整 */
    @media (max-width: 640px) {
        .main .block-container {
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# セッション状態の初期化
if 'source_lang_name' not in st.session_state:
    st.session_state.source_lang_name = "自動検出 (auto)"
if 'target_lang_name' not in st.session_state:
    st.session_state.target_lang_name = "japanese"
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""

# タイトル
st.title("🌐 翻訳ツール Pro")

# 言語リストの取得
@st.cache_resource
def get_supported_languages():
    try:
        translator = GoogleTranslator()
        langs_dict = translator.get_supported_languages(as_dict=True)
        return {"自動検出 (auto)": "auto", **langs_dict}
    except Exception:
        return {"自動検出 (auto)": "auto", "english": "en", "japanese": "ja"}

supported_languages = get_supported_languages()
lang_names = list(supported_languages.keys())

# 言語入れ替え関数
def swap_languages():
    old_source = st.session_state.source_lang_name
    old_target = st.session_state.target_lang_name
    st.session_state.source_lang_name = old_target
    st.session_state.target_lang_name = old_source

# 翻訳実行ロジック
def run_translation(text):
    if not text.strip():
        st.warning("翻訳するテキストがありません")
        return ""
    try:
        source_code = supported_languages[st.session_state.source_lang_name]
        target_code = supported_languages[st.session_state.target_lang_name]
        translator = GoogleTranslator(source=source_code, target=target_code)
        return translator.translate(text)
    except Exception as e:
        st.error(f"翻訳エラー: {e}")
        return ""

# OCR用の画像処理関数（精度向上用）
def preprocess_image(image):
    # グレースケール化
    image = ImageOps.grayscale(image)
    # コントラスト強調
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    return image

# 言語選択UI（スマホ向けに横並びを調整）
def language_selector_ui(key_suffix):
    c1, c2, c3 = st.columns([4, 2, 4])
    with c1:
        st.selectbox("元", lang_names, key="source_lang_name", label_visibility="collapsed")
    with c2:
        st.button("⇄", on_click=swap_languages, key=f"swap_{key_suffix}")
    with c3:
        st.selectbox("先", lang_names, key="target_lang_name", label_visibility="collapsed")

# タブ構成
tab1, tab2, tab3 = st.tabs(["📝 テキスト", "📄 ファイル", "📷 カメラ・画像"])

# --- テキスト入力 ---
with tab1:
    input_text = st.text_area("翻訳したい文章", height=150, placeholder="ここに入力...", key="text_in", label_visibility="collapsed")
    language_selector_ui("text")
    if st.button("🚀 翻訳する", type="primary", key="exec_text"):
        with st.spinner("翻訳中..."):
            st.session_state.translated_text = run_translation(input_text)
    
    if st.session_state.translated_text:
        st.markdown("#### ✨ 翻訳結果")
        st.info(st.session_state.translated_text)

# --- ファイルアップロード ---
with tab2:
    uploaded_file = st.file_uploader("テキストファイルを選択", type=["txt", "md"])
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("内容プレビュー", value=content, height=100, disabled=True)
        language_selector_ui("file")
        if st.button("🚀 ファイルを翻訳", type="primary"):
            result = run_translation(content)
            if result:
                st.markdown("#### ✨ 翻訳結果")
                st.success(result)
                st.download_button("💾 結果を保存", result, "translated.txt")

# --- カメラ・画像翻訳 ---
with tab3:
    option = st.radio("入力方法を選択", ["カメラで撮影", "アルバムから選ぶ"], horizontal=True)
    
    img_file = None
    if option == "カメラで撮影":
        img_file = st.camera_input("カメラを起動")
    else:
        img_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="プレビュー", use_column_width=True)
        
        if st.button("🔍 文字を読み取って翻訳", type="primary"):
            with st.spinner("解析中..."):
                # 画像処理で精度向上
                processed_img = preprocess_image(img)
                # 日本語と英語を解析
                text_from_img = pytesseract.image_to_string(processed_img, lang='jpn+eng')
            
            if text_from_img.strip():
                st.write("---")
                st.markdown("**読み取った文字:**")
                st.text(text_from_img)
                
                result = run_translation(text_from_img)
                if result:
                    st.markdown("**✨ 翻訳結果:**")
                    st.success(result)
            else:
                st.error("文字を検出できませんでした。もっと明るい場所で撮影するか、文字に近づけてください。")

st.markdown("---")
st.caption("🌐 翻訳ツール Pro | Powered by deep-translator & Tesseract")
