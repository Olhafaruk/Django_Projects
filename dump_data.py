import os
import json
from django.core.serializers import serialize
from django.apps import apps
import django

# Установите настройки проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itg.settings')
django.setup()

# Укажите ваши модели
models = apps.get_models()

data = []
for model in models:
    serialized_data = serialize('json', model.objects.all())
    data.extend(json.loads(serialized_data))

# Запишите данные в файл db.json с кодировкой UTF-8
with open('db.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
