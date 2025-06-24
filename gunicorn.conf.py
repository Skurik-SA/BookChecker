# gunicorn.conf.py

# Количество воркеров: обычно 2 × CPU + 1
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"

# Таймаут: сколько ждать ответа от воркера
timeout = 30

# Логи
accesslog = "-"           # пишем в stdout
errorlog = "-"            # пишем в stderr
loglevel = "info"

# При желании: перезапуск воркеров при изменении кода (только dev)
reload = True
