import os, requests, pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

def get_price(symbol="PAXGUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=100"
        r = requests.get(url, timeout=10).json()
        df = pd.DataFrame(r, columns=["ot","o","h","l","c","v","ct","qv","n","tb","tq","i"])
        for col in ["o","h","l","c"]: df[col]=df[col].astype(float)
        return df
    except: return None

def analyze(df):
    if df is None: return "فشل جلب البيانات"
    last=df.iloc[-1]; prev=df.iloc[-2]
    body=abs(last["c"]-last["o"])
    up=last["h"]-max(last["c"],last["o"])
    low=min(last["c"],last["o"])-last["l"]
    msg=[]
    if low>body*2: msg.append("🔨 مطرقة (شراء قوي)")
    if up>body*2: msg.append("⭐ شهاب (بيع)")
    if body<(last["h"]-last["l"])*0.1: msg.append("➕ دوجي - تردد")
    if not msg: msg.append("شمعة استمرارية")
    return "\n".join(msg) + f"\n\nالسعر: {last['c']:.2f}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا ياسين سالم 🥇\n/gold تحليل الذهب\n/btc البيتكوين\nالذهب شغال 100%")

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df=get_price("PAXGUSDT")
    await update.message.reply_text(f"🥇 تحليل الذهب 15د:\n{analyze(df)}")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df=get_price("BTCUSDT")
    await update.message.reply_text(f"₿ بيتكوين:\n{analyze(df)}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gold", gold))
app.add_handler(CommandHandler("btc", btc))
app.run_polling()
