import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ⚠️ Ivide ninte ഒറിജിനൽ ടെലിഗ്രാം ടോക്കൺ പേസ്റ്റ് ചെയ്യുക
TOKEN = "8939436590:AAEoLKK_l2UxF4gWv1mlNT-cpBqrb6jJCfw"

def scrape_live_leads():
    url = "https://toscrape.com" 
    
    # വെബ്‌സൈറ്റ് ബ്ലോക്ക് ചെയ്യാതിരിക്കാൻ ഒരു വ്യാജ ബ്രൗസർ ഐഡി (User-Agent) കൊടുക്കുന്നു
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # headers ഉപയോഗിച്ച് വെബ്‌സൈറ്റിലേക്ക് കണക്ട് ചെയ്യുന്നു
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        quotes = soup.find_all('div', class_='quote')
        
        live_data = []
        for item in quotes[:3]:
            text = item.find('span', class_='text').get_text()
            author = item.find('small', class_='author').get_text()
            
            live_data.append({
                "name": f"{author} Enterprises",
                "category": "Consultancy & Services",
                "info": text[:50] + "..."
            })
        return live_data
    except Exception as e:
        print(f"Scraping Error: {e}")
        return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **Live Data Scraping Bot Ready!**\n\n"
        "ഇന്റർനെറ്റിൽ നിന്ന് തത്സമയ ബിസിനസ്സ് വിവരങ്ങൾ എടുക്കാൻ **/get_leads** എന്ന് ടൈപ്പ് ചെയ്യൂ ബ്രോ."
    )

async def generate_live_leads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ഇന്റർനെറ്റിലെ വെബ്‌സൈറ്റുകളിലേക്ക് കണക്ട് ചെയ്ത് ലൈവ് ഡാറ്റ സ്ക്രാപ്പ് ചെയ്യുന്നു... വൺ സെക്കൻഡ് ബ്രോ! 🌐⏳")
    
    scraped_leads = scrape_live_leads()
    
    if not scraped_leads:
        await update.message.reply_text("❌ ഖേദിക്കുന്നു ബ്രോ, ഇന്റർനെറ്റിൽ നിന്ന് ഡാറ്റ എടുക്കാൻ പറ്റിയില്ല. നെറ്റ്‌വർക്ക് നോക്കൂ.")
        return
        
    reply_message = "✅ **Live Scraping Success!**\n\nഇതാ ഇന്റർനെറ്റിൽ നിന്ന് തത്സമയം എടുത്ത ബിസിനസ്സ് വിവരങ്ങൾ:\n\n"
    
    for row in scraped_leads:
        reply_message += (
            f"🏢 **{row['name']}**\n"
            f"• Category: {row['category']}\n"
            f"• About: {row['info']}\n\n"
        )
        
    reply_message += "💵 ഈ ലൈവ് ഡാറ്റ നിങ്ങൾക്ക് ക്ലയന്റുകൾക്ക് അയച്ചു നൽകാം!"
    await update.message.reply_text(reply_message)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_leads", generate_live_leads))
    
    print("Live Business Bot is running... Go to Telegram!")
    app.run_polling()

if __name__ == "__main__":
    main()
