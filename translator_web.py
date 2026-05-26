import streamlit as st
from deep_translator import GoogleTranslator
import time

# ページ設定
st.set_page_config(
    page_title="Google翻訳ツール",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# タイトルとヘッダー
st.title("🌐 Google翻訳ツール")
st.markdown("---")

# サイドバーで言語リストを読み込む
@st.cache_resource
def get_supported_languages():
    """サポートされている言語を取得する"""
    try:
        translator = GoogleTranslator()
        langs_dict = translator.get_supported_languages(as_dict=True)
        # 'auto' オプションを追加
        langs_dict = {"自動検出 (auto)": "auto", **langs_dict}
        return langs_dict
    except Exception as e:
        st.error(f"言語リストの取得に失敗しました: {e}")
        return {"自動検出 (auto)": "auto", "English": "en", "日本語": "ja"}

# 言語リストを取得
supported_languages = get_supported_languages()
lang_names = list(supported_languages.keys())
lang_codes = list(supported_languages.values())

# レイアウト: 2列構成
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 翻訳元テキスト")
    input_text = st.text_area(
        "翻訳したいテキストを入力してください",
        height=200,
        label_visibility="collapsed"
    )

with col2:
    st.subheader("✨ 翻訳結果")
    output_text = st.text_area(
        "翻訳結果がここに表示されます",
        height=200,
        disabled=True,
        label_visibility="collapsed",
        key="output_area"
    )

# 言語選択部分
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("**元言語**")
    source_lang_name = st.selectbox(
        "元言語を選択",
        lang_names,
        index=0,
        label_visibility="collapsed"
    )
    source_lang_code = supported_languages[source_lang_name]

with col2:
    st.markdown("**翻訳先言語**")
    target_lang_name = st.selectbox(
        "翻訳先言語を選択",
        lang_names,
        index=lang_codes.index("ja") if "ja" in lang_codes else 1,
        label_visibility="collapsed"
    )
    target_lang_code = supported_languages[target_lang_name]

with col3:
    st.markdown("**アクション**")
    translate_button = st.button("🚀 翻訳実行", use_container_width=True)

# 翻訳処理
if translate_button:
    if not input_text.strip():
        st.warning("翻訳するテキストを入力してください。")
    else:
        try:
            with st.spinner("翻訳中..."):
                translator = GoogleTranslator(source=source_lang_code, target=target_lang_code)
                result = translator.translate(input_text)
                
                # 結果を表示
                st.success("翻訳完了！")
                st.text_area(
                    "翻訳結果",
                    value=result,
                    height=200,
                    disabled=True,
                    label_visibility="collapsed"
                )
                
        except Exception as e:
            st.error(f"翻訳エラーが発生しました: {e}")

# フッター
st.markdown("---")
st.markdown("""
### 使い方
1. 左側のテキストエリアに翻訳したいテキストを入力します
2. 元言語と翻訳先言語を選択します
3. **翻訳実行** ボタンをクリックします
4. 右側に翻訳結果が表示されます

### 注意事項
- このツールは `deep-translator` ライブラリを利用しており、無料で利用できます
- 短時間に大量のリクエストを送信するとIP制限を受ける可能性があります
- 大量の翻訳が必要な場合は、Google Cloud Translation APIなどの公式サービスの利用を検討してください
""")
