import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import google.generativeai as genai

BOT_TOKEN = "BU_YERGA_BOTFATHER_TOKENINI_QO'YING"
GEMINI_API_KEY = "BU_YERGA_GEMINI_KALITINI_QO'YING"
ADMIN_ID = 123456789  # O'z Telegram ID raqamingiz

SIZNING_USLUBINGIZ = """
Sen Parizodaning shaxsiy yordamchisisan. 
Vazifang — Telegramda yozgan odamlarga o'zbek tilida muloqot qilish. 
Mijoz qanday uslubda yozsa, sen ham uning gapiga va ohangiga mos ravishda erkin va tabiiy javob qaytar. 

JUDA MUHIM QOIDA (TO'LOV VA PUL MASALASI):
Agar kimdir to'lov qilmoqchiligini, pul o'tkazganini, chek tashlaganini yoki rekvizit so'rasa:
1. Unga qat'iy qilib ayt: "Parizoda o'zi tez orada sizga javob beradi va ma'lumot beradi."
2. Boshqa ortiqcha gap yozma.
"""

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", system_instruction=SIZNING_USLUBINGIZ
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.business_message()
async def handle_business_message(message: Message):
  if (
      message.from_user
      and message.chat
      and message.from_user.id == message.chat.id
  ):
    if message.text:
      user_text = message.text
      user_name = (
          message.from_user.full_name
          or message.from_user.username
          or "Foydalanuvchi"
      )

      try:
        response = model.generate_content(user_text)
        reply_text = response.text

        tolev_sozlari = [
            "tolov",
            "to'lov",
            "pul",
            "karta",
            "click",
            "payme",
            "otkazdim",
            "o'tkazdim",
            "skrin",
            "chek",
            "sotib",
            "zakaz",
        ]
        if any(soz in user_text.lower() for soz in tolev_sozlari):
          await bot.send_message(
              chat_id=ADMIN_ID,
              text=(
                  f"🚨 **DIQQAT TO'LOV / ZAKAZ!**\n\n👤 Kimdan:"
                  f" {user_name}\n💬 Xabar: {user_text}"
              ),
          )

        await bot.send_message(
            chat_id=message.chat.id,
            text=reply_text,
            business_connection_id=message.business_connection_id,
        )

      except Exception as e:
        print(f"Xatolik: {e}")


@dp.message()
async def handle_direct_message(message: Message):
  if message.text:
    user_text = message.text
    user_name = (
        message.from_user.full_name or message.from_user.username or "Foydalanuvchi"
    )

    try:
      response = model.generate_content(user_text)
      reply_text = response.text

      tolev_sozlari = [
          "tolov",
          "to'lov",
          "pul",
          "karta",
          "click",
          "payme",
          "otkazdim",
          "o'tkazdim",
          "skrin",
          "chek",
          "sotib",
          "zakaz",
      ]
      if any(soz in user_text.lower() for soz in tolev_sozlari):
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🚨 **DIQQAT TO'LOV / ZAKAZ!**\n\n👤 Kimdan:"
                f" {user_name}\n💬 Xabar: {user_text}"
            ),
        )

      await message.reply(reply_text)
    except Exception as e:
      print(f"Xatolik: {e}")


async def main():
  print("Yordamchingiz to'liq ishga tushdi! ✨")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
