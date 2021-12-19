from google_trans_new import google_translator

list_of_languages = {"0": "ru",
                     "1": "en",
                     "2": "de",
                     "3": "ja",  # японский
                     "4": "fr",
                     "5": "cs",  # чешский
                     "6": "zh-cn"  # китайский
                      }
list_of_phrases = ["Извините, я не понял эту команду.", "Здравствуй, ", "Пожалуйста, выберете один из предложенных языков.", "Язык успешно сменён!", "Незнакомый пользователь", "Пожалуйста, выберете одно из предложенных времён, когда вам будет удобно получать рассылку с курсами валют.",
                   "Время определено.", "Я могу помочь вам следить за курсом доллара и евро в удобное для вас время.\n\nВы можете контролировать меня, отправляя эти команды:\n\n/dollar- узнать курс доллара\n/euro- узнать курс евро\n/language- сменить язык на удобный для вас\n"
                                        "/time- выбрать удобное для вас время, когда вам будет приходить рассылка с курсом валют\n/add_email- добавить email, для того чтобы получать рассылку не только в Telegram, но и на почту\n/delete_email- удалить вашу почту из моей базы данных",
                   "Почта уcпешно удалена!", "Напишите адрес своей почты.", "Почта некорректна.", "Почта введена корректно."]


class MyTranslator:
    translator = google_translator()

    def translate(self, number_of_phrase, number_of_language):
        try:
            return self.translator.translate(list_of_phrases[number_of_phrase], lang_tgt=list_of_languages[number_of_language])
        except Exception:
            return self.translator.translate(number_of_phrase, lang_tgt=list_of_languages[number_of_language])