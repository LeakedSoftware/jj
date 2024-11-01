from hikka import loader, utils
from telethon import events

def register(cb):
    cb(ReplyDownloaderMod1())

class ReplyDownloaderMod1(loader.Module):
    """Скачать файлом реплай и отправить в избранное."""
    strings = {'name': 'Reply Downloader'}

    async def dlrcmd(self, message):
        """Команда .dlr <реплай на файл> <название (по желанию)> скачивает файл, либо сохраняет текст в файл на который был сделан реплай, и отправляет в избранное."""
        name = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if reply:
            sent_anything = False  # Флаг для отслеживания отправки содержимого

            # Сохраняем текст, если он есть
            if reply.text:
                text_fname = f'{name or message.id + reply.id}_text.txt'
                with open(text_fname, 'w') as text_file:
                    text_file.write(reply.text)
                await message.client.send_file('me', text_fname)
                os.remove(text_fname)
                sent_anything = True

            # Проверяем, есть ли медиафайлы в реплае
            if reply.media:
                media_files = []

                # Если это альбом, обрабатываем его
                if hasattr(reply.media, 'media_album_id'):
                    async for msg in message.client.iter_messages(reply.chat_id, media_album_id=reply.media.media_album_id):
                        media_files.append(msg)
                else:
                    media_files.append(reply)  # Просто одно сообщение с медиа

                # Скачиваем и отправляем каждый файл
                for index, media_message in enumerate(media_files):
                    if media_message.media:
                        fname = f'{name or message.id + reply.id}_{index}.file'
                        await message.client.download_media(media_message, fname)
                        await message.client.send_file('me', fname)
                        os.remove(fname)
                        sent_anything = True

            # Сообщение, если отправлено содержимое
            if sent_anything:
                await message.edit('Содержимое успешно отправлено в Избранное.')
            else:
                await message.edit('Нет текста или файлов для отправки.')
        else:
            await message.edit('Нет реплая.')

    @events.register(events.Album)
    async def albumHandler(self, event):
        """Обработчик альбома."""
        # Отправляем весь альбом в нужный чат
        await event.forward_to('me')
