import streamlit as st
from deep_translator import GoogleTranslator
from PIL import Image
import pytesseract
import io

# ページ設定
st.set_page_config(
    page_title="Google翻訳ツール",
    page_icon="🌐",
    layout="wide"
)

# セッション状態の初期化
if 'source_lang_index' not in st.session_state:
    st.session_state.source_lang_index = 0
if 'target_lang_index' not in st.session_state:
    st.session_state.target_lang_index = 1
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'first_run' not in st.session_state:
    st.session_state.first_run = False

# タイトル
st.title("🌐 Google翻訳ツール")
st.markdown("テキスト・ファイル・カメラから翻訳できます")
st.markdown("---")

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

# 日本語の初期インデックスを探す
if not st.session_state.first_run:
    try:
        st.session_state.target_lang_index = lang_names.index("japanese")
    except ValueError:
        st.session_state.target_lang_index = 1
    st.session_state.first_run = True

# 言語入れ替え関数
def swap_languages():
    current_source = st.session_state.source_lang_index
    current_target = st.session_state.target_lang_index
    st.session_state.source_lang_index = current_target
    st.session_state.target_lang_index = current_source

# 翻訳実行関数
def perform_translation(text_to_translate):
    if not text_to_translate.strip():
        st.warning("翻訳するテキストを入力してください")
        return
    
    try:
        with st.spinner("翻訳中..."):
            source_code = supported_languages[lang_names[st.session_state.source_lang_index]]
            target_code = supported_languages[lang_names[st.session_state.target_lang_index]]
            
            translator = GoogleTranslator(source=source_code, target=target_code)
            result = translator.translate(text_to_translate)
            
            st.session_state.translated_text = result
            st.rerun()
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

# タブを使用して入力方法を選択
tab1, tab2, tab3 = st.tabs(["📝 テキスト入力", "📄 ファイルアップロード", "📷 カメラ撮影"])

# ========== タブ1: テキスト入力 ==========
with tab1:
    col_input, col_output = st.columns(2)
    
    with col_input:
        st.subheader("翻訳元テキスト")
        input_text = st.text_area(
            "入力",
            height=250,
            placeholder="翻訳したい文章を入力してください...",
            label_visibility="collapsed"
        )
    
    with col_output:
        st.subheader("翻訳結果")
        st.text_area(
            "結果",
            value=st.session_state.translated_text,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    c1, c2, c3, c4 = st.columns([2, 0.5, 2, 1.5])
    
    with c1:
        st.selectbox("元言語", lang_names, key="source_lang_index", label_visibility="collapsed")
    
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("⇄", on_click=swap_languages, help="言語を入れ替える", use_container_width=True)
    
    with c3:
        st.selectbox("翻訳先言語", lang_names, key="target_lang_index", label_visibility="collapsed")
    
    with c4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 翻訳実行", use_container_width=True, type="primary", key="btn_text"):
            perform_translation(input_text)

# ========== タブ2: ファイルアップロード ==========
with tab2:
    st.subheader("📄 テキストファイルをアップロード")
    uploaded_file = st.file_uploader("テキストファイルを選択 (.txt, .md など)", type=["txt", "md", "csv"])
    
    if uploaded_file is not None:
        try:
            file_content = uploaded_file.read().decode('utf-8')
            st.text_area("ファイルの内容", value=file_content, height=200, disabled=True)
            
            st.markdown("---")
            c1, c2, c3, c4 = st.columns([2, 0.5, 2, 1.5])
            
            with c1:
                st.selectbox("元言語", lang_names, key="source_lang_file", label_visibility="collapsed")
            
            with c2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.button("⇄", on_click=swap_languages, help="言語を入れ替える", use_container_width=True, key="swap_file")
            
            with c3:
                st.selectbox("翻訳先言語", lang_names, key="target_lang_file", label_visibility="collapsed")
            
            with c4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚀 翻訳実行", use_container_width=True, type="primary", key="btn_file"):
                    source_code = supported_languages[lang_names[st.session_state.source_lang_file]]
                    target_code = supported_languages[lang_names[st.session_state.target_lang_file]]
                    
                    try:
                        with st.spinner("翻訳中..."):
                            translator = GoogleTranslator(source=source_code, target=target_code)
                            translated = translator.translate(file_content)
                            
                            st.success("翻訳完了！")
                            st.text_area("翻訳結果", value=translated, height=250, disabled=True)
                            
                            # ダウンロードボタン
                            st.download_button(
                                label="💾 翻訳結果をダウンロード",
                                data=translated,
                                file_name="translated.txt",
                                mime="text/plain"
                            )
                    except Exception as e:
                        st.error(f"翻訳エラー: {e}")
        except Exception as e:
            st.error(f"ファイル読み込みエラー: {e}")

# ========== タブ3: カメラ撮影 ==========
with tab3:
    st.subheader("📷 カメラで撮影して翻訳")
    
    camera_input = st.camera_input("カメラで撮影してください")
    
    if camera_input is not None:
        image = Image.open(camera_input)
        st.image(image, caption="撮影した画像", use_column_width=True)
        
        try:
            with st.spinner("画像から文字を読み取り中..."):
                extracted_text = pytesseract.image_to_string(image, lang='jpn+eng')
            
            if extracted_text.strip():
                st.text_area("抽出されたテキスト", value=extracted_text, height=150, disabled=True)
                
                st.markdown("---")
                c1, c2, c3, c4 = st.columns([2, 0.5, 2, 1.5])
                
                with c1:
                    st.selectbox("元言語", lang_names, key="source_lang_camera", label_visibility="collapsed")
                
                with c2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.button("⇄", on_click=swap_languages, help="言語を入れ替える", use_container_width=True, key="swap_camera")
                
                with c3:
                    st.selectbox("翻訳先言語", lang_names, key="target_lang_camera", label_visibility="collapsed")
                
                with c4:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🚀 翻訳実行", use_container_width=True, type="primary", key="btn_camera"):
                        source_code = supported_languages[lang_names[st.session_state.source_lang_camera]]
                        target_code = supported_languages[lang_names[st.session_state.target_lang_camera]]
                        
                        try:
                            with st.spinner("翻訳中..."):
                                translator = GoogleTranslator(source=source_code, target=target_code)
                                translated = translator.translate(extracted_text)
                                
                                st.success("翻訳完了！")
                                st.text_area("翻訳結果", value=translated, height=200, disabled=True)
                        except Exception as e:
                            st.error(f"翻訳エラー: {e}")
            else:
                st.warning("画像から文字が検出されませんでした。別の画像を試してください。")
        except Exception as e:
            st.error(f"OCR処理エラー: {e}")

# フッター
st.markdown("---")
st.caption("Powered by deep-translator & Streamlit | OCR by Tesseract")

