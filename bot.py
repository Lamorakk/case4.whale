import asyncio
import contextlib
import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile
from aiogram.enums import ChatMemberStatus, ParseMode
from aiogram.filters import Command, CommandStart, CommandObject, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import decode_payload, create_start_link
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputFile, FSInputFile
import constants as c
import keyboard as k
from aiogram.types import ChatJoinRequest, Message, ChatMemberUpdated
from aiogram import Bot, Dispatcher, F, types

from request_data_server import post_new_user, get_user_data_by_tgid
from requests_main_server import get_login_token_for_game, post_user_to_main_server

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
# logging.basicConfig(
#     filename='debug.log',  # Set the desired log file name
#     level=logging.DEBUG,  # Capture debug messages
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Optional formatting
# )
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)
#
# handler = logging.FileHandler("app.log")
# handler.setLevel(logging.INFO)  # Capture INFO and higher levels
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler.setFormatter(formatter)
# logger = logging.getLogger("main.py")  # Use __name__ for current module name
# logger.addHandler(handler)  # Add the handler to the logger
# logger.setLevel(logging.DEBUG)  # Set logging level for the entire application

dp = Dispatcher()
bot = Bot(token=c.BOT_TOKEN)

DELIMITER = "?"


# class UserState(StatesGroup):
#     lang_code = State()

# Privacy policy message
# PRIVACY_POLICY_TEXTS = {
#     'ENG': (
#         "Privacy Policy 😊\n"
#         "Your Privacy Matters 💖\n\n"
#         "We take responsibility for protecting your privacy and ensuring the security of your personal data. "
#         "This Privacy Policy outlines how we collect, use, and safeguard your information when you use our website.\n"
#         "Data Collection 📊\n\n"
#         "We may collect personal data from you when you interact with our site, such as when you register for an account, "
#         "subscribe to our newsletter, fill out a form, or make a purchase. The types of information we collect include:\n\n"
#         "    Personal Identification Information: Name, email address, phone number, and postal address. 📇\n"
#         "    Technical Data: IP address, browser type and version, time zone setting, browser plug-in types and versions, "
#         "operating system, and platform. 🖥️\n"
#         "    Usage Data: Information about how you use our website, products, and services. 📈\n"
#         "    Marketing and Communications Data: Your preferences in receiving marketing from us and your communication preferences. 💌\n\n"
#         "Use of Data 🔧\n\n"
#         "The personal data we collect may be used for the following purposes:\n\n"
#         "    To provide and maintain our service ⚙️\n"
#         "    To notify you about changes to our service 🔔\n"
#         "    To allow you to participate in interactive features ✨"
#     ),
#     'RU': (
#         "Вы рискуете своими личными средствами !\n\n"
#         "🚨 Внимание: Продолжая инвестировать, вы рискуете потерять личные средства. 💸\n"
#         "Пожалуйста, убедитесь, что вы внимательно изучили все детали перед продолжением. 🤔\n"
#         "Инвестируйте разумно и будьте в курсе событий. 📈\n\n"
#         "Сбор данных 📊\n\n"
#         "Мы можем собирать персональные данные от вас при взаимодействии с нашим сайтом, такими как регистрация учетной записи, "
#         "подписка на нашу рассылку, заполнение формы или совершение покупки. Типы информации, которые мы собираем, включают:\n\n"
#         "    Персональная идентификационная информация: Имя, адрес электронной почты, номер телефона и почтовый адрес. 📇\n"
#         "    Технические данные: IP-адрес, тип и версия браузера, настройки часового пояса, типы и версии плагинов браузера, "
#         "операционная система и платформа. 🖥️\n"
#         "    Данные об использовании: Информация о том, как вы используете наш веб-сайт, продукты и услуги. 📈\n"
#         "    Данные о маркетинге и коммуникациях: Ваши предпочтения в получении маркетинговых материалов от нас и ваши предпочтения в общении. 💌\n\n"
#         "Использование данных 🔧\n\n"
#         "Персональные данные, которые мы собираем, могут использоваться для следующих целей:\n\n"
#         "    Для предоставления и поддержки наших услуг ⚙️\n"
#         "    Для уведомления вас о изменениях в наших услугах 🔔\n"
#         "    Для предоставления возможности участия в интерактивных функциях ✨"
#     )
# }
# ------------------------ COMMAND HANDLERS --------------------------------- #
@dp.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject, state: FSMContext):
    user_data = await state.get_data()
    args = check_if_any_payload(command)
    referral_login = args[0]
    response = get_user_data_by_tgid(args[0])
    if args is None:
        await message.answer("No payload found. Referral link is damaged or this referral is not registered")
    elif response is None:
        await message.answer("Referral data could not be retrieved. Referral link might be incorrect or the user is not registered.")
    elif response["login"] == referral_login:

        user_reg = {
            "login": str(message.from_user.id),
            "password": "random_password",
        }

        try:
            login_data = post_new_user(user_reg)
            login, password = login_data['login'], login_data['password']
            await message.answer("Choose language🌍", reply_markup=k.firstkeyboard)

            refdata = str(message.from_user.id) + DELIMITER + c.ENG
            reflink = await create_start_link(bot, refdata, encode=True)
            user_data = {
                "login": login,
                "password": password,
                "name": message.from_user.first_name,
                "username": message.from_user.username,
                "referralLogin": referral_login,
                "reflink": reflink
            }
            post_user_to_main_server(user_data)

        except Exception as e:
            logging.error(e)
            photo = FSInputFile('whale.jpg')  # Use FSInputFile to load the photo
            await bot.send_photo(message.chat.id, photo=photo, caption=c.CAPTION,
                                 reply_markup=k.keyboards_menu[c.ENG], parse_mode='HTML')
# @dp.callback_query(F.data == "eng_change")
# async def eng_change(callback: types.CallbackQuery, state: FSMContext):
#     user_id = callback.from_user.id
#     try:
#         await callback.message.edit_text(f"To get started, join our project channel and click the ready button.\n\n"
#                                          f"👉 [Click here to join]({c.CHANNEL_LINK})\n",
#                                          reply_markup=k.ready_keyboard, parse_mode="Markdown")
#     except Exception as e:
#         logging.error(e)
#         await callback.message.delete()
#         await callback.message.answer("To get started, join our project channel and click the ready button.\n\n"
#                                          "👉 [Click here to join](https://t.me/+2Lg1H7U5iMQ1NTlk)\n",
#                                          reply_markup=k.ready_keyboard, parse_mode="Markdown")


async def check_channel_membership(bot: Bot, user_id: int, channel_id: int) -> bool:
    member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    return member.status in ['member', 'administrator', 'creator']


# async def check_chat_membership(bot: Bot, user_id: int, chat_id: int) -> bool:
#     member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
#     return member.status in ['member', 'administrator', 'creator']


@dp.callback_query(F.data == "eng_change")
async def eng_change(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    try:
        await callback.message.edit_text(
            "To get started, join our project channel and chat, then click the ready button.\n\n"
            f"👉 [Join the channel]({c.CHANNEL_test_LINK})\n",
            reply_markup=k.ready_keyboard,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    except Exception as e:
        logging.error(e)
        await callback.message.delete()
        await callback.message.answer(
            "To get started, join our project channel and chat, then click the ready button.\n\n"
            f"👉 [Join the channel]({c.CHANNEL_test_LINK})\n",
            reply_markup=k.ready_keyboard,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )


@dp.callback_query(F.data == "ready")
async def check_sub(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id

    is_channel_member = await check_channel_membership(bot, user_id, c.CHANNEL_test_ID)
    # is_chat_member = await check_chat_membership(bot, user_id, c.chat_id)
    if is_channel_member:
        await callback.answer("🎉 You are a member! Welcome! 🎉", show_alert=True)
        photo = FSInputFile('whale.jpg')
        await bot.send_photo(callback.message.chat.id, photo=photo, caption=c.CAPTION,
                             reply_markup=k.keyboards_menu[c.ENG], parse_mode='HTML')
        await callback.message.delete()
    else:
        await callback.answer("❌ You need to join the channel to proceed.", show_alert=True)


async def check_subscription2(user: types.User):
    user_id = user.id
    res = await bot.get_chat_member(c.CHANNEL_ID, user_id)
    if res.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return True
    return False






# @dp.message(CommandStart(deep_link=True))
# async def handler(message: Message, command: CommandObject, state: FSMContext):
#     args = check_if_any_payload(command)
#     referral_login = args[0]
#
#     response = get_user_data_by_tgid(args[0])
#     if args is None:
#         await message.answer("No payload found. Referral link is damaged or this referral is not registered")
#     elif response["login"] == referral_login:
#
#         user_reg = {
#             "login": str(message.from_user.id),
#             "password": "random_password",
#         }
#
#         try:
#             login_data = post_new_user(user_reg)
#             login, password = login_data['login'], login_data['password']
#
#             refdata = message.text.split(" ")[1] + DELIMITER + c.ENG
#             reflink = await create_start_link(bot, refdata, encode=True)
#             user_data = {
#                 "login": login,
#                 "password": password,
#                 "name": message.from_user.first_name,
#                 "username": message.from_user.username,
#                 "referralLogin": referral_login,
#                 "reflink": reflink
#             }
#             post_user_to_main_server(user_data)
#             await message.answer(f"Welcome! Your login: {login}, Password: {password}",
#                                  reply_markup=k.keyboards_menu[c.ENG])
#            except Exception as e:
#             logging.error(e)
#             await message.answer("An error occurred during registration. Maybe you have already registered")


# @dp.message(CommandStart(deep_link=True))
# async def handler(message: Message, command: CommandObject, state: FSMContext):
#     # await state.set_state(UserState.lang_code)
#     args = check_if_any_payload(command)
#     if args is not None:
#         referral_id, lang = args
#         await state.update_data(content=lang)
#         await message.answer(f"🌟 Hello! Your referral ID: {referral_id} and Language: {lang}", reply_markup=k.keyboards_menu[lang])
#
#     else:
#         await message.answer("❗️ There seems to be an issue with your referral ID. Please contact your referral issuer or our support team. 🛠")


@dp.message(Command("start"))
async def handler(message: Message):
    await message.answer(c.WITHOUT_REFERRAL)


# ------------------------ CHECKING IF ANY PAYLOAD --------------------------------- #


def check_if_any_payload(command: CommandObject):
    args = command.args
    if args is not None:
        args_decoded = decode_payload(args).split(DELIMITER)
        if len(args_decoded) >= 2:
            return args_decoded[0], args_decoded[1]
    return None, None


@dp.message(Command("referral"))
async def handler(message: Message):
    ref = str(message.from_user.id) + DELIMITER + c.ENG
    link = await create_start_link(bot, ref, encode=True)
    # result: 'https://t.me/MyBot?start=Zm9v'
    # args = message.get_args()
    # print(args)
    # payload = decode_payload(args)
    await message.answer(f"🚀 Click the link below to start your journey! {link}")


@dp.message(Command("r"))
async def handler(message: Message):
    ref = message.text.split(" ")[1] + DELIMITER + c.ENG
    link = await create_start_link(bot, ref, encode=True)
    # result: 'https://t.me/MyBot?start=Zm9v'
    # args = message.get_args()
    # print(args)
    # payload = decode_payload(args)
    await message.answer(f"🚀 Click the link below to start your journey! {link}")


# ------------------------ INLINE BUTTONS HANDLERS --------------------------------- #


@dp.callback_query(F.data.startswith("change_lang"))
async def changeLanguage(callback: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    toggled_lang = toggle_lang(lang)

    await state.update_data(content=toggled_lang)
    await try_editing(callback.message, msg_text=c.CONTENT[toggled_lang]["WELCOME_WITH_REFERRAL"],
                      msg_keyboard=k.keyboards_menu[toggled_lang])



# Constants for button text and callback data
ACCEPT_PRIVACY_POLICY = "accept_privacy_policy"
DECLINE_PRIVACY_POLICY = "decline_privacy_policy"

# Inline keyboard with Accept and Decline buttons
privacy_policy_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Accept", callback_data=ACCEPT_PRIVACY_POLICY),
        InlineKeyboardButton(text="Decline", callback_data=DECLINE_PRIVACY_POLICY)
    ]
])

@dp.callback_query(F.data == "confirm_terms")
async def confirm_terms(callback: CallbackQuery, state: FSMContext):
    await state.update_data(terms_confirmed=True)
    await open_web_app(callback, state)

async def send_terms_and_conditions(callback: CallbackQuery):
    terms_message = (
        "Before starting, you confirm that you have read our terms and conditions. "
        f'<a href="https://telegra.ph/WhaleRace--Terms-and-Conditions-07-09">You can find it here</a>.'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Confirm ✅", callback_data="confirm_terms")]
        ]
    )
    try:
        await callback.message.edit_text(terms_message, reply_markup=keyboard, parse_mode="HTML",
                                         disable_web_page_preview=True)
    except Exception as e:
        logging.error(e)
        await callback.message.delete()
        await callback.message.answer(terms_message, reply_markup=keyboard, parse_mode="HTML",
                                         disable_web_page_preview=True)


@dp.callback_query(F.data == "start_earning")
async def start_earning(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    if user_data.get("terms_confirmed"):
        await open_web_app(callback, state)
    else:
        await send_terms_and_conditions(callback)


async def open_web_app(callback: types.CallbackQuery, state: FSMContext):
    photo = FSInputFile('whale.jpg')  # Use FSInputFile instead of InputFile
    try:
        # Retrieve the language
        lang = await get_lang(state)
        if lang not in c.CONTENT:
            raise ValueError(f"Language '{lang}' not found in CONTENT")

        # Retrieve user data
        login_data = get_user_data_by_tgid(callback.from_user.id)
        if login_data is None:
            await callback.answer("User data could not be retrieved. Please try again later.", show_alert=True)
            return

        login, password = login_data['login'], login_data['password']

        localization = 'default'
        if lang == 'ENG':
            localization = 'en'
        elif lang == 'RU':
            localization = 'ru'

        web_app_url = f"{c.URL_TO_WEBSITE}?data={login}&pmain={password}&lang={localization}"
        web_app_info = WebAppInfo(url=web_app_url)

        builder = InlineKeyboardBuilder()
        builder.button(text="🐳 PLAY", web_app=web_app_info)
        builder.button(text="📘 HOW TO START", callback_data="tutorf")
        builder.button(text="🌐 NEWS CHANNEL", url=c.NEWS_CHANNEL)
        builder.button(text="💬 CHAT (ENG)", url=c.CHAT_ENG)
        builder.adjust(1)
        new_markup = builder.as_markup()

        await callback.message.delete()
        # await callback.message.edit_text("Welcome!", reply_markup=new_markup)
        await bot.send_photo(callback.message.chat.id, photo=photo, caption=c.CAPTION,
                             reply_markup=new_markup, parse_mode='HTML')

    except Exception as e:
        logging.error(f"Error in open_web_app: {e}")
        await callback.answer("Some unexpected error occurred", show_alert=True)

# @dp.callback_query(F.data == "tutor")
# async def tutor(callback: CallbackQuery, state: FSMContext):
#     user_data = await state.get_data()
#     try:
#         await callback.message.edit_text("After reading the articles you will understand how the game works, how to make a "
#                                       "deposit, how to withdraw profits and how to make more profit than others!",
#                                       reply_markup=k.tutorkeyboard)
#     except Exception as e:
#         logging.error(e)
#         await callback.message.delete()
#         await callback.message.answer("After reading the articles you will understand how the game works, how to make a "
#                                       "deposit, how to withdraw profits and how to make more profit than others!",
#                                       reply_markup=k.tutorkeyboard)


@dp.callback_query(F.data == "tutor")
async def tutor(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    source_chat_id = -1002158523451
    message_id = 2
    caption_text = ("Watch the video to understand how our game works 🐳\n\n"
                    "To read the article, choose:")

    try:
        # Attempt to delete the original callback message
        await callback.message.delete()
    except TelegramBadRequest as e:
        logging.error(f"Failed to delete message: {e}")

    try:
        # Forward the video message from the source chat to get its message ID
        forwarded_message = await callback.message.bot.forward_message(
            chat_id=callback.message.chat.id,
            from_chat_id=source_chat_id,
            message_id=message_id
        )

        # Extract file ID from the forwarded message
        file_id_video = forwarded_message.video.file_id if forwarded_message.video else None

        if not file_id_video:
            logging.error("Error: Video file ID is missing")
            await callback.message.answer("Unable to retrieve the video. Please try again later.")
            return

        # Delete the forwarded message to remove "forwarded from" note
        await callback.message.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=forwarded_message.message_id
        )

        # Send the video using its file ID
        await callback.message.bot.send_video(
            chat_id=callback.message.chat.id,
            video=file_id_video,
            caption=caption_text,
            parse_mode=ParseMode.HTML,
            reply_markup=k.tutorkeyboard
        )

    except TelegramBadRequest as e:
        logging.error(f"Failed to handle video: {e}")
        await callback.message.answer("Unable to process the video. Please check the source chat and message ID.")

@dp.callback_query(F.data == "tutorf")
async def tutorf(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    source_chat_id = -1002158523451
    message_id = 2
    caption_text = ("Watch the video to understand how our game works 🐳\n\n"
                    "To read the article, choose:")

    try:
        # Attempt to delete the original callback message
        await callback.message.delete()
    except TelegramBadRequest as e:
        logging.error(f"Failed to delete message: {e}")

    try:
        # Forward the video message from the source chat to get its message ID
        forwarded_message = await callback.message.bot.forward_message(
            chat_id=callback.message.chat.id,
            from_chat_id=source_chat_id,
            message_id=message_id
        )

        # Extract file ID from the forwarded message
        file_id_video = forwarded_message.video.file_id if forwarded_message.video else None

        if not file_id_video:
            logging.error("Error: Video file ID is missing")
            await callback.message.answer("Unable to retrieve the video. Please try again later.")
            return

        # Delete the forwarded message to remove "forwarded from" note
        await callback.message.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=forwarded_message.message_id
        )

        # Send the video using its file ID
        await callback.message.bot.send_video(
            chat_id=callback.message.chat.id,
            video=file_id_video,
            caption=caption_text,
            parse_mode=ParseMode.HTML,
            reply_markup=k.tutorkeyboardred
        )

    except TelegramBadRequest as e:
        logging.error(f"Failed to handle video: {e}")
        await callback.message.answer("Unable to process the video. Please check the source chat and message ID.")
@dp.callback_query(F.data == "go_back")
async def go_back(callback: types.CallbackQuery, state: FSMContext):
    photo = FSInputFile('whale.jpg')  # Use FSInputFile instead of InputFile
    await callback.message.delete()
    await bot.send_photo(callback.message.chat.id, photo=photo, caption=c.CAPTION,
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=k.kb_eng_menu), parse_mode='HTML')

@dp.callback_query(F.data == "go_backbut")
async def go_back(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    if lang not in c.CONTENT:
        raise ValueError(f"Language '{lang}' not found in CONTENT")

    # Retrieve user data
    login_data = get_user_data_by_tgid(callback.from_user.id)
    if login_data is None:
        await callback.answer("User data could not be retrieved. Please try again later.", show_alert=True)
        return

    login, password = login_data['login'], login_data['password']

    localization = 'default'
    if lang == 'ENG':
        localization = 'en'
    elif lang == 'RU':
        localization = 'ru'

    web_app_url = f"{c.URL_TO_WEBSITE}?data={login}&pmain={password}&lang={localization}"
    web_app_info = WebAppInfo(url=web_app_url)

    builder = InlineKeyboardBuilder()
    builder.button(text="🐳 PLAY", web_app=web_app_info)
    builder.button(text="📘 HOW TO START", callback_data="tutorf")
    builder.button(text="🌐 NEWS CHANNEL", url=c.NEWS_CHANNEL)
    builder.button(text="💬 CHAT (ENG)", url=c.CHAT_ENG)
    builder.adjust(1)
    new_markup = builder.as_markup()
    photo = FSInputFile('whale.jpg')  # Use FSInputFile instead of InputFile
    await callback.message.delete()
    await bot.send_photo(callback.message.chat.id, photo=photo, caption=c.CAPTION,
                         reply_markup=new_markup, parse_mode='HTML')
@dp.callback_query(F.data == DECLINE_PRIVACY_POLICY)
async def decline_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        await callback.answer(
            text="We are sorry, but we cannot proceed without accepting the privacy policy. 😞",
            show_alert=True
        )
    except Exception as e:
        await callback.answer(text="Some unexpected error occurred", show_alert=True)

# @dp.callback_query(F.data.startswith("start_earning"))
# async def start_earning(callback: types.CallbackQuery, state: FSMContext):
#     try:
#         lang = await get_lang(state)
#         is_subscribed = await check_subscription(callback.from_user)
#         if is_subscribed:
#             login_data = get_user_data_by_tgid(callback.from_user.id)
#             login, password = login_data['login'], login_data['password']
#
#             localization = "default"
#             if lang == c.ENG:
#                 localization = 'en'
#             if lang == c.RU:
#                 localization = 'ru'
#
#             await bot.set_chat_menu_button(chat_id=callback.from_user.id, menu_button=None)
#             web_app = WebAppInfo(url=c.URL_TO_WEBSITE + f"?data={login}&pmain={password}&lang={localization}")
#             menu_button = types.MenuButtonWebApp(text="Web", web_app=web_app)
#             await bot.set_chat_menu_button(chat_id=callback.from_user.id, menu_button=menu_button)
#
#             # await try_editing(callback.message, msg_text=c.CONTENT[lang]["LETTING_TO_GAME"])
#             await callback.answer(
#                 text=c.CONTENT[lang]["LETTING_TO_GAME"],
#                 show_alert=True
#             )
#             # await callback.answer(c.CONTENT[lang]["LETTING_TO_GAME"], show_alert=True)
#         else:
#             await try_editing(callback.message, msg_text=c.CONTENT[lang]["NOT_LETTING_TO_GAME"])
#             await callback.answer(
#                 text=c.CONTENT[lang]["NOT_LETTING_TO_GAME"],
#                 show_alert=True
#             )
#             # await callback.answer(c.CONTENT[lang]["NOT_LETTING_TO_GAME"])
#             # await bot.pin_chat_message(callback.from_user.id, sent_message.message_id)
#     except Exception:
#         await callback.answer(text="Some unexpected error occured", show_alert=True)


@dp.callback_query(F.data.startswith("questions"))
async def start_earning(callback: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    await try_editing(callback.message, msg_text=c.CONTENT[lang]["MSG_HOW_TO_EARN"])
    # await try_editing(callback.message, c.CONTENT[lang]["LETTING_TO_GAME"])


# ------------------------ DISPATCHER EVENT HANDLERS --------------------------------- #


async def on_user_leave_eng(event: ChatMemberUpdated):
    await on_user_leave(event, c.ENG)


async def on_user_leave_ru(event: ChatMemberUpdated):
    await on_user_leave(event, c.RU)


async def on_user_leave(event: ChatMemberUpdated, lang):
    sub_status = await check_subscription(event.from_user)
    if not sub_status:
        await bot.send_message(chat_id=event.from_user.id, text=c.CONTENT[lang]["LEFT_CHANNEL"])
        await bot.set_chat_menu_button(chat_id=event.from_user.id, menu_button=None)


async def on_user_join_eng(chat_request: ChatJoinRequest):
    await on_user_join(chat_request, c.ENG)


async def on_user_join_ru(chat_request: ChatJoinRequest):
    await on_user_join(chat_request, c.RU)


async def on_user_join(chat_request: ChatJoinRequest, lang):
    await chat_request.approve()
    print(chat_request, lang)


# ------------------------ UTIL FUNCTIONS --------------------------------- #

async def try_editing(message: types.Message, msg_text=None, msg_keyboard=None):
    if msg_text is None:
        msg_text = message.text
    if msg_keyboard is None:
        msg_keyboard = message.reply_markup
    try:
        if msg_text != message.text or msg_keyboard != message.reply_markup:
            await message.edit_text(text=msg_text, reply_markup=msg_keyboard)
    except Exception as e:
        logging.error(f"Failed to edit message: {e}")
        new_message = await message.answer(text=msg_text, reply_markup=msg_keyboard)
        try:
            await message.delete()
        except Exception as delete_error:
            logging.error(f"Failed to delete the original message: {delete_error}")
        return new_message

async def check_subscription(user: types.User):
    res = await bot.get_chat_member(c.SUBSCRIBE_TO_ENG_CHANNEL_ID, user.id)
    if res.status == ChatMemberStatus.MEMBER or res.status == ChatMemberStatus.ADMINISTRATOR or res.status == ChatMemberStatus.CREATOR:
        return True

    res = await bot.get_chat_member(c.SUBSCRIBE_TO_RU_CHANNEL_ID, user.id)
    if res.status == ChatMemberStatus.MEMBER or res.status == ChatMemberStatus.ADMINISTRATOR or res.status == ChatMemberStatus.CREATOR:
        return True
    else:
        return False


def toggle_lang(lang):
    if lang == c.RU:
        return c.ENG
    if lang == c.ENG:
        return c.RU


# async def get_lang(state: FSMContext):
#     data = await state.get_data()
#
#     if data == {}:
#         # await state.set_state(UserState.lang_code)
#         await state.update_data(content=c.ENG)
#
#     data = await state.get_data()
#     return data["content"]
async def get_lang(state: FSMContext):
    data = await state.get_data()
    if 'content' not in data:
        await state.update_data(content='ENG')  # Default to 'ENG' if not set

    data = await state.get_data()
    logging.info(f"State data: {data}")
    return data.get('content', 'ENG')
# ------------------------ MAIN FUNCTIONS --------------------------------- #


# async def exec_main():
#     # try:
#     dp.chat_join_request.register(on_user_join_ru, F.chat.id == c.SUBSCRIBE_TO_RU_CHANNEL_ID)
#     dp.chat_join_request.register(on_user_join_eng, F.chat.id == c.SUBSCRIBE_TO_ENG_CHANNEL_ID)
#
#     dp.chat_member.register(on_user_leave_eng, F.chat.id == c.SUBSCRIBE_TO_ENG_CHANNEL_ID,
#                             ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
#     dp.chat_member.register(on_user_leave_ru, F.chat.id == c.SUBSCRIBE_TO_ENG_CHANNEL_ID,
#                             ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
#     await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
# except Exception as ex:
#     logger.error(f'[Exception] - {ex}', exc_info=True)
# finally:
#     await bot.session.close()

# if __name__ == '__main__':
# with open(c.USERS_FILENAME, "wb") as f:
#     pickle.dump([], f)
# with contextlib.suppress(KeyboardInterrupt, SystemExit):
# asyncio.run(exec_main())
async def exec_main():
    dp.chat_join_request.register(on_user_join_ru, F.chat.id == c.SUBSCRIBE_TO_RU_CHANNEL_ID)
    dp.chat_join_request.register(on_user_join_eng, F.chat.id == c.SUBSCRIBE_TO_ENG_CHANNEL_ID)
    dp.chat_member.register(on_user_leave_eng, F.chat.id == c.SUBSCRIBE_TO_ENG_CHANNEL_ID,
                            ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
    dp.chat_member.register(on_user_leave_ru, F.chat.id == c.SUBSCRIBE_TO_ENG_CHANNEL_ID,
                            ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(exec_main())
