from datetime import date

import iuliia

def transliterate(s:str):
    return iuliia.translate(s, iuliia.YANDEX_MAPS)

def render_date(date_:date):
    month = [
        "", "января", "февраля", "марта", "апреля", "мая", "июня", 
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ][date_.month]
    return date_.strftime(f"%d {month} %Y") 
