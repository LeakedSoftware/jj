import os
from .. import loader, utils
from asyncio import sleep

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

            # Отправка текста, если он присутствует в ответе
            if reply.text:
                text = reply.text
                text_fname = f'{name or message.id+reply.id}_text.txt'
                with open(text_fname, 'w') as text_file:
                    text_file.write(text)
                
                # Отправляем файл с текстом в "Избранное"
                await message.client.send_file('me', text_fname)
                os.remove(text_fname)  # Удаляем текстовый файл после отправки
                sent_anything = True

            # Отправка файла, если он присутствует в ответе
            if reply.file:
                ext = reply.file.ext or ""  # Получаем расширение, если оно есть
                file_fname = f'{name or message.id+reply.id}{ext}'
                await message.client.download_media(reply, file_fname)
                
                # Отправляем скачанный файл в "Избранное"
                await message.client.send_file('me', file_fname)
                os.remove(file_fname)  # Удаляем скачанный файл после отправки
                sent_anything = True

            if sent_anything:
                # Здесь можно добавить, что именно было отправлено, если нужно
                await message.delete()
            else:
                await message.client.send_message('me', 'Нет текста или файлов для отправки.')
        else:
            await message.client.send_message('me', 'Нет реплая.')

        # Удаляем оригинальное сообщение
        await message.delete()
