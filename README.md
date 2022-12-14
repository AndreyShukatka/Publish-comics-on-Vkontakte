# Publish-comics-on-Vkontakte
Данный скрипт создан для публикации рандомных комиксов с комментариями с сайта [xkcd](https://xkcd.com) в указанную вами группу [Вконтакте](https://vk.com)

### Для начала работы потербуется:
1. Авторизоваться на сайте [Вконтакте](https://vk.com)
2. Создать группу, можете это сделать по [этой ссылке](https://vk.com/groups?tab=admin&w=groups_create)
3. Создать приложение. Создать приложение можно в разделе Мои приложения. Ссылка на него в шапке [данной страницы](https://vk.com/dev).
4. В качестве типа приложения следует указать `standalone` — это подходящий тип для приложений, которые просто запускаются на компьютере.
5. Получите `client_id` созданного приложения. Если нажать на кнопку `“Редактировать”` для нового приложения, в адресной строке вы увидите его `client_id`
6. Получите личный ключ. Как получить токен описано в [данной статье](https://vk.com/dev/implicit_flow_user). Параметр `redirect_uri` ненужен.
7. Узнать group_id можно по [этой ссылке](https://regvk.com/id/)





### Как установить:
1. Установить `Python`
2. Установить библиотеки из файла `requirements.txt`:
```
pip install -r requirements.txt
```
3. Создать файл `.env`
4. В файле записать ваш id клиента, id группы со знаком `-` и токен:
```
'VK_GROUP_ID' = '- id вашей группы'
'VK_CLIENT_ID' = 'Ваш id'
'VK_ACCESS_TOKEN' = 'Ваш token'
```
6. Для запуска нужно прописать в консоли:
```
python main.py
```

Если всё сделали правильно, то в вашей созданной группе появится опубликованный комикс:
![image](https://user-images.githubusercontent.com/106096891/184088225-fbff0b13-eb3c-461a-a754-d8282e6061eb.png)
