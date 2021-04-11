from aiogram.utils.callback_data import CallbackData

withdraw_callback = CallbackData("withdraw_callback", "choice")
info_callback = CallbackData("info_callback", "choice")
back_callback = CallbackData("back_callback", "from_where")

balance_callback = CallbackData("balance", "event")
payment_method_callback = CallbackData("payment", "method")
accept_phone_callback = CallbackData("accept_phone", "choice")
accept_card_callback = CallbackData("accept_card", "choice")
cancel_callback = CallbackData("cancel", "withdraw_method")


admin_callback = CallbackData("admin", "command")
cancel_admin_callback = CallbackData("cancel", "choice")