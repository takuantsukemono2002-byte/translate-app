import streamlit as st
from deep_translator import GoogleTranslator
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import io

# ページ設定
st.set_page_config(
    page_title="翻訳ツール Pro",
    page_icon="🌐",
    layout="centered"
)

# カスタムCSS: スマホ向け最適化
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 3.2em;
        font-size: 1.1em !important;
        border-radius: 10px;
    }
    .stTextArea textarea {
        font-size: 1.1em !important;
        border-radius: 10px;
    }
    .stAlert {
        border-radius: 10px;
    }
    /* タブの文字を大きく */
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1em;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# セッション状態
if 'source_lang' not in st.session_state:
    st.session_state.source_lang = "自動検出 (auto)"
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = "japanese"
if 'result' not in st.session_state:
    st.session_state.result = ""

# 言語リスト
@st.cache_resource
def get_langs():
    try:
        translator = GoogleTranslator()
        d = translator.get_supported_languages(as_dict=True)
        return {"自動検出 (auto)": "auto", **d}
    except:
        return {"自動検出 (auto)": "auto", "english": "en", "japanese": "ja"}

langs = get_langs()
lang_names = list(langs.keys())

def swap():
    st.session_state.source_lang, st.session_state.target_lang = st.session_state.target_lang, st.session_state.source_lang

def translate(text):
    if not text.strip(): return ""
    try:
        src = langs[st.session_state.source_lang]
        tgt = langs[st.session_state.target_lang]
        return GoogleTranslator(source=src, target=tgt).translate(text)
    except Exception as e:
        st.error(f"翻訳エラー: {e}")
        return ""

def ocr(img):
    try:
        # OCR精度向上のための前処理
        img = ImageOps.grayscale(img)
        img = ImageEnhance.Contrast(img).enhance(2.0)
        return pytesseract.image_to_string(img, lang='jpn+eng')
    except Exception as e:
        st.error(f"解析エラー: {e}")
        return ""

st.title("🌐 翻訳ツール Pro")

tab1, tab2 = st.tabs(["📝 テキスト入力", "📷 画像・ファイル"])

# --- タブ1: テキスト ---
with tab1:
    txt = st.text_area("翻訳したい文章", height=180, placeholder="ここに文字を入力...", label_visibility="collapsed")
    
    c1, c2, c3 = st.columns([4, 2, 4])
    with c1: st.selectbox("元", lang_names, key="source_lang", label_visibility="collapsed")
    with c2: st.button("⇄", on_click=swap, key="sw1")
    with c3: st.selectbox("先", lang_names, key="target_lang", label_visibility="collapsed")
    
    if st.button("🚀 翻訳する", type="primary", key="ex1"):
        with st.spinner("翻訳中..."):
            st.session_state.result = translate(txt)
    
    if st.session_state.result:
        st.markdown("---")
        st.markdown("**✨ 翻訳結果**")
        st.success(st.session_state.result)

# --- タブ2: 画像・ファイル ---
with tab2:
    f = st.file_uploader("画像またはテキストファイルを選択", type=["jpg", "jpeg", "png", "txt", "md"])
    
    if f:
        if f.type.startswith("image"):
            img = Image.open(f)
            st.image(img, use_column_width=True)
            if st.button("🔍 画像を解析して翻訳", type="primary"):
                with st.spinner("解析中..."):
                    text = ocr(img)
                    if text.strip():
                        res = translate(text)
                        st.markdown("**読み取り内容:**")
                        st.text(text)
                        st.markdown("**✨ 翻訳結果:**")
                        st.success(res)
                    else:
                        st.warning("文字が見つかりませんでした。")
        else:
            text = f.read().decode("utf-8")
            st.text_area("ファイル内容", value=text, height=150, disabled=True)
            if st.button("🚀 ファイルを翻訳", type="primary"):
                with st.spinner("翻訳中..."):
                    res = translate(text)
                    st.success(res)
                    st.download_button("💾 結果を保存", res, "translated.txt")

st.markdown("---")
st.caption("スマホでは「ファイルを選択」から直接カメラを起動できます")
