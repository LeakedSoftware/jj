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

            # Сохраняем текст, если он есть
            if reply.text:
                text_fname = f'{name or message.id+reply.id}_text.txt'
                with open(text_fname, 'w') as text_file:
                    text_file.write(reply.text)
                await message.client.send_file('me', text_fname)
                os.remove(text_fname)
                sent_anything = True

            # Сохраняем медиа, если оно присутствует
            if reply.media:
                media_files = []
                
                # Проверяем наличие документа
                if reply.document:
                    media_files.append(reply.document)
                # Проверяем наличие фото
                elif reply.photo:
                    media_files.append(reply.photo)
                
                # Скачиваем и отправляем каждый файл
                for index, media in enumerate(media_files):
                    fname = f'{name or message.id+reply.id}_{index}.file'
                    await message.client.download_media(media, fname)
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

    async def ulfcmd(self, message):
        """Команда .ulf <d>* <название файла> отправляет файл в чат.\n* - удалить файл после отправки."""
        name = utils.get_args_raw(message)
        d = 'd ' in name
        if name:
            name = name.replace('d ', '')
            try:
                await message.edit(f'Отправляем <code>{name}</code>...')
                await message.client.send_file(message.to_id, name)
                if d:
                    os.remove(name)
                    await message.edit(f'Файл <code>{name}</code> отправлен и удалён.')
                await sleep(0.5)
            except FileNotFoundError:
                await message.edit('Такой файл не существует.')
            await message.delete()
        else:
            await message.edit('Нет аргументов.')
