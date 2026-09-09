import streamlit as st
from datetime import datetime, time

# ----------------- 1. 頁面設定 -----------------
st.set_page_config(
    page_title="酷澎自動化帶貨工作台",
    page_icon="🛍️",
    layout="wide"
)

# ----------------- 2. 私密登入驗證 (從 Secrets 讀取) -----------------
# 優先讀取 Streamlit 後台 Secrets，若未設定則暫用預設帳密 (admin / admin888)
CORRECT_USER = st.secrets.get("ADMIN_USER", "admin")
CORRECT_PWD = st.secrets.get("ADMIN_PWD", "admin888")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.authenticated:
    st.markdown("### 🔒 酷澎自動化帶貨系統")
    st.caption("內部私有工具，不開放對外註冊。")

    with st.form("login_form"):
        input_user = st.text_input("帳號", placeholder="請輸入帳號")
        input_pwd = st.text_input("密碼", type="password", placeholder="請輸入密碼")
        submitted = st.form_submit_button("登入系統", type="primary")

        if submitted:
            if input_user == CORRECT_USER and input_pwd == CORRECT_PWD:
                st.session_state.authenticated = True
                st.session_state.username = input_user
                st.success("登入成功！")
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請重新輸入。")
    st.stop()  # 未通過登入驗證，中斷後續介面載入

# ----------------- 3. 初始化工作台狀態 -----------------
if "today_products" not in st.session_state:
    st.session_state.today_products = [
        {
            "id": "CP101",
            "name": "象印 不鏽鋼真空保溫杯 480ml",
            "orig_price": 1200,
            "disc_price": 699,
            "post_time": time(10, 0),
            "post_threads": True,
            "copy": "今天辦公室必備神物降價！保冷超有感，冰塊放整天都不融化～特價 $699 真的超划算 🔥",
            "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&q=80"
        },
        {
            "id": "CP102",
            "name": "日本原裝 洗衣精補充包 6件組",
            "orig_price": 890,
            "disc_price": 499,
            "post_time": time(12, 30),
            "post_threads": True,
            "copy": "囤貨魔人快看！平均一包不到85元，香氣自然不刺鼻，今天買最便宜 🫧",
            "image": "https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=300&q=80"
        },
        {
            "id": "CP103",
            "name": "多功能人體工學記憶棉護腰靠墊",
            "orig_price": 750,
            "disc_price": 380,
            "post_time": time(15, 0),
            "post_threads": True,
            "copy": "久坐族救星！支撐度剛剛好，腰不再痠，辦公室必備好物分享～",
            "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=300&q=80"
        },
        {
            "id": "CP104",
            "name": "氣炸鍋專用烘焙紙 100入",
            "orig_price": 300,
            "disc_price": 149,
            "post_time": time(18, 0),
            "post_threads": False,
            "copy": "氣炸鍋懶人必備，用完直接丟不用洗鍋子！百元出頭太划算～",
            "image": "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=300&q=80"
        },
        {
            "id": "CP105",
            "name": "無線降噪藍牙耳機 旗艦版",
            "orig_price": 2490,
            "disc_price": 1290,
            "post_time": time(21, 0),
            "post_threads": True,
            "copy": "千元出頭的降噪耳機天花板！通話清晰、續航力超強，睡前推薦給大家 🎧",
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&q=80"
        }
    ]

if "history" not in st.session_state:
    st.session_state.history = [
        {
            "name": "摩卡濃縮咖啡豆 1kg 深焙",
            "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=200&q=80",
            "date": "2026-09-09 08:30"
        },
        {
            "name": "超輕量摺疊晴雨兩用傘 (抗UV)",
            "image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=200&q=80",
            "date": "2026-09-08 18:45"
        }
    ]

# ----------------- 4. 側邊欄與選單 -----------------
st.sidebar.title("🛍️ 酷澎自動帶貨")
st.sidebar.caption(f"登入帳號：{st.session_state.username}")

menu = st.sidebar.radio(
    "功能選單",
    ["今日帶貨", "今日排程", "自己找商品", "我的內容"]
)

if st.sidebar.button("登出系統", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.rerun()

# ----------------- 5. 四大選單頁面 -----------------

# ======== 選單 1：今日帶貨 ========
if menu == "今日帶貨":
    st.header("✨ 今日帶貨（每日精選 5 檔）")
    st.caption("挑選 5 個商品，可微調文案、勾選發布至 Threads，並自訂各篇貼文發布時間。")

    col_btn, _ = st.columns([2, 5])
    with col_btn:
        if st.button("🚀 確認送出今日 5 篇排程", type="primary", use_container_width=True):
            st.success("已成功排程！系統將於排定時間自動推播至 Threads。")

    st.write("---")

    for i, prod in enumerate(st.session_state.today_products):
        with st.container():
            c1, c2, c3 = st.columns([1.5, 3.5, 2])
            with c1:
                st.image(prod["image"], use_container_width=True)
            with c2:
                st.subheader(f"#{i+1} {prod['name']}")
                st.markdown(f"**特價：:red[NT${prod['disc_price']}]** ~~原價：NT${prod['orig_price']}~~")
                prod["copy"] = st.text_area(f"Threads 文案預覽與修改 (#{i+1})", value=prod["copy"], height=80)
            with c3:
                st.write("**排程設定**")
                prod["post_threads"] = st.checkbox(
                    "勾選加入 Threads 今日發文", 
                    value=prod["post_threads"], 
                    key=f"check_{prod['id']}"
                )
                prod["post_time"] = st.time_input(
                    "調整發布時間", 
                    value=prod["post_time"], 
                    key=f"time_{prod['id']}"
                )
            st.write("---")

# ======== 選單 2：今日排程 ========
elif menu == "今日排程":
    st.header("📊 今日排程狀態看板")
    st.caption("即時追蹤貼文發布佇列與狀態統計。")

    total_checked = sum(1 for p in st.session_state.today_products if p["post_threads"])
    pending = 5 - total_checked
    scheduled = total_checked
    published = len(st.session_state.history)
    failed = 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("⏳ 待確認", f"{pending} 篇")
    m2.metric("📅 已排程", f"{scheduled} 篇")
    m3.metric("✅ 已發布", f"{published} 篇")
    m4.metric("❌ 失敗", f"{failed} 篇")

    st.write("### 今日排程清單明細")
    for prod in st.session_state.today_products:
        status_text = "🟢 已排程" if prod["post_threads"] else "🟡 待確認 (尚未勾選發文)"
        st.write(f"- **[{prod['post_time'].strftime('%H:%M')}]** {prod['name']} ➜ {status_text}")

# ======== 選單 3：自己找商品 ========
elif menu == "自己找商品":
    st.header("🔍 搜尋酷澎商品")
    st.caption("搜尋酷澎商品，自動串聯 API 獲取特價資訊、AI 生成文案，一鍵勾選加入發文。")

    search_query = st.text_input("輸入關鍵字或貼上酷澎商品連結", placeholder="例如：行動電源、乳清蛋白...")
    
    if st.button("搜尋酷澎商品", type="primary"):
        st.info(f"已串接酷澎 API 查詢關鍵字：『{search_query}』")

    st.write("### 推薦商品與即時價格")
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&q=80", width=180)
        st.write("**三得利 芝麻明EX 90錠**")
        st.markdown("**目前價格：:red[NT$1,450]**")
        st.write("💡 **產出文案：** 經常失眠、精神不濟？這款回購率超高，睡得好精神自然好！")
        if st.button("➕ 勾選加入今日發文", key="search_add_1"):
            st.success("已加入今日發文清單！")

    with col2:
        st.image("https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?w=300&q=80", width=180)
        st.write("**便攜式手持掛燙機**")
        st.markdown("**目前價格：:red[NT$599]**")
        st.write("💡 **產出文案：** 租屋族救星！30秒快速出蒸氣，皺巴巴襯衫瞬間燙平 ✨")
        if st.button("➕ 勾選加入今日發文", key="search_add_2"):
            st.success("已加入今日發文清單！")

# ======== 選單 4：我的內容 ========
elif menu == "我的內容":
    st.header("📁 我的內容（已發布貼文紀錄）")
    st.caption("記錄過去已成功發布的產品圖片、名稱與發布時間。")

    for item in st.session_state.history:
        c_img, c_info = st.columns([1, 4])
        with c_img:
            st.image(item["image"], width=130)
        with c_info:
            st.subheader(item["name"])
            st.markdown(f"🕒 **發布時間：** `{item['date']}` (包含年月日、幾點幾分)")
            st.markdown("[🔗 前往 Threads 檢視貼文](https://threads.net)")
        st.write("---")
