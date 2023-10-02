import subprocess
import os

# Запуск парсера link_parser.py для получения списка ссылок на
# товары zappos_shoes_urls.txt
subprocess.call([os.sys.executable, "link_parser.py"])

# После завершения выполнения link_parser.py запуск content_parser.py
# он переходит по ссылкам из файла zappos_shoes_urls.txt , записывает
# контент в таблицу zappos_{актуальная дата}.xlsx и собирает фото
# размещая их по папкам согласно критерию бренд
subprocess.call([os.sys.executable, "content_parser.py"])
