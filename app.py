import streamlit as st
from PIL import Image
from io import BytesIO
from splitter import split_grid_from_image
from streamlit_cropper import st_cropper

if "pieces" not in st.session_state:
    st.session_state.pieces = None
st.set_page_config(
    page_title="Boddy splitter Pro",
    page_icon="🥵",   
    layout="wide"
)
st.title("🔥 Splitter Pro")
st.write("拖拉裁切 + IG 專用比例 + 拼接預覽")

uploaded = st.file_uploader("上傳圖片", type=["jpg", "png"])

# IG 模式
mode = st.radio(
    "選擇模式",
    ["自訂", "IG 2切", "IG 3切", "IG 九宮格"]
)

# IG 切圖設定
if mode == "IG 2切":
    rows, cols = 1, 2
elif mode == "IG 3切":
    rows, cols = 1, 3
elif mode == "IG 九宮格":
    rows, cols = 3, 3
else:
    rows = st.slider("列數", 1, 5, 1)
    cols = st.slider("欄數", 1, 5, 2)

# 🔥 IG 比例選擇（新功能）
aspect_option = st.selectbox(
    "IG 比例",
    ["原始比例", "1:1", "4:5", "5:4", "9:16", "16:9", "21:9"]
)

aspect_dict = {
    "原始比例": None,
    "1:1": (1, 1),
    "4:5": (4, 5),
    "5:4": (5,4),
    "9:16": (9, 16),
    "16:9": (16,9),
    "21:9": (21,9)

}

if uploaded:
    image = Image.open(uploaded)

    st.subheader("✂️ 拖拉裁切")

    # 拖拉裁切
    cropped = st_cropper(
        image,
        realtime_update=True,
        aspect_ratio=aspect_dict[aspect_option],
        box_color='#FF4B4B'
    )

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="原圖", use_column_width=True)

    with col2:
        st.image(cropped, caption="裁切後", use_column_width=True)

    if st.button("切圖 + 預覽"):
        with st.spinner("⚡ Fxxking making your IG layout..."):
            st.session_state.pieces = split_grid_from_image(cropped, rows, cols)

        st.success("完成！")

    if st.session_state.pieces is not None:
        pieces = st.session_state.pieces

        st.subheader("📸 拼接預覽")

        idx = 0
        for r in range(rows):
            cols_ui = st.columns(cols)
            for c in range(cols):
                with cols_ui[c]:
                    st.image(pieces[idx], use_column_width=True)
                idx += 1

        st.subheader("⬇下載")

        for i, img in enumerate(pieces):
            buf = BytesIO()
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(buf, format="JPEG", quality=95)
            
            st.download_button(
                label=f"下載 img_{i+1}.jpg",
                data=buf.getvalue(),
                file_name=f"img_{i+1}.jpg",
                mime="image/jpeg"
            )