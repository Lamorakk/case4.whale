from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
import constants as c


firstkeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="eng_change")]
    ]
)

ready_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ready ✅", callback_data="ready")]
    ]
)

tutorkeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔹How does it work?", url=c.TUTORIAL_gen)],
        [InlineKeyboardButton(text="🔹How to deposit and withdraw?", url=c.TUTORIAL_with)],
        [InlineKeyboardButton(text="🔹How to promote a link?", url=c.TUTORIAL_pr)],
        [InlineKeyboardButton(text="BACK ↩", callback_data= "go_back")],

    ]
)

tutorkeyboardred = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔹How does it work?", url=c.TUTORIAL_gen)],
        [InlineKeyboardButton(text="🔹How to deposit and withdraw?", url=c.TUTORIAL_with)],
        [InlineKeyboardButton(text="🔹How to promote a link?", url=c.TUTORIAL_pr)],
        [InlineKeyboardButton(text="BACK ↩", callback_data= "go_backbut")],

    ]
)

# RU Menu Keyboard
# kb_ru_menu = [
#     [
#         types.InlineKeyboardButton(text="Играть", callback_data="start_earning"),
#     ],
#     [
#         types.InlineKeyboardButton(text="⭐ Руководство", url=c.TUTORIAL),
#     ],
#     [
#         types.InlineKeyboardButton(text="📢 Канал новостей", url=c.NEWS_CHANNEL),
#     ],
#     [
#         types.InlineKeyboardButton(text="❓ Чат (Рус)", url=c.CHAT_ENG),
#     ],
# ]


kb_ru_menu = [
    [
        types.InlineKeyboardButton(text="🐳 PLAY ", callback_data="start_earning"),
    ],
    [
        types.InlineKeyboardButton(text="📘 HOW TO START", callback_data="tutor"),
    ],
    [
        types.InlineKeyboardButton(text="🌐 NEWS CHANNEL  ", url=c.NEWS_CHANNEL),
    ],
    [
        types.InlineKeyboardButton(text="💬 CHAT (ENG)  ", url=c.CHAT_ENG),
    ],
]

# ENG Menu Keyboard
kb_eng_menu = [
    [
        types.InlineKeyboardButton(text="🐳 PLAY ", callback_data="start_earning"),
    ],
    [
        types.InlineKeyboardButton(text="📘 HOW TO START", callback_data="tutor"),
    ],
    [
        types.InlineKeyboardButton(text="🌐 NEWS CHANNEL  ", url=c.NEWS_CHANNEL),
    ],
    [
        types.InlineKeyboardButton(text="💬 CHAT (ENG)  ", url=c.CHAT_ENG),
    ],
]


keyboard_ru_menu = types.InlineKeyboardMarkup(inline_keyboard=kb_ru_menu)
keyboard_eng_menu = types.InlineKeyboardMarkup(inline_keyboard=kb_eng_menu)

keyboards_menu = {
    c.ENG: keyboard_eng_menu,
    c.RU: keyboard_ru_menu
}

keyboard_ru_menu = types.InlineKeyboardMarkup(inline_keyboard=kb_ru_menu)
keyboard_eng_menu = types.InlineKeyboardMarkup(inline_keyboard=kb_eng_menu)

keyboards_menu = {
    c.ENG: keyboard_eng_menu,
    c.RU: keyboard_ru_menu
}

















#####################################################################################################
#Previous

# kb_ru_menu = [
#     [
#         types.InlineKeyboardButton(text="💸 Начать заработок", callback_data="start_earning"),
#     ],
#     [
#         types.InlineKeyboardButton(text="📢 Подписаться на канал", url=c.SUBSCRIBE_TO_RU_CHANNEL_URL),
#     ],
#     [
#         types.InlineKeyboardButton(text="⭐ Инвестировать с помощью stars [скоро]", callback_data="invest_stars"),
#     ],
#     [
#         types.InlineKeyboardButton(text="❓ Как зарабатывать с игры", callback_data="questions")
#     ],
#     [
#         types.InlineKeyboardButton(text="🌐 Изменить язык на ENG", callback_data="change_lang_en")
#     ]
# ]
#
# # ENG Menu Keyboard
# kb_eng_menu = [
#     [
#         types.InlineKeyboardButton(text="💸 Start earning", callback_data="start_earning"),
#     ],
#     [
#         types.InlineKeyboardButton(text="📢 Subscribe to channel", url=c.SUBSCRIBE_TO_ENG_CHANNEL_URL),
#     ],
#     [
#         types.InlineKeyboardButton(text="⭐ Invest via stars [soon]", callback_data="invest_stars"),
#     ],
#     [
#         types.InlineKeyboardButton(text="❓ How to earn", callback_data="questions"),
#     ],
#     [
#         types.InlineKeyboardButton(text="🌐 Language to RU", callback_data="change_lang_ru")
#     ]
# ]


##########################################################################################


# kb_run_inline_web = [
#     [types.InlineKeyboardButton(text="Войти на вебсайт", web_app=WebAppInfo(url="https://www.youtube.com"))],
# ]
# kb_eng_inline_web = [
#     [types.InlineKeyboardButton(text="Login website", web_app=WebAppInfo(url="https://www.youtube.com"))],
# ]
#
# keyboard_ru_web = types.InlineKeyboardMarkup(inline_keyboard=kb_run_inline_web)
# keyboard_eng_web = types.InlineKeyboardMarkup(inline_keyboard=kb_eng_inline_web)
#
# keyboards_web = {
#     c.ENG: keyboard_eng_web,
#     c.RU: keyboard_ru_web
# }


##########################################################################################


# RU Link to Channel Keyboard
kb_ru_link_to_channel = [
    [types.InlineKeyboardButton(text="📢 Подписка", url="https://t.me/pbl_channel")],
]
# ENG Link to Channel Keyboard
kb_eng_link_to_channel = [
    [types.InlineKeyboardButton(text="📢 Subscribe", url="https://t.me/pbl_channel")],
]
keyboard_ru_link = types.InlineKeyboardMarkup(inline_keyboard=kb_ru_link_to_channel)
keyboard_eng_link = types.InlineKeyboardMarkup(inline_keyboard=kb_eng_link_to_channel)

keyboards_link = {
    c.ENG: keyboard_eng_link,
    c.RU: keyboard_ru_link
}
