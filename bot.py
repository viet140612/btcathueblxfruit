import discord
from discord.ext import commands
import json, os, uuid, asyncio
import sys
import io
import datetime
from discord import app_commands
import asyncio
from flask import Flask
import threading
import hashlib
import aiohttp
from flask import Flask, request, jsonify
import string
import random
import requests
import random
import uuid
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # THIẾU DÒNG NÀY ĐÂY ÔNG NHÉ!
import threading
import uvicorn
from dotenv import load_dotenv
# Sửa lỗi hiển thị icon và tiếng Việt trên Terminal Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os

load_dotenv() 


TOKEN = os.getenv("DISCORD_TOKEN")

OWNER_ID = 1222153820679966761 

TSR_PARTNER_ID = "46843352354"
TSR_PARTNER_KEY = "3f9e74b0fa70705f17c58fa47875c190"
API_URL = "https://thesieure.com/chargingws/v2"
BASE_URL_BLOG = "https://keybotcaythue.blogspot.com/2026/02/key-cho-bot.html"
LINKS_CONFIG_FILE = "links_config.json"
KEYS_STORAGE_FILE = "active_keys.json" # File bot tự tạo để quản lý key tạm thời
DATA_FILE = "data.json"
PRICE_FILE = "banggia.json"
ADMIN_FILE = "admins.json"

print("TOKEN =", TOKEN)

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ================= DỮ LIỆU BẢNG GIÁ MỚI =================
DEFAULT_PRICES = {
    "Kiếm & Súng": {
        "Kiếm Yama": 20000,
        "Kiếm Tushita": 20000,
        "CDK (Đủ 2 thanh + Mas)": 10000,
        "Shark Anchor": 40000,
        "Skull Guitar (Đủ NL)": 20000,
        "TTK (10k/thanh, Mas 20k)": 50000
    },
    "Fighting Style": {
        "Electric Claw": 10000,
        "Dragon Talon": 20000,
        "Karate": 10000,
        "God Human (Đủ võ + Mas)": 20000,
        "Suguine Art (Tim + NL)": 70000
    },
    "Nguyên Liệu": {
        "Cày Mas (1-350)": 20000,
        "10k Beli": 20000,
        "10k Fragment": 10000
    },
    "Sea Event": {
        "Săn Leviathan": 50000,
        "Săn đảo núi lửa (1 đảo)": 20000,
        "Lấy full đai": 70000
    },
    "Race (Tộc)": {
        "1 Gear": 10000,
        "Full Gear": 50000,
        "Gạt cần": 20000,
        "Tộc Cyborg (Key + Raid Law)": 40000,
        "Tộc Goul": 20000
    }
}




# ================= XỬ LÝ DỮ LIỆU =================
import threading
import uvicorn
import json
import requests
from discord.ext import commands
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# --- 1. CẤU HÌNH DỮ LIỆU ---
ADMIN_FILE = "admins.json"
LINK_CONFIGS = {
    "link_1": {"name": "Link 1s", "max": 3},
    "link_2": {"name": "Link 2s", "max": 5}
}
storage_web_status = {} # Lưu IP và trạng thái từ Web

# --- 2. KHỞI TẠO FASTAPI ---
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cấu hình CORS cho Render (cho phép Blogspot gọi API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Có thể đổi thành domain blog của bạn để bảo mật hơn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI, Request

# ===== TEST HOME =====

app = FastAPI()

@app.get("/")
async def home():
    return {"ok": True}

@app.get("/verify-link")
async def verify_link(key: str, ip: str, type: str):
    return {"success": True}




import json

@app.get("/get-config")
async def get_config():
    with open("links_config.json", "r", encoding="utf-8") as f:
        data = json.load(f)  # <-- QUAN TRỌNG
    return data


@app.get("/update-ip")
async def update_ip(key: str, ip: str, limit_reached: str = "false"):
    is_blocked = limit_reached.lower() == "true"
    storage_web_status[key] = {"ip": ip, "is_blocked": is_blocked}
    print(f"📡 Web xác nhận: Key {key} | IP {ip} | Blocked: {is_blocked}")
    return {"status": "success"}

# --- 4. CHẠY SERVER API TRONG LUỒNG RIÊNG ---

import os

def run_api_server():
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

threading.Thread(target=run_api_server, daemon=True).start()


# --- 5. CÁC HÀM HỖ TRỢ (ADMIN/JSON) ---
def load_admins():
    try:
        with open(ADMIN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        default_admins = [123456789012345678] # Thay ID của ông vào đây
        with open(ADMIN_FILE, "w", encoding="utf-8") as f:
            json.dump(default_admins, f)
        return default_admins

# --- 6. CODE BOT DISCORD CỦA ÔNG TIẾP TỤC Ở ĐÂY ---
# bot = commands.Bot(command_prefix="!", intents=...)
# @bot.command()...
# Tải danh sách admin khi chạy bot
list_admins = load_admins()
# Lấy đại diện 1 ID để gửi thông báo (thường là người đầu tiên trong danh sách)
ADMIN_ID = list_admins[0] if list_admins else None
def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4, ensure_ascii=False)
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def save_json(path, data_save):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_save, f, indent=4, ensure_ascii=False)

data = load_json(DATA_FILE, {"orders": []})
admins_list = load_json(ADMIN_FILE, [OWNER_ID])
# Ưu tiên load từ file banggia.json nếu có, nếu không thì dùng DEFAULT_PRICES
# Load dữ liệu từ file lên
bang_gia = load_json(PRICE_FILE, DEFAULT_PRICES)

# LOGIC GỘP DỮ LIỆU: Đảm bảo không mất mục gốc
for category, items in DEFAULT_PRICES.items():
    if category not in bang_gia:
        bang_gia[category] = items # Nếu file thiếu danh mục (ví dụ Sea Event), bù vào ngay
    else:
        # Nếu danh mục có rồi, kiểm tra xem có thiếu món gốc nào không thì bù vào món đó
        for item_name, price in items.items():
            if item_name not in bang_gia[category]:
                bang_gia[category][item_name] = price

save_json(PRICE_FILE, bang_gia) # Lưu lại bản đã gộp đầy đủ
def is_admin(user_id): 
    return user_id in admins_list or user_id == OWNER_ID

def format_money(x): 
    return f"{int(x):,}đ"

# ================= HỆ THỐNG ĐẾM NGƯỢC =================
async def code_countdown_task(order_id, user_id):
    try:
        user = await bot.fetch_user(user_id)
        for i in range(15, 0, -1):
            order = next((o for o in data["orders"] if o["id"] == order_id), None)
            if not order or not order.get("waiting_code") or order["status"] != "dang_cay":
                return
            await user.send(f"⏳ **NHẮC NHỞ:** Admin cần mã cho đơn `{order['don']}`. Bạn còn **{i} phút** để dùng `/malogin`!")
            await asyncio.sleep(60)

        final_check = next((o for o in data["orders"] if o["id"] == order_id), None)
        if final_check and final_check.get("waiting_code"):
            final_check["status"] = "huy"
            final_check["waiting_code"] = False
            save_json(DATA_FILE, data)
            await user.send(f"❌ **HỦY ĐƠN:** Đơn `{final_check['don']}` đã bị hủy tự động do không gửi mã kịp lúc.")
    except: pass

# ================= VIEWS XỬ LÝ ĐƠN =================
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

def generate_random_key():
    # Tạo chuỗi ngẫu nhiên 12 ký tự cho Key
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=12))

class OrderActionView(discord.ui.View):
    def __init__(self, order_id, admin_id):
        super().__init__(timeout=None)
        self.order_id = order_id
        self.admin_id = admin_id

    # ... Giữ nguyên các nút @discord.ui.button khác (Hoàn thành, Hủy...) ...

    @discord.ui.button(label="❌ Báo lỗi TK/MK", style=discord.ButtonStyle.danger)
    async def report_error(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 1. Tìm đơn hàng trong data
        order = next((o for o in data["orders"] if o["id"] == self.order_id), None)
        if not order:
            return await interaction.response.send_message("❌ Không tìm thấy đơn hàng!", ephemeral=True)

        user_id = order['owner']
        
        # 2. Gửi Embed thông báo cho khách hàng
        try:
            user = await interaction.client.fetch_user(user_id)
            embed = discord.Embed(
                title="⚠️ CẢNH BÁO: SAI THÔNG TIN ĐĂNG NHẬP",
                description=f"Admin thông báo đơn hàng **{order['don']}** (Mã: `{self.order_id}`) bị sai tài khoản hoặc mật khẩu.",
                color=0xe74c3c
            )
            embed.add_field(
                name="🛠 Cách xử lý", 
                value="Vui lòng sử dụng lệnh `/suathongtin` ngay tại Bot để cập nhật lại thông tin đúng."
            )
            embed.set_footer(text="Nếu không sửa, đơn hàng sẽ không thể thực hiện.")
            
            await user.send(embed=embed)
            await interaction.response.send_message(f"✅ Đã gửi thông báo lỗi tới {user.mention}!", ephemeral=True)
        except:
            await interaction.response.send_message("❌ Khách khóa DM, không thể gửi thông báo trực tiếp!", ephemeral=True)

class ConfirmHuyDon(discord.ui.View):
    def __init__(self, order_info, admin_id):
        super().__init__(timeout=30)
        self.order_info = order_info
        self.admin_id = admin_id

    @discord.ui.button(label="Xác nhận Hủy", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        uid = str(interaction.user.id)
        order_id = self.order_info['id']
        refund_amount = self.order_info['money']
        game_user = self.order_info.get('username', 'N/A')

        # 1. Hoàn tiền cho người dùng
        if uid not in data["users"]:
            data["users"][uid] = {"balance": 0, "total_nap": 0}
        data["users"][uid]["balance"] += refund_amount

        # 2. Xóa đơn khỏi dữ liệu
        data["orders"] = [o for o in data["orders"] if o["id"] != order_id]
        save_json(DATA_FILE, data)

        # 3. Phản hồi cho người dùng
        await interaction.response.edit_message(
            content=f"✅ Đã hủy đơn `{order_id}` thành công. Bạn đã được hoàn lại **{format_money(refund_amount)}** vào ví!",
            view=None
        )

        # 4. Thông báo cho Admin
        try:
            admin = await interaction.client.fetch_user(self.admin_id)
            embed_ad = discord.Embed(title="⚠️ KHÁCH TỰ HỦY ĐƠN", color=0xffa500)
            embed_ad.add_field(name="Người hủy", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
            embed_ad.add_field(name="Mã đơn", value=f"`{order_id}`", inline=True)
            embed_ad.add_field(name="Dịch vụ", value=f"{self.order_info['don']}", inline=False)
            embed_ad.add_field(name="Tài khoản Game", value=f"`{game_user}`", inline=False)
            embed_ad.add_field(name="Số tiền đã hoàn", value=f"{format_money(refund_amount)}", inline=True)
            
            await admin.send(embed=embed_ad)
        except:
            pass

    @discord.ui.button(label="Quay lại", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Đã hủy thao tác.", view=None)


class OrderView(discord.ui.View):
    def __init__(self, order_id: str):
        super().__init__(timeout=None)
        self.order_id = order_id

    @discord.ui.button(label="Đã Nhận", style=discord.ButtonStyle.primary, custom_id="btn_acc")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_admin(interaction.user.id): return
        order = next((o for o in data["orders"] if o["id"] == self.order_id), None)
        if order:
            order["status"] = "dang_cay"
            save_json(DATA_FILE, data)
            try:
                u = await bot.fetch_user(order["owner"])
                await u.send(f"✅ **THÔNG BÁO:** Đơn hàng `{order['don']}` của bạn đã được Admin nhận cày!")
            except: pass
            await interaction.response.edit_message(content=f"📥 **ĐÃ NHẬN:** {order['don']}", view=None)

    @discord.ui.button(label="Báo Lỗi", style=discord.ButtonStyle.danger, custom_id="btn_err")
    async def error(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_admin(interaction.user.id): return
        order = next((o for o in data["orders"] if o["id"] == self.order_id), None)
        if order:
            try:
                u = await bot.fetch_user(order["owner"])
                await u.send(f"⚠️ **SAI TÀI KHOẢN:** Đơn `{order['don']}` lỗi đăng nhập. Hãy dùng `/suathongtin`!")
                await interaction.response.send_message("Đã gửi tin báo lỗi!", ephemeral=True)
            except: pass

class WorkingOrderView(discord.ui.View):
    def __init__(self, order_id: str):
        super().__init__(timeout=None)
        self.order_id = order_id

    @discord.ui.button(label="Hoàn Thành", style=discord.ButtonStyle.success, custom_id="btn_done")
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_admin(interaction.user.id): return
        order = next((o for o in data["orders"] if o["id"] == self.order_id), None)
        if order:
            order["status"] = "da_xong"
            save_json(DATA_FILE, data)
            try:
                u = await bot.fetch_user(order["owner"])
                await u.send(f"🎉 **HOÀN THÀNH:** Đơn `{order['don']}` đã xong!")
            except: pass
            await interaction.response.edit_message(content=f"✅ **HOÀN TẤT:** {order['don']}", view=None)

    @discord.ui.button(label="Lấy Mã", style=discord.ButtonStyle.primary, custom_id="btn_code")
    async def get_code(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_admin(interaction.user.id): return
        order = next((o for o in data["orders"] if o["id"] == self.order_id), None)
        if order:
            order["waiting_code"] = True
            save_json(DATA_FILE, data)
            bot.loop.create_task(code_countdown_task(self.order_id, order["owner"]))
            await interaction.response.send_message("Đã yêu cầu khách lấy mã!", ephemeral=True)

# ================= LỆNH QUẢN TRỊ ADMIN =================


@bot.tree.command(name="themitem", description="[Admin] Thêm/Sửa món đồ (Gõ tên cũ để sửa giá, tên mới để thêm)")

@app_commands.describe(

    danh_muc="Chọn danh mục có sẵn hoặc nhập danh mục mới",

    ten_mon="Chọn món có sẵn để sửa hoặc nhập tên món mới",

    gia_tien="Giá tiền mới"

)

async def themitem(interaction: discord.Interaction, danh_muc: str, ten_mon: str, gia_tien: int):

    if not is_admin(interaction.user.id): 

        return await interaction.response.send_message("❌ Bạn không có quyền!", ephemeral=True)

    

    global bang_gia

    await interaction.response.defer()



    try:

        # Nếu danh mục chưa tồn tại, tự động tạo mới

        if danh_muc not in bang_gia:

            bang_gia[danh_muc] = {}

            action_text = f"Tạo danh mục mới `{danh_muc}` và thêm món"

        else:

            if ten_mon in bang_gia[danh_muc]:

                action_text = f"Cập nhật giá cho món"

            else:

                action_text = f"Thêm món mới vào mục `{danh_muc}`"



        # Cập nhật/Thêm dữ liệu

        bang_gia[danh_muc][ten_mon] = gia_tien

        save_json(PRICE_FILE, bang_gia)

        

        # Thông báo

        embed = discord.Embed(title="📢 BẢNG GIÁ ĐÃ THAY ĐỔI", color=0x3498db)

        embed.description = f"**Hành động:** {action_text}"

        embed.add_field(name="📂 Danh mục", value=f"**{danh_muc}**", inline=True)

        embed.add_field(name="📦 Dịch vụ", value=f"`{ten_mon}`", inline=True)

        embed.add_field(name="💰 Giá tiền", value=f"**{format_money(gia_tien)}**", inline=True)

        embed.set_footer(text=f"Admin: {interaction.user.name}")

        

        await interaction.followup.send(embed=embed)



    except Exception as e:

        await interaction.followup.send(f"❌ Lỗi: {e}")



# --- PHẦN GỢI Ý TỰ ĐỘNG (AUTOCOMPLETE) ---

@themitem.autocomplete('danh_muc')

async def themitem_category_autocomplete(interaction: discord.Interaction, current: str):

    cats = list(bang_gia.keys())

    return [

        app_commands.Choice(name=c, value=c)

        for c in cats if current.lower() in c.lower()

    ][:25]



@themitem.autocomplete('ten_mon')

async def themitem_item_autocomplete(interaction: discord.Interaction, current: str):

    # Lấy giá trị danh mục mà người dùng đang chọn ở ô phía trên

    danh_muc_chon = interaction.namespace.danh_muc

    if not danh_muc_chon or danh_muc_chon not in bang_gia:

        return []

    

    items = list(bang_gia[danh_muc_chon].keys())

    return [

        app_commands.Choice(name=i, value=i)

        for i in items if current.lower() in i.lower()

    ][:25]


@bot.tree.command(name="xoaitem", description="[Admin] Xóa một món đồ khỏi bảng giá")
async def xoaitem(interaction: discord.Interaction):
    if not is_admin(interaction.user.id): 
        return await interaction.response.send_message("❌ Bạn không có quyền!", ephemeral=True)
    
    if not bang_gia: 
        return await interaction.response.send_message("❌ Bảng giá đang trống!", ephemeral=True)

    view = discord.ui.View()
    opts = [discord.SelectOption(label=k) for k in bang_gia.keys() if bang_gia[k]]
    sel_cat = discord.ui.Select(placeholder="Chọn danh mục có món cần xóa...", options=opts)

    async def cat_cb(i: discord.Interaction):
        muc = sel_cat.values[0]
        view_itm = discord.ui.View()
        itms = [discord.SelectOption(label=n) for n in bang_gia[muc].keys()]
        sel_itm = discord.ui.Select(placeholder="Chọn món đồ cụ thể để xóa...", options=itms)

        async def itm_cb(i2: discord.Interaction):
            ten_mon = sel_itm.values[0]
            
            # Xóa khỏi bảng giá và lưu file
            del bang_gia[muc][ten_mon]
            save_json(PRICE_FILE, bang_gia)
            
            # Thông báo công khai cho mọi người
            embed = discord.Embed(title="🗑️ DỊCH VỤ ĐÃ NGỪNG CUNG CẤP", color=0xff0000)
            embed.description = f"Admin {i2.user.mention} vừa xóa một dịch vụ khỏi bảng giá."
            embed.add_field(name="📂 Danh mục", value=f"**{muc}**", inline=True)
            embed.add_field(name="📦 Dịch vụ đã xóa", value=f"`{ten_mon}`", inline=True)
            embed.set_footer(text="Gõ /banggia để cập nhật danh sách còn lại.")
            
            await i2.response.edit_message(content=None, embed=embed, view=None)

        sel_itm.callback = itm_cb
        view_itm.add_item(sel_itm)
        await i.response.edit_message(content=f"Bạn đang chọn mục **{muc}**, hãy chọn món muốn xóa:", view=view_itm)

    sel_cat.callback = cat_cb
    view.add_item(sel_cat)
    await interaction.response.send_message("Lưu ý: Xóa xong sẽ thông báo công khai trong nhóm!", view=view, ephemeral=True)
@bot.tree.command(name="themadmin", description="Thêm một người làm Admin bot")
async def themadmin(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.id != OWNER_ID: return await interaction.response.send_message("Chỉ Chủ Bot mới dùng được!", ephemeral=True)
    if user.id not in admins_list:
        admins_list.append(user.id); save_json(ADMIN_FILE, admins_list)
        await interaction.response.send_message(f"✅ Đã thêm **{user.display_name}** làm Admin.", ephemeral=True)

@bot.tree.command(name="xoaadmin", description="Xóa quyền Admin")
async def xoaadmin(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.id != OWNER_ID: return await interaction.response.send_message("Chỉ Chủ Bot mới dùng được!", ephemeral=True)
    if user.id in admins_list and user.id != OWNER_ID:
        admins_list.remove(user.id); save_json(ADMIN_FILE, admins_list)
        await interaction.response.send_message(f"🗑️ Đã xóa quyền Admin của **{user.display_name}**.", ephemeral=True)

@bot.tree.command(name="xemadmin", description="Xem danh sách Admin")
async def xemadmin(interaction: discord.Interaction):
    if not is_admin(interaction.user.id): return
    txt = "\n".join([f"- <@{a}> (ID: `{a}`)" for a in admins_list])
    embed = discord.Embed(title="DANH SÁCH QUẢN TRỊ VIÊN", description=txt, color=0xFFA500)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ================= LỆNH KHÁCH HÀNG =================

@bot.tree.command(name="start", description="Hướng dẫn sử dụng các lệnh của Bot")
async def start(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📚 HƯỚNG DẪN SỬ DỤNG BOT QUẢN LÝ CÀY THUÊ",
        description="Chào mừng bạn! Dưới đây là danh sách các lệnh được phân loại theo quyền hạn:",
        color=0x3498db
    )

    # --- PHẦN 1: DÀNH CHO NGƯỜI DÙNG (KHÁCH HÀNG) ---
    # --- PHẦN 1: DÀNH CHO NGƯỜI DÙNG (KHÁCH HÀNG) ---

    user_commands = (
        "**`/info`**: Xem số dư ví và danh sách đơn hàng của bạn.\n"
        "**`/banggia`**: Xem menu dịch vụ cày thuê và giá cả.\n"
        "**`/datdon`**: Đặt đơn cày thuê mới.\n"
        "**`/huydon`**: 🗑️ **Tự hủy đơn & hoàn tiền** (Chỉ khi đơn chưa có người nhận).\n"
        "**`/napthe`**: Nạp tiền vào ví qua hệ thống Thesieure.\n"
        "**`/check`**: Kiểm tra trạng thái/tiến độ đơn hàng.\n"
        "**`/malogin`**: Gửi mã xác minh tài khoản game (nếu cần).\n"
        "**`/vuotlink`**: 🔗 Lấy link vượt để kiếm tiền / nhận key.\n"
        "**`/nhapkey`**: 🔑 Nhập key sau khi vượt link để nhận thưởng."
)





    embed.add_field(name="👤 DÀNH CHO NGƯỜI DÙNG", value=user_commands, inline=False)

    # --- PHẦN 2: DÀNH CHO ADMIN (THỢ CÀY) ---
    admin_commands = (
        "**`/doncay`**: Xem và nhận các đơn hàng đang chờ.\n"
        "**`/donnhan`**: Quản lý các đơn hàng bạn đang xử lý.\n"
        "**`/themitem`**: Thêm/Sửa dịch vụ trong bảng giá.\n"
        "**`/xoaitem`**: Xóa món đồ khỏi bảng giá.\n"
        "**`/suathongtin`**: Sửa tài khoản/mật khẩu đơn hàng cho khách.\n"
        "**`/panel`**: Bảng điều khiển quản lý đơn hàng toàn diện."
    )
    embed.add_field(name="🛡️ DÀNH CHO ADMIN", value=admin_commands, inline=False)

    # --- PHẦN 3: DÀNH CHO OWNER (CHỦ BOT) ---
    owner_commands = (
        "**`/setmoney`**: 💰 **Chỉnh sửa số dư tài khoản cho khách**.\n"
        "**`/themadmin`**: Cấp quyền Admin cho thành viên.\n"
        "**`/xoaadmin`**: Thu hồi quyền Admin.\n"
        "**`/xemadmin`**: Xem danh sách đội ngũ Admin hiện tại."
    )
    embed.add_field(name="👑 DÀNH CHO OWNER", value=owner_commands, inline=False)

    embed.set_footer(text="💡 Lưu ý: Các lệnh Admin/Owner chỉ hoạt động nếu bạn có quyền tương ứng.")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="info", description="Xem ví tiền và danh sách đơn hàng của bạn")
async def info(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    # Lấy dữ liệu ví tiền
    u_data = data["users"].get(uid, {"balance": 0, "total_nap": 0})
    
    embed = discord.Embed(title="💳 THÔNG TIN TÀI KHOẢN", color=0x2ecc71)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.add_field(name="💰 Số dư hiện tại", value=f"**{format_money(u_data['balance'])}**", inline=True)
    embed.add_field(name="📈 Tổng nạp", value=f"{format_money(u_data['total_nap'])}", inline=True)

    # --- PHẦN HIỂN THỊ ĐƠN HÀNG ---
    # Lọc danh sách đơn hàng của người dùng này (so khớp ID người dùng)
    user_orders = [o for o in data["orders"] if str(o.get('owner')) == uid]

    if user_orders:
        order_text = ""
        for o in user_orders:
            # Chuyển đổi trạng thái sang tiếng Việt cho dễ nhìn
            status_map = {
                "chua_nhan": "⏳ Đang chờ",
                "dang_cay": "🚀 Đang cày",
                "da_xong": "✅ Hoàn thành"
            }
            tt = status_map.get(o.get('status'), "❓ Không rõ")
            order_text += f"• Mã: `{o['id']}` - **{o['don']}**\n└ Trạng thái: {tt}\n"
        
        embed.add_field(name="📦 Đơn hàng của bạn", value=order_text, inline=False)
    else:
        embed.add_field(name="📦 Đơn hàng của bạn", value="*Bạn chưa có đơn hàng nào.*", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="setmoney", description="[Owner] Chỉnh tiền cho khách")
async def setmoney(interaction: discord.Interaction, user: discord.Member, amount: int):
    # Kiểm tra xem người dùng có phải là Owner không
    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Chỉ có **Owner (Chủ Bot)** mới có quyền sử dụng lệnh này!", ephemeral=True)
    
    uid = str(user.id)
    
    # Khởi tạo dữ liệu nếu user chưa có trong hệ thống
    if uid not in data["users"]: 
        data["users"][uid] = {"balance": 0, "total_nap": 0}
    
    # Cập nhật số dư
    data["users"][uid]["balance"] = amount
    save_json(DATA_FILE, data)
    
    await interaction.response.send_message(f"✅ Đã đặt số dư của {user.mention} thành **{format_money(amount)}**")


# --- PHẦN 1: LỆNH NẠP THẺ ---




import random
import requests


# lưu tạm request_id -> user_id
pending_cards = {}

from discord import app_commands

@bot.tree.command(name="napthe", description="Nạp thẻ cào vào ví")
@app_commands.choices(
    telco=[
        app_commands.Choice(name="Viettel", value="VIETTEL"),
        app_commands.Choice(name="Mobifone", value="MOBIFONE"),
        app_commands.Choice(name="Vinaphone", value="VINAPHONE"),
        app_commands.Choice(name="Vietnamobile", value="VIETNAMOBILE"),
    ],
    amount=[
        app_commands.Choice(name="10.000đ", value=10000),
        app_commands.Choice(name="20.000đ", value=20000),
        app_commands.Choice(name="50.000đ", value=50000),
        app_commands.Choice(name="100.000đ", value=100000),
        app_commands.Choice(name="200.000đ", value=200000),
        app_commands.Choice(name="500.000đ", value=500000),
    ]
)
async def napthe(
    interaction: discord.Interaction,
    telco: app_commands.Choice[str],
    amount: app_commands.Choice[int],
    code: str,
    serial: str
):
    uid = str(interaction.user.id)

    request_id = str(uuid.uuid4())

    data["pending_cards"][request_id] = {
        "uid": uid,
        "amount": amount.value
    }
    save_data()

    payload = {
        "telco": telco.value,
        "code": code,
        "serial": serial,
        "amount": amount.value,
        "request_id": request_id,
        "partner_id": PARTNER_ID,
        "sign": PARTNER_KEY
    }

    # gửi API...
    await interaction.response.send_message(
        f"⏳ Đã gửi thẻ {amount.name} ({telco.name}), đang xử lý...",
        ephemeral=True
    )

@bot.tree.command(name="nhapkey", description="Nhập mã Key để nhận tiền thưởng")
async def nhapkey(interaction: discord.Interaction, key: str):
    uid = str(interaction.user.id)
    user_key = key.strip()
    today = datetime.now().strftime("%Y-%m-%d")

    # 1. Tải dữ liệu Key và dữ liệu chính (data.json)
    all_keys = load_json(KEYS_STORAGE_FILE, {"ActiveTasks": {}})
    active_tasks = all_keys.get("ActiveTasks", {})
    
    # Load data.json để cập nhật số dư và giới hạn IP
    # Giả sử biến 'data' của ông đã được load từ data.json
    if "ip_limits" not in data: data["ip_limits"] = {}

    # 2. Kiểm tra Key có tồn tại không
    if user_key not in active_tasks:
        return await interaction.response.send_message("❌ Mã Key không hợp lệ hoặc đã được sử dụng!", ephemeral=True)

    # 3. Lấy dữ liệu Web đã gửi về thông qua FastAPI
    web_data = storage_web_status.get(user_key)

    if not web_data:
        return await interaction.response.send_message("❌ Web chưa gửi dữ liệu xác nhận. Vui lòng vượt link đến trang cuối!", ephemeral=True)

    # 4. Kiểm tra trạng thái chặn từ phía Web (Lượt click trên trình duyệt)
    if web_data.get("is_blocked"):
        return await interaction.response.send_message(
            f"❌ Hệ thống thông báo: IP của bạn ({web_data['ip']}) đã hết lượt vượt link này trên trình duyệt hôm nay!", 
            ephemeral=True
        )

    task_info = active_tasks[user_key]
    choice = task_info.get("type", "link4m")
    user_ip = web_data['ip']

    # --- KIỂM TRA CHỐNG CLONE IP TẠI ĐÂY ---
    ip_key = f"{user_ip}_{choice}"
    ip_usage = data["ip_limits"].get(ip_key, {"count": 0, "date": today})

    # Nếu IP này đã dùng hết lượt trên Bot (dù Web chưa chặn)
    # Lấy giới hạn từ LINK_CONFIGS (nếu có) hoặc mặc định là 2
    max_limit = 2 
    if 'LINK_CONFIGS' in globals() and choice in LINK_CONFIGS:
        max_limit = LINK_CONFIGS[choice]['max']

    if ip_usage["date"] == today and ip_usage["count"] >= max_limit:
         return await interaction.response.send_message(f"❌ Địa chỉ mạng này ({user_ip}) đã nhận thưởng {max_limit} lần cho nhiệm vụ này rồi!", ephemeral=True)

    # 5. TIẾN HÀNH CỘNG TIỀN VÀ CẬP NHẬT GIỚI HẠN
    reward_amount = task_info["amount"]

    if uid not in data["users"]:
        data["users"][uid] = {"balance": 0, "total_nap": 0, "daily_limit": {}}

    # Cộng tiền
    data["users"][uid]["balance"] += reward_amount
    
    # Cập nhật giới hạn User (daily_limit)
    user_limits = data["users"][uid].get("daily_limit", {})
    if choice not in user_limits or user_limits[choice]["date"] != today:
        user_limits[choice] = {"count": 1, "date": today}
    else:
        user_limits[choice]["count"] += 1
    data["users"][uid]["daily_limit"] = user_limits

    # Cập nhật giới hạn IP (ip_limits) để chặn clone
    data["ip_limits"][ip_key] = {"count": ip_usage["count"] + 1, "date": today}
    
    # Lưu lại file data.json
    save_json("data.json", data) 

    # 6. Xóa dữ liệu tạm
    del active_tasks[user_key]
    save_json(KEYS_STORAGE_FILE, all_keys)
    if user_key in storage_web_status: 
        del storage_web_status[user_key]

    # 7. Phản hồi thành công
    embed = discord.Embed(title="✅ XÁC MINH THÀNH CÔNG", color=0x2ecc71)
    embed.add_field(name="💰 Tiền thưởng", value=f"+**{reward_amount:,} VNĐ**", inline=True)
    embed.add_field(name="💳 Số dư mới", value=f"**{data['users'][uid]['balance']:,} VNĐ**", inline=True)
    embed.set_footer(text=f"IP xác thực: {user_ip}")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
import requests



LINK_CONFIGS = {
    "link4m": {
        "name": "Link4M",
        "price": 550,
        "max": 2,
        "token": "6992c01de896613eeb1c7976",
        "api_url": "https://link4m.co/api-shorten/v2?api={token}&url={url}"
    },
    "yeumoney": {
        "name": "YeuMoney",
        "price": 600,
        "max": 3,
        "token": "d68dab4fa90dd7fb1763a886c4f34541e28dabde53d32bd3aa5be0ce3bc031a6",
        "api_url": "https://yeumoney.com/QL_api.php?token={token}&format=json&url={url}"
    },
     "4mmo": {
        "name": "4MMO",
        "price": 400,
        "max": 2,
        "token": "ccb887e55fd846e88a250c1644054e5c0e95d919",
        "api_url": "https://4mmo.net/api?api={token}&url={url}"
    },
   "nhapma": {
        "name": "NhapMa",
        "price": 400, 
        "max": 3,
        "token": "99087d7f-e1df-4d96-9e87-c38337633c11", 
        "api_url": "https://service.nhapma.com/api?token={token}&url={url}"
    },
    "linkngon": {
    "name": "LinkNgon",
    "price": 500,
    "max": 2,
    "token": "4ui1TCdMeWMWU2LMzjDCwm093I5kb9ZaOaQTNUz7EkdzNS",
    "api_url": "https://linkngon.io/api?api={token}&url={url}"
    }

}



from urllib.parse import quote

def get_shortened_link(source_key, target_url):
    try:
        conf = LINK_CONFIGS.get(source_key)
        if not conf:
            return {"status":"error","message":"Nguồn không tồn tại"}

        encoded_url = quote(target_url, safe="")
        api_link = conf["api_url"].format(
            token=conf["token"],
            url=encoded_url
        )

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        response = requests.get(api_link, headers=headers, timeout=30)

        if response.status_code != 200:
            return {
                "status":"error",
                "message": f"HTTP {response.status_code}"
            }

        try:
            data = response.json()
        except:
            return {
                "status":"error",
                "message":"API không trả JSON"
            }

        short_url = (
            data.get("shortlink")
            or data.get("url")
            or data.get("shortenedUrl")
        )

        if short_url:
            return {"status":"success","shortenedUrl":short_url}

        return {"status":"error","message":str(data)}

    except Exception as e:
        return {"status":"error","message":str(e)}

@bot.tree.command(name="vuotlink", description="Chọn loại link để cày tiền")
async def vuotlink(interaction: discord.Interaction):

    user_id = str(interaction.user.id)
    today = datetime.now().strftime("%Y-%m-%d")

    view = discord.ui.View()
    select = discord.ui.Select(placeholder="Danh sách nhiệm vụ hôm nay...")

    for key, info in LINK_CONFIGS.items():
        select.add_option(
            label=f"{info['name']} ({info['price']:,}đ)",
            value=key,
            description=f"Giới hạn: {info['max']} lần/ngày"
        )

    async def select_callback(inter: discord.Interaction):

        choice = select.values[0]
        config = LINK_CONFIGS[choice]

        # Load dữ liệu
        full_data = load_json(DATA_FILE, {"users": {}})

        # Check theo User ID בלבד
        user_daily = full_data["users"].get(user_id, {}).get(
            "daily_limit", {}
        ).get(choice, {"count": 0, "date": today})

        if user_daily["date"] == today and user_daily["count"] >= config["max"]:
            return await inter.response.send_message(
                f"❌ Bạn đã hết lượt vượt **{config['name']}** hôm nay!",
                ephemeral=True
            )

        await inter.response.defer(ephemeral=True)
        # Tạo link
        
        new_key = str(uuid.uuid4())

        target_url = f"{BASE_URL_BLOG}?ma={new_key}&type={choice}"

        data_api = get_shortened_link(choice, target_url)

        if data_api and data_api.get("status") == "success":

            all_keys = load_json(KEYS_STORAGE_FILE, {"ActiveTasks": {}})

            if "ActiveTasks" not in all_keys:
                all_keys["ActiveTasks"] = {}

            all_keys["ActiveTasks"][new_key] = {
                "user_id": user_id,
                "amount": config["price"],
                "type": choice
            }

            save_json(KEYS_STORAGE_FILE, all_keys)

            embed = discord.Embed(
                title=f"🚀 NHIỆM VỤ: {config['name']}",
                color=0x3498db
            )
            embed.description = (
                f"Phưởng thưởng: **{config['price']:,} VNĐ**\n\n"
                f"🔗 **[NHẤN VÀO ĐÂY ĐỂ VƯỢT LINK]({data_api['shortenedUrl']})**"
            )

            await inter.followup.send(embed=embed, ephemeral=True)

        else:
            await inter.followup.send(
                f"❌ Lỗi API {config['name']}.",
                ephemeral=True
            )

    select.callback = select_callback
    view.add_item(select)

    await interaction.response.send_message(
        "Chọn nhiệm vụ:",
        view=view,
        ephemeral=True
    )

@bot.tree.command(name="banggia", description="Xem menu dịch vụ đầy đủ")
async def banggia_cmd(interaction: discord.Interaction):
    # Bước 1: Gửi tín hiệu "đang xử lý" để tránh lỗi Unknown Interaction
    await interaction.response.defer() 
    
    global bang_gia
    if not bang_gia:
        return await interaction.followup.send("❌ Bảng giá hiện đang trống!")
    
    embed = discord.Embed(
        title="📜 MENU DỊCH VỤ CÀY THUÊ", 
        description="Dưới đây là danh sách dịch vụ mới nhất.",
        color=0x00FFCC
    )
    
    found_any = False
    for cat in bang_gia:
        items = bang_gia[cat]
        if items:
            text_list = [f"• {name}: **{format_money(price)}**" for name, price in items.items()]
            val = "\n".join(text_list)
            embed.add_field(name=f"💎 {cat.upper()}", value=val, inline=False)
            found_any = True
            
    if not found_any:
        return await interaction.followup.send("❌ Hiện chưa có món đồ nào!")

    # Bước 2: Dùng followup.send vì đã dùng defer ở trên
    await interaction.followup.send(embed=embed)



@bot.tree.command(name="datdon", description="Đặt đơn cày thuê mới")
async def datdon(interaction: discord.Interaction):
    # Bước 1: Hiện bảng nhập Tài khoản / Mật khẩu
    class DDModal(discord.ui.Modal, title="THÔNG TIN TÀI KHOẢN"):
        u = discord.ui.TextInput(label="Tài khoản (Username/Email/Phone)", placeholder="Nhập tên đăng nhập...", required=True)
        p = discord.ui.TextInput(label="Mật khẩu (Password)", placeholder="Nhập mật khẩu...", required=True)
        
        async def on_submit(self, i: discord.Interaction):
            if not bang_gia:
                return await i.response.send_message("❌ Bảng giá hiện đang trống!", ephemeral=True)
            
            # Bước 2: Hiện danh sách danh mục (Select Menu 1)
            view = discord.ui.View()
            opts = [discord.SelectOption(label=k) for k in bang_gia.keys() if bang_gia[k]]
            if not opts:
                return await i.response.send_message("❌ Hiện không có danh mục nào khả dụng.", ephemeral=True)
                
            sel_cat = discord.ui.Select(placeholder="--- Chọn danh mục dịch vụ ---", options=opts)

            async def cat_cb(i2: discord.Interaction):
                muc = sel_cat.values[0]
                view_itm = discord.ui.View()
                itms = [discord.SelectOption(label=f"{n}", description=f"Giá: {format_money(p)}", value=n) 
                        for n, p in bang_gia[muc].items()]
                sel_itm = discord.ui.Select(placeholder=f"Chọn món trong mục {muc}...", options=itms)

                async def itm_cb(i3: discord.Interaction):
                    uid = str(i3.user.id)
                    ten_mon = sel_itm.values[0]
                    gia_mon = bang_gia[muc][ten_mon]

                    # --- KIỂM TRA VÀ KHỞI TẠO DỮ LIỆU NGƯỜI DÙNG ---
                    if uid not in data["users"]:
                        data["users"][uid] = {"balance": 0, "total_nap": 0}
                    
                    user_bal = data["users"][uid].get("balance", 0)

                    # --- KIỂM TRA SỐ DƯ ---
                    if user_bal < gia_mon:
                        return await i3.response.send_message(
                            f"❌ Bạn không đủ tiền! Ví hiện có: `{format_money(user_bal)}`. Cần thêm `{format_money(gia_mon - user_bal)}`", 
                            ephemeral=True
                        )

                    # --- ĐỦ TIỀN: TIẾN HÀNH TRỪ TIỀN VÀ TẠO ĐƠN ---
                    data["users"][uid]["balance"] -= gia_mon
                    
                    oid = str(uuid.uuid4())[:8].upper()
                    new_order = {
                        "id": oid,
                        "owner": i3.user.id,
                        "username": self.u.value,
                        "password": self.p.value,
                        "don": ten_mon,
                        "money": gia_mon,
                        "status": "chua_nhan"
                    }
                    data["orders"].append(new_order)
                    save_json(DATA_FILE, data)

                    # --- THÔNG BÁO CHO NGƯỜI DÙNG ---
                    embed_user = discord.Embed(title="✅ ĐẶT ĐƠN THÀNH CÔNG!", color=0x2ecc71)
                    embed_user.add_field(name="🆔 Mã đơn", value=f"`{oid}`", inline=True)
                    embed_user.add_field(name="📦 Dịch vụ", value=f"`{ten_mon}`", inline=True)
                    embed_user.add_field(name="💰 Số dư còn lại", value=f"**{format_money(data['users'][uid]['balance'])}**", inline=False)
                    embed_user.set_footer(text="Vui lòng chờ Admin duyệt đơn.")
                    
                    await i3.response.edit_message(content=None, embed=embed_user, view=None)

                    # --- THÔNG BÁO CHO ADMIN ---
                    embed_admin = discord.Embed(title="🆕 CÓ ĐƠN HÀNG MỚI!", color=0xe74c3c)
                    embed_admin.add_field(name="👤 Khách hàng", value=f"{i3.user.mention} ({i3.user.name})", inline=False)
                    embed_admin.add_field(name="🆔 Mã đơn", value=f"`{oid}`", inline=True)
                    embed_admin.add_field(name="📦 Dịch vụ", value=f"`{ten_mon}`", inline=True)
                    embed_admin.add_field(name="🔐 Tài khoản", value=f"||`{self.u.value}`||", inline=True)
                    embed_admin.add_field(name="🔑 Mật khẩu", value=f"||`{self.p.value}`||", inline=True)
                    embed_admin.add_field(name="💰 Giá tiền", value=f"**{format_money(gia_mon)}**", inline=False)
                    embed_admin.set_footer(text="Dùng lệnh /doncay để nhận đơn này.")

                    for admin_id in admins_list:
                        try:
                            adm = await bot.fetch_user(admin_id)
                            await adm.send(embed=embed_admin)
                        except:
                            pass

                sel_itm.callback = itm_cb
                view_itm.add_item(sel_itm)
                await i2.response.edit_message(content=f"📍 Danh mục: **{muc}**. Hãy chọn dịch vụ cụ thể:", view=view_itm)

            sel_cat.callback = cat_cb
            view.add_item(sel_cat)
            await i.response.send_message(f"Chào {i.user.mention}, mời bạn chọn dịch vụ:", view=view, ephemeral=True)

    await interaction.response.send_modal(DDModal())


async def account_autocomplete(interaction: discord.Interaction, current: str):
    uid = interaction.user.id
    # Lấy danh sách các đơn hàng của người dùng này chưa hoàn thành và chưa nhận
    # o.get('username') là tên tài khoản game bạn lưu khi đặt đơn
    choices = [
        app_commands.Choice(name=f"{o['username']} (Mã: {o['id']})", value=o['id'])
        for o in data["orders"] 
        if o["owner"] == uid and o["status"] == "chua_nhan" and current.lower() in o.get('username', '').lower()
    ]
    return choices[:25] # Discord chỉ cho phép tối đa 25 gợi ý


@bot.tree.command(name="huydon", description="Hủy đơn hàng bằng cách chọn tài khoản game")
@app_commands.describe(ma_don="Chọn tài khoản game bạn muốn hủy đơn (Gõ để tìm kiếm)")
@app_commands.autocomplete(ma_don=account_autocomplete) 
async def huydon(interaction: discord.Interaction, ma_don: str):
    await interaction.response.defer(ephemeral=True) 
    uid = interaction.user.id

    # 1. Tải danh sách Admin
    list_admins = load_admins() 
    target_admin = list_admins[0] if list_admins else None

    if not target_admin:
        return await interaction.followup.send("❌ Hệ thống chưa thiết lập Admin xử lý!", ephemeral=True)

    # 2. Tìm đơn hàng
    order = next((o for o in data["orders"] if o["id"] == ma_don and o["owner"] == uid), None)

    # 3. Kiểm tra tồn tại
    if not order:
        return await interaction.followup.send("❌ Không tìm thấy đơn hàng này hoặc đơn không thuộc quyền sở hữu của bạn!", ephemeral=True)

    # 4. Kiểm tra trạng thái nghiêm ngặt
    if order["status"] == "dang_cay":
        return await interaction.followup.send(
            f"🚫 **KHÔNG THỂ HỦY:** Đơn hàng `{order['username']}` đã được Admin nhận và đang thực hiện.", 
            ephemeral=True
        )
    
    if order["status"] == "da_xong":
        return await interaction.followup.send("❌ Đơn hàng này đã hoàn thành, không thể hoàn tiền!", ephemeral=True)

    # 5. Hiện nút xác nhận (ConfirmHuyDon giữ nguyên class của bạn)
    view = ConfirmHuyDon(order, target_admin) 
    await interaction.followup.send(
        content=f"❓ **XÁC NHẬN HỦY ĐƠN**\n"
                f"📝 Tài khoản: **{order['username']}**\n"
                f"📦 Dịch vụ: **{order['don']}**\n"
                f"💰 Tiền sẽ hoàn lại: **{format_money(order['money'])}**",
        view=view,
        ephemeral=True
    )
@bot.tree.command(name="check", description="Kiểm tra tiến độ")
async def check(interaction: discord.Interaction):
    u_orders = [o for o in data["orders"] if o["owner"] == interaction.user.id]
    if not u_orders: return await interaction.response.send_message("Bạn chưa có đơn nào!", ephemeral=True)
    view = discord.ui.View()
    opts = [discord.SelectOption(label=f"Đơn: {o['don']}", value=o['id']) for o in u_orders[-25:]]
    sel = discord.ui.Select(placeholder="Chọn đơn cần xem...", options=opts)
    async def cb(i: discord.Interaction):
        o = next(x for x in data["orders"] if x["id"] == sel.values[0])
        st = {"chua_nhan": "⏳ Chờ duyệt", "dang_cay": "🛠️ Đang cày", "da_xong": "✅ Hoàn thành", "huy": "❌ Đã hủy"}
        embed = discord.Embed(title=f" TIẾN ĐỘ: #{o['id']}", color=0x3498db)
        embed.add_field(name="Gói:", value=o['don'], inline=True)
        embed.add_field(name="Trạng thái:", value=st.get(o['status']), inline=True)
        await i.response.edit_message(embed=embed, view=None)
    sel.callback = cb; view.add_item(sel); await interaction.response.send_message("Chọn đơn hàng:", view=view, ephemeral=True)
@bot.tree.command(name="malogin", description="Gửi mã xác minh theo tài khoản game của bạn")
@app_commands.describe(
    tai_khoan="Chọn tài khoản game bạn đang đặt đơn",
    ma="Nhập mã xác minh (6 số hoặc mã dự phòng)"
)
async def malogin(interaction: discord.Interaction, tai_khoan: str, ma: str):
    # Tìm đơn hàng dựa trên Username và ID người dùng Discord
    # Phải kiểm tra status là 'dang_cay' để tránh gửi nhầm đơn cũ
    order = next((o for o in data["orders"] 
                  if o["username"] == tai_khoan 
                  and o["owner"] == interaction.user.id 
                  and o["status"] == "dang_cay"), None)
    
    if not order:
        return await interaction.response.send_message(
            f"❌ Không tìm thấy đơn hàng đang cày nào cho tài khoản `{tai_khoan}`!", 
            ephemeral=True
        )
    
    # Dừng vòng lặp đếm ngược 15 phút
    order["waiting_code"] = False 
    save_json(DATA_FILE, data)

    await interaction.response.send_message(f"✅ Đã gửi mã cho tài khoản `{tai_khoan}` thành công!", ephemeral=True)

    # Thông báo cho Admin
    embed_to_admin = discord.Embed(title="🔑 KHÁCH ĐÃ GỬI MÃ LOGIN", color=0x00ff00)
    embed_to_admin.add_field(name="🔐 Tài khoản", value=f"`{tai_khoan}`", inline=True)
    embed_to_admin.add_field(name="📦 Dịch vụ", value=f"{order['don']}", inline=True)
    embed_to_admin.add_field(name="👤 Khách hàng", value=f"{interaction.user.mention}", inline=False)
    embed_to_admin.add_field(name="🔢 MÃ XÁC MINH", value=f"**{ma}**", inline=False)
    embed_to_admin.set_footer(text=f"ID đơn liên quan: {order['id']}")
    
    for admin_id in admins_list:
        try:
            admin_user = await bot.fetch_user(admin_id)
            await admin_user.send(embed=embed_to_admin)
        except:
            pass

# --- PHẦN TỰ ĐỘNG GỢI Ý USERNAME CHO NGƯỜI DÙNG ---
@malogin.autocomplete('tai_khoan')
async def malogin_username_autocomplete(interaction: discord.Interaction, current: str):
    # Lấy danh sách Username của các đơn 'dang_cay' thuộc về người dùng này
    user_usernames = list(set([
        o["username"] for o in data["orders"] 
        if o["owner"] == interaction.user.id and o["status"] == "dang_cay"
    ]))
    
    return [
        app_commands.Choice(name=name, value=name)
        for name in user_usernames if current.lower() in name.lower()
    ][:25]


@bot.tree.command(name="suathongtin", description="Sửa tài khoản/mật khẩu đơn hàng")
async def suathongtin(interaction: discord.Interaction):
    # Lọc ra các đơn hàng của người dùng này mà chưa hoàn thành
    user_orders = [o for o in data["orders"] if o["owner"] == interaction.user.id and o["status"] != "da_xong"]
    
    if not user_orders: 
        return await interaction.response.send_message("❌ Bạn không có đơn hàng nào đang chờ để sửa!", ephemeral=True)
    
    view = discord.ui.View()
    opts = [discord.SelectOption(label=f"{o['don']} ({o['id']})", value=o['id']) for o in user_orders]
    sel = discord.ui.Select(placeholder="Chọn đơn cần sửa thông tin...", options=opts)
    
    async def cb(i: discord.Interaction):
        order = next(o for o in data["orders"] if o["id"] == sel.values[0])
        
        class EditModal(discord.ui.Modal, title="CẬP NHẬT THÔNG TIN"):
            u = discord.ui.TextInput(label="Tài khoản mới", default=order["username"], required=True)
            p = discord.ui.TextInput(label="Mật khẩu mới", default=order["password"], required=True)
            
            async def on_submit(self, i2: discord.Interaction):
                # Cập nhật vào dữ liệu
                old_user = order["username"]
                order["username"] = self.u.value
                order["password"] = self.p.value
                save_json(DATA_FILE, data)
                
                # --- PHẦN THÔNG BÁO RIÊNG CHO ADMIN ---
                thong_bao_admin = (
                    f"🔄 **KHÁCH VỪA SỬA THÔNG TIN ĐƠN!**\n"
                    f"📦 **Dịch vụ:** `{order['don']}`\n"
                    f"🆔 **Mã đơn:** `{order['id']}`\n"
                    f"👤 **Khách hàng:** {i2.user.mention}\n"
                    f"--------------------------\n"
                    f"🔐 **Tài khoản mới:** `{self.u.value}`\n"
                    f"🔑 **Mật khẩu mới:** `{self.p.value}`"
                )
                
                # Gửi cho tất cả admin trong danh sách
                for admin_id in admins_list:
                    try:
                        adm = await bot.fetch_user(admin_id)
                        await adm.send(thong_bao_admin)
                    except:
                        pass # Bỏ qua nếu admin chặn DM
                # ---------------------------------------

                await i2.response.send_message(f"✅ Đã cập nhật thông tin đơn `{order['id']}` và báo cho Admin!", ephemeral=True)
        
        await i.response.send_modal(EditModal())
        
    sel.callback = cb
    view.add_item(sel)
    await interaction.response.send_message("Chọn đơn hàng bạn muốn thay đổi thông tin:", view=view, ephemeral=True)




@bot.tree.command(name="doncay", description="[Admin] Xem và quản lý các đơn chưa nhận")
async def doncay(interaction: discord.Interaction):
    if not is_admin(interaction.user.id): 
        return await interaction.response.send_message("❌ Bạn không có quyền!", ephemeral=True)

    orders = [o for o in data["orders"] if o["status"] == "chua_nhan"]
    if not orders:
        return await interaction.response.send_message("📭 Hiện không có đơn hàng nào đang chờ.", ephemeral=True)

    # --- CLASS XỬ LÝ PHÂN TRANG CHO ĐƠN CÀY ---
    class DoncayPaginationView(discord.ui.View):
        def __init__(self, order_list, page=0):
            super().__init__(timeout=120)
            self.order_list = order_list
            self.page = page
            per_page = 25
            start, end = page * per_page, (page + 1) * per_page
            curr_orders = order_list[start:end]

            # Menu chọn đơn
            opts = [
                discord.SelectOption(
                    label=f"Đơn: {o['don']}", 
                    description=f"Khách: {o['username']} | ID: {o['id']}", 
                    value=o['id']
                ) for o in curr_orders
            ]
            self.select = discord.ui.Select(placeholder=f"🔍 Chọn đơn hàng (Trang {page+1})...", options=opts)
            self.select.callback = self.select_callback
            self.add_item(self.select)

            # Nút chuyển trang
            if page > 0:
                btn_p = discord.ui.Button(label="⬅️ Trước", style=discord.ButtonStyle.gray)
                btn_p.callback = self.prev; self.add_item(btn_p)
            if end < len(order_list):
                btn_n = discord.ui.Button(label="Sau ➡️", style=discord.ButtonStyle.gray)
                btn_n.callback = self.next; self.add_item(btn_n)

        async def select_callback(self, i_select: discord.Interaction):
            oid = self.select.values[0]
            o = next(x for x in data["orders"] if x["id"] == oid)

            embed = discord.Embed(title="⏳ ĐƠN HÀNG ĐANG CHỜ", color=0xf1c40f)
            embed.add_field(name="🆔 Mã đơn", value=f"`{o['id']}`", inline=True)
            embed.add_field(name="📦 Dịch vụ", value=f"**{o['don']}**", inline=True)
            embed.add_field(name="👤 Khách", value=f"<@{o['owner']}>", inline=False)
            
            view_action = discord.ui.View()
            
            # NÚT NHẬN ĐƠN (Thêm lưu admin_id)
            btn_nhan = discord.ui.Button(label="Nhận đơn", style=discord.ButtonStyle.success, emoji="✅")
            async def nhan_cb(i: discord.Interaction, order_info=o):
                order_info["status"] = "dang_cay"
                order_info["admin_id"] = i.user.id # LƯU ADMIN_ID
                save_json(DATA_FILE, data)
                await i.response.edit_message(content=f"✅ Bạn đã nhận đơn `{order_info['id']}`", embed=None, view=None)
                try:
                    user = await bot.fetch_user(order_info['owner'])
                    await user.send(f"✅ Đơn hàng `{order_info['don']}` (ID: {order_info['id']}) của bạn đã được Admin nhận!")
                except: pass

            # NÚT HỦY ĐƠN (Giữ nguyên code cũ)
            btn_huy = discord.ui.Button(label="Hủy đơn & Hoàn tiền", style=discord.ButtonStyle.danger, emoji="🗑️")
            async def huy_cb(i: discord.Interaction, order_info=o):
                uid = str(order_info['owner'])
                so_tien_hoan = order_info['money']
                if uid not in data["users"]: data["users"][uid] = {"balance": 0, "total_nap": 0}
                data["users"][uid]["balance"] += so_tien_hoan
                data["orders"] = [x for x in data["orders"] if x["id"] != order_info['id']]
                save_json(DATA_FILE, data)
                await i.response.edit_message(content=f"❌ Đã hủy đơn `{order_info['id']}`", embed=None, view=None)
                try:
                    user = await bot.fetch_user(order_info['owner'])
                    await user.send(f"🚫 Đơn hàng `{order_info['id']}` đã bị hủy. Hoàn tiền thành công.")
                except: pass

            btn_nhan.callback = nhan_cb; btn_huy.callback = huy_cb
            view_action.add_item(btn_nhan); view_action.add_item(btn_huy)
            await i_select.response.send_message(embed=embed, view=view_action, ephemeral=True)

        async def next(self, i2): await i2.response.edit_message(view=DoncayPaginationView(self.order_list, self.page+1))
        async def prev(self, i2): await i2.response.edit_message(view=DoncayPaginationView(self.order_list, self.page-1))

    await interaction.response.send_message(f"📦 Có {len(orders)} đơn chưa nhận:", view=DoncayPaginationView(orders), ephemeral=True)
@bot.tree.command(name="donnhan", description="[Admin] Quản lý đơn hàng (Chỉ xem đơn mình đã nhận)")
async def donnhan(interaction: discord.Interaction):
    if not is_admin(interaction.user.id): 
        return await interaction.response.send_message("❌ Bạn không có quyền!", ephemeral=True)

    uid = interaction.user.id
    is_owner = (uid == OWNER_ID) # Thay OWNER_ID bằng ID của bạn

    # 1. Lọc đơn: Nếu là Owner thì thấy hết, nếu là Admin thường chỉ thấy đơn mình nhận (admin_id)
    if is_owner:
        pending_orders = [o for o in data["orders"] if o["status"] == "dang_cay"]
    else:
        pending_orders = [o for o in data["orders"] if o["status"] == "dang_cay" and o.get("admin_id") == uid]

    if not pending_orders:
        return await interaction.response.send_message("📭 Hiện không có đơn nào bạn đang thực hiện.", ephemeral=True)

    # --- CLASS XỬ LÝ PHÂN TRANG & HIỂN THỊ ---
    class DonNhanPaginationView(discord.ui.View):
        def __init__(self, order_list, page=0):
            super().__init__(timeout=120)
            self.order_list = order_list
            self.page = page
            per_page = 25
            start, end = page * per_page, (page + 1) * per_page
            curr_orders = order_list[start:end]

            # 2. Tạo Select Menu chứa danh sách tài khoản
            opts = [
                discord.SelectOption(
                    label=f"Tài khoản: {o['username']}", 
                    description=f"Dịch vụ: {o['don']} | ID: {o['id']}", 
                    value=o['id']
                ) for o in curr_orders
            ]
            self.select = discord.ui.Select(placeholder=f"🔍 Chọn đơn cần xử lý (Trang {page+1})...", options=opts)
            self.select.callback = self.select_callback
            self.add_item(self.select)

            # Nút chuyển trang nếu > 25 đơn
            if page > 0:
                btn_p = discord.ui.Button(label="⬅️ Trang trước", style=discord.ButtonStyle.gray)
                btn_p.callback = self.prev; self.add_item(btn_p)
            if end < len(order_list):
                btn_n = discord.ui.Button(label="Trang sau ➡️", style=discord.ButtonStyle.gray)
                btn_n.callback = self.next; self.add_item(btn_n)

        async def select_callback(self, i: discord.Interaction):
            order_id = self.select.values[0]
            order_info = next(o for o in data["orders"] if o["id"] == order_id)
            
            embed = discord.Embed(title="🛠️ CHI TIẾT ĐƠN ĐANG XỬ LÝ", color=0x3498db)
            embed.add_field(name="🆔 Mã đơn", value=f"`{order_info['id']}`", inline=True)
            embed.add_field(name="📦 Dịch vụ", value=f"**{order_info['don']}**", inline=True)
            embed.add_field(name="👤 Khách", value=f"<@{order_info['owner']}>", inline=False)
            embed.add_field(name="🔐 Tài khoản", value=f"||`{order_info['username']}`||", inline=True)
            embed.add_field(name="🔑 Mật khẩu", value=f"||`{order_info['password']}`||", inline=True)
            if is_owner: # Hiện thêm thông tin ai đang cày cho Owner xem
                admin_cày = order_info.get("admin_id", "Không rõ")
                embed.set_footer(text=f"Admin đang nhận đơn này: {admin_cày}")

            action_view = discord.ui.View()

            # --- NÚT 1: LẤY MÃ LOGIN (GIỮ NGUYÊN) ---
            btn_code = discord.ui.Button(label="Lấy mã Login", style=discord.ButtonStyle.secondary, emoji="🔑")
            async def code_cb(i_btn: discord.Interaction):
                try:
                    user = await bot.fetch_user(order_info['owner'])
                    ten_acc = order_info['username']
                    emb_guide = discord.Embed(title="⚠️ YÊU CẦU MÃ XÁC MINH (2FA)", description=f"Admin đang chờ mã tài khoản: **{ten_acc}**", color=0xe67e22)
                    emb_guide.add_field(name="📝 Cách gửi", value=f"Dùng lệnh: `/malogin tai_khoan:{ten_acc} ma:______`", inline=False)
                    await user.send(embed=emb_guide)
                    await i_btn.response.send_message(f"✅ Đã gửi yêu cầu lấy mã cho khách `{ten_acc}`", ephemeral=True)
                except:
                    await i_btn.response.send_message("❌ Lỗi gửi tin nhắn cho khách!", ephemeral=True)
            btn_code.callback = code_cb

            # --- NÚT 2: BÁO LỖI TK/MK (GIỮ NGUYÊN) ---
            btn_error = discord.ui.Button(label="Báo lỗi TK/MK", style=discord.ButtonStyle.danger, emoji="⚠️")
            async def error_cb(i_btn: discord.Interaction):
                try:
                    user = await bot.fetch_user(order_info['owner'])
                    await user.send(f"⚠️ **Thông báo:** Admin báo tài khoản `{order_info['username']}` bị sai TK/MK. Vui lòng kiểm tra lại!")
                    await i_btn.response.send_message(f"✅ Đã báo khách sửa thông tin đơn `{order_id}`", ephemeral=True)
                except: pass
            btn_error.callback = error_cb

            # --- NÚT 3: HOÀN THÀNH (Lưu doanh thu) ---
            btn_done = discord.ui.Button(label="Hoàn thành", style=discord.ButtonStyle.success, emoji="🏆")
            async def done_cb(i_btn: discord.Interaction):
                order_info["status"] = "da_xong"
                # Doanh thu được tính tự động dựa trên status da_xong và admin_id đã lưu
                save_json(DATA_FILE, data)
                await i_btn.response.edit_message(content=f"🏆 Đã xong đơn `{order_id}`! Doanh thu đã được ghi nhận vào Panel.", embed=None, view=None)
                try:
                    user = await bot.fetch_user(order_info['owner'])
                    await user.send(f"🥳 Đơn hàng `{order_info['don']}` của bạn đã hoàn thành!")
                except: pass
            btn_done.callback = done_cb

            # --- NÚT 4: HỦY & HOÀN TIỀN (GIỮ NGUYÊN) ---
            btn_huy = discord.ui.Button(label="Hủy & Hoàn tiền", style=discord.ButtonStyle.danger, emoji="❌")
            async def huy_cb(i_btn: discord.Interaction):
                uid_khach = str(order_info['owner'])
                so_tien_hoan = order_info['money']
                if uid_khach not in data["users"]: data["users"][uid_khach] = {"balance": 0, "total_nap": 0}
                data["users"][uid_khach]["balance"] += so_tien_hoan
                data["orders"] = [x for x in data["orders"] if x["id"] != order_info['id']]
                save_json(DATA_FILE, data)
                await i_btn.response.edit_message(content=f"✅ Đã hủy và hoàn lại {format_money(so_tien_hoan)} cho khách.", embed=None, view=None)
            btn_huy.callback = huy_cb

            action_view.add_item(btn_code); action_view.add_item(btn_error)
            action_view.add_item(btn_done); action_view.add_item(btn_huy)
            await i.response.send_message(embed=embed, view=action_view, ephemeral=True)

        async def next(self, i2): await i2.response.edit_message(view=DonNhanPaginationView(self.order_list, self.page+1))
        async def prev(self, i2): await i2.response.edit_message(view=DonNhanPaginationView(self.order_list, self.page-1))

    await interaction.response.send_message("🔍 Chọn tài khoản game bạn đang xử lý:", view=DonNhanPaginationView(pending_orders), ephemeral=True)
@bot.tree.command(name="panel", description="[Admin] Bảng điều khiển quản lý đơn hàng toàn diện")
async def panel(interaction: discord.Interaction):
    if not is_admin(interaction.user.id):
        return await interaction.response.send_message("❌ Bạn không có quyền truy cập!", ephemeral=True)

    def create_panel_embed():
        # Phân loại đơn hàng
        da_cay = [o for o in data["orders"] if o["status"] == "da_xong"]
        da_nhan = [o for o in data["orders"] if o["status"] == "dang_cay"]
        chua_nhan = [o for o in data["orders"] if o["status"] == "chua_nhan"]

        # Tính toán tiền bạc
        tong_tien_da_cay = sum(o["money"] for o in da_cay)
        tong_tien_dang_cay = sum(o["money"] for o in da_nhan)
        tong_tien_chua_nhan = sum(o["money"] for o in chua_nhan)

        embed = discord.Embed(title="🖥️ HỆ THỐNG QUẢN LÝ CÀY THUÊ", color=0x3498db)
        embed.add_field(name="✅ Đã hoàn thành", value=f"**{len(da_cay)}** đơn\n💰 `{format_money(tong_tien_da_cay)}`", inline=True)
        embed.add_field(name="👷 Đang thực hiện", value=f"**{len(da_nhan)}** đơn\n💰 `{format_money(tong_tien_dang_cay)}`", inline=True)
        embed.add_field(name="⏳ Đang chờ duyệt", value=f"**{len(chua_nhan)}** đơn\n💰 `{format_money(tong_tien_chua_nhan)}`", inline=True)
        embed.set_footer(text="Chọn các nút bên dưới để quản lý chi tiết từng mục.")
        return embed

    class PanelView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        # --- 1. LỊCH SỬ ĐÃ CÀY (GIỮ NGUYÊN) ---
        @discord.ui.button(label="Lịch sử đơn", style=discord.ButtonStyle.success, emoji="📜")
        async def lich_su(self, i: discord.Interaction, button: discord.ui.Button):
            orders = [o for o in data["orders"] if o["status"] == "da_xong"]
            if not orders: return await i.response.send_message("Chưa có đơn nào hoàn thành!", ephemeral=True)
            
            view = discord.ui.View()
            for o in orders[:5]: 
                btn = discord.ui.Button(label=f"Xóa {o['id']}", style=discord.ButtonStyle.danger)
                async def xoa_callback(i2, oid=o['id']):
                    data["orders"] = [x for x in data["orders"] if x["id"] != oid]
                    save_json(DATA_FILE, data)
                    await i2.response.send_message(f"🗑️ Đã xóa lịch sử đơn `{oid}`", ephemeral=True)
                btn.callback = xoa_callback
                view.add_item(btn)
            
            emb = discord.Embed(title="📜 LỊCH SỬ ĐƠN HOÀN THÀNH", description="\n".join([f"ID: `{o['id']}` - {o['don']}" for o in orders]))
            await i.response.send_message(embed=emb, view=view, ephemeral=True)

        # --- 2. QUẢN LÝ ĐƠN ĐÃ NHẬN (GIỮ NGUYÊN) ---
        @discord.ui.button(label="Đơn đã nhận", style=discord.ButtonStyle.primary, emoji="👷")
        async def dang_cay(self, i: discord.Interaction, button: discord.ui.Button):
            orders = [o for o in data["orders"] if o["status"] == "dang_cay"]
            if not orders: return await i.response.send_message("Bạn chưa nhận đơn nào!", ephemeral=True)

            for o in orders:
                view = discord.ui.View()
                btn_code = discord.ui.Button(label="Lấy mã Login", style=discord.ButtonStyle.secondary)
                async def code_cb(i2, oid=o['id']):
                    await i2.response.send_message(f"🔔 Đang yêu cầu khách gửi mã cho đơn `{oid}`...", ephemeral=True)
                
                btn_done = discord.ui.Button(label="Hoàn thành", style=discord.ButtonStyle.success)
                async def done_cb(i2, order=o):
                    order["status"] = "da_xong"
                    save_json(DATA_FILE, data)
                    await i2.response.send_message(f"✅ Đã xong đơn `{order['id']}`!", ephemeral=True)
                
                btn_code.callback = code_cb
                btn_done.callback = done_cb
                view.add_item(btn_code); view.add_item(btn_done)
                await i.user.send(f"📦 Đơn: {o['don']} | ID: `{o['id']}`", view=view)
            await i.response.send_message("Đã gửi danh sách đơn vào DM của bạn để xử lý!", ephemeral=True)

        # --- 3. QUẢN LÝ ĐƠN CHƯA NHẬN (CẬP NHẬT LƯU ADMIN_ID) ---
        @discord.ui.button(label="Đơn chưa nhận", style=discord.ButtonStyle.secondary, emoji="⏳")
        async def chua_nhan(self, i: discord.Interaction, button: discord.ui.Button):
            orders = [o for o in data["orders"] if o["status"] == "chua_nhan"]
            if not orders: return await i.response.send_message("Không có đơn nào đang chờ!", ephemeral=True)

            for o in orders:
                view = discord.ui.View()
                btn_nhan = discord.ui.Button(label="Nhận đơn", style=discord.ButtonStyle.success)
                btn_huy = discord.ui.Button(label="Hủy đơn", style=discord.ButtonStyle.danger)
                
                async def nhan_cb(i2, order=o):
                    order["status"] = "dang_cay"
                    order["admin_id"] = i2.user.id
                    save_json(DATA_FILE, data)
                    await i2.response.send_message(f"✅ Bạn đã nhận đơn `{order['id']}`", ephemeral=True)
                
                async def huy_cb(i2, oid=o['id']):
                    data["orders"] = [x for x in data["orders"] if x["id"] != oid]
                    save_json(DATA_FILE, data)
                    await i2.response.send_message(f"❌ Đã hủy đơn `{oid}`", ephemeral=True)

                btn_nhan.callback = nhan_cb; btn_huy.callback = huy_cb
                view.add_item(btn_nhan); view.add_item(btn_huy)
                await i.user.send(f"⏳ Đơn chờ: {o['don']} | Giá: {format_money(o['money'])}", view=view)
            await i.response.send_message("Đã gửi danh sách chờ vào DM của bạn!", ephemeral=True)

        # --- 4. QUẢN LÝ TIỀN (GỘP PHÂN TRANG & THỐNG KÊ CHI TIẾT) ---
        @discord.ui.button(label="Quản lý tiền", style=discord.ButtonStyle.danger, emoji="💰")
        async def quan_ly_tien(self, i: discord.Interaction, button: discord.ui.Button):
            all_admins = list(set([o["admin_id"] for o in data["orders"] if "admin_id" in o and o["status"] == "da_xong"]))
            
            if not all_admins:
                return await i.response.send_message("Chưa có dữ liệu doanh thu hoàn thành!", ephemeral=True)

            def get_stats(target_id):
                if target_id == "all":
                    summary = ""
                    total_m = 0
                    total_c = 0
                    for aid in all_admins:
                        user_orders = [o for o in data["orders"] if o.get("admin_id") == aid and o["status"] == "da_xong"]
                        count = len(user_orders)
                        money = sum(o["money"] for o in user_orders)
                        summary += f"👤 <@{aid}>: **{count}** đơn - `{format_money(money)}`\n"
                        total_m += money
                        total_c += count
                    return total_c, total_m, "Báo cáo tất cả Admin", summary
                
                orders = [o for o in data["orders"] if o.get("admin_id") == target_id and o["status"] == "da_xong"]
                return len(orders), sum(o["money"] for o in orders), f"Admin: <@{target_id}>", None

            class AdminPaginationView(discord.ui.View):
                def __init__(self, admin_list, page=0):
                    super().__init__(timeout=60)
                    self.admin_list = admin_list
                    self.page = page
                    per_page = 23 
                    start, end = page * per_page, (page + 1) * per_page
                    curr_admins = admin_list[start:end]

                    opts = [discord.SelectOption(label="🌟 TỔNG TẤT CẢ ADMIN", value="all", description="Xem danh sách chi tiết doanh thu từng người")]
                    for aid in curr_admins:
                        count, money, _, _ = get_stats(aid)
                        opts.append(discord.SelectOption(
                            label=f"ID: {aid}", 
                            description=f"Xong: {count} đơn | Tiền: {format_money(money)}",
                            value=str(aid)
                        ))
                    
                    self.sel = discord.ui.Select(placeholder=f"Chọn Admin để xem (Trang {page+1})", options=opts)
                    self.sel.callback = self.sel_cb
                    self.add_item(self.sel)

                    if page > 0:
                        btn_p = discord.ui.Button(label="⬅️ Trước", style=discord.ButtonStyle.gray)
                        btn_p.callback = self.prev; self.add_item(btn_p)
                    if end < len(admin_list):
                        btn_n = discord.ui.Button(label="Sau ➡️", style=discord.ButtonStyle.gray)
                        btn_n.callback = self.next; self.add_item(btn_n)

                async def sel_cb(self, i2):
                    val = self.sel.values[0]
                    target = "all" if val == "all" else int(val)
                    count, money, title, detail_text = get_stats(target)
                    
                    emb = discord.Embed(title="📊 THỐNG KÊ DOANH THU", color=0xf1c40f)
                    emb.add_field(name="📋 Đối tượng", value=title, inline=False)
                    
                    if detail_text:
                        emb.add_field(name="👥 Chi tiết từng Admin", value=detail_text, inline=False)
                        emb.add_field(name="📈 Tổng đơn", value=f"**{count}** đơn", inline=True)
                        emb.add_field(name="💰 Tổng tiền", value=f"**{format_money(money)}**", inline=True)
                    else:
                        emb.add_field(name="✅ Đã hoàn thành", value=f"**{count}** đơn", inline=True)
                        emb.add_field(name="💰 Thu nhập", value=f"**{format_money(money)}**", inline=True)
                        
                    await i2.response.send_message(embed=emb, ephemeral=True)

                async def next(self, i2): await i2.response.edit_message(view=AdminPaginationView(self.admin_list, self.page+1))
                async def prev(self, i2): await i2.response.edit_message(view=AdminPaginationView(self.admin_list, self.page-1))

            await i.response.send_message("Vui lòng chọn Admin muốn xem thống kê:", view=AdminPaginationView(all_admins), ephemeral=True)

    await interaction.response.send_message(embed=create_panel_embed(), view=PanelView())
@bot.event
async def on_message(message):
    # Chỉ xử lý tin nhắn bắt đầu bằng NDK và không phải bot
    if message.author.bot or not message.content.startswith("NDK"):
        return

    user_key = message.content.strip()
    all_keys = load_json(KEYS_STORAGE_FILE, {"ActiveTasks": {}})
    active_tasks = all_keys.get("ActiveTasks", {})

    # 1. Kiểm tra mã Key tồn tại
    if user_key not in active_tasks:
        return

    # 2. LẤY IP TỪ WEB (Quan trọng nhất để chống clone)
    # Lưu ý: storage_ip phải khớp với tên biến ông dùng trong FastAPI (storage_web_status hoặc storage_ip)
    real_ip = storage_ip.get(user_key)
    if not real_ip:
        return await message.reply("❌ Web chưa gửi dữ liệu IP. Vui lòng vượt link đến trang cuối!")

    task_info = active_tasks[user_key]
    task_type = task_info["type"]
    reward = task_info["amount"]
    user_id = str(message.author.id)
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 3. KIỂM TRA GIỚI HẠN IP (CHỐNG CLONE)
    full_data = load_json(DATA_FILE, {"users": {}, "ip_limits": {}})
    ip_key = f"{real_ip}_{task_type}"
    ip_usage = full_data.get("ip_limits", {}).get(ip_key, {"count": 0, "date": today})
    
    max_limit = LINK_CONFIGS[task_type]["max"]
    if ip_usage["date"] == today and ip_usage["count"] >= max_limit:
        return await message.reply(f"❌ IP này đã đạt giới hạn nhận tiền cho {task_type} hôm nay.")

    # 4. CỘNG TIỀN VÀ CẬP NHẬT (Đồng bộ với lệnh /info)
    if user_id not in full_data["users"]:
        full_data["users"][user_id] = {"balance": 0, "total_nap": 0}

    # Cộng tiền vào ví
    full_data["users"][user_id]["balance"] += reward
    
    # Cập nhật lượt IP để không cho nick khác dùng chung mạng nhận thêm
    if "ip_limits" not in full_data: full_data["ip_limits"] = {}
    full_data["ip_limits"][ip_key] = {"count": ip_usage["count"] + 1, "date": today}

    # 5. LƯU VÀ DỌN DẸP
    save_json(DATA_FILE, full_data)
    del active_tasks[user_key]
    save_json(KEYS_STORAGE_FILE, all_keys)
    if user_key in storage_ip: del storage_ip[user_key]

    # Phản hồi ngắn gọn
    await message.reply(f"✅ Thành công! +**{reward:,} VNĐ**. Số dư: **{full_data['users'][user_id]['balance']:,} VNĐ**")

# --- KẾT THÚC PHẦN EVENT ---
async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
