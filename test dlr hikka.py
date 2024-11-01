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
            # Отправка текста, если он присутствует в ответе
            if reply.text:
                text = reply.text
                text_fname = f'{name or message.id+reply.id}_text.txt'
                with open(text_fname, 'w') as text_file:
                    text_file.write(text)
                
                # Отправляем файл с текстом в "Избранное"
                await message.client.send_file('me', text_fname)
                os.remove(text_fname)  # Удаляем текстовый файл после отправки

            # Отправка файла, если он присутствует в ответе
            if reply.file:
                ext = reply.file.ext
                file_fname = f'{name or message.id+reply.id}{ext}'
                await message.client.download_media(reply, file_fname)
                
                # Отправляем скачанный файл в "Избранное"
                await message.client.send_file('me', file_fname)
                os.remove(file_fname)  # Удаляем скачанный файл после отправки
            
            await message.edit('Содержимое успешно отправлено в Избранное.')
        else:
            return await message.edit('Нет реплая.')

    async def ulfcmd(self, message):
        """Команда .ulf <d>* <название файла> отправляет файл в чат.\n* - удалить файл после отправки."""
        name = utils.get_args_raw(message)
        d = False
        if('d ' in name):
            d = True
        if name:
            try:
                name = name.replace('d ', '')
                await message.edit(f'Отправляем <code>{name}</code>...')
                if d == True:
                    await message.client.send_file(message.to_id, f'{name}')
                    await message.edit(f'Отправляем <code>{name}</code>... Успешно!\nУдаляем <code>{name}</code>...')
                    os.remove(name)
                    await message.edit(f'Отправляем <code>{name}</code>... Успешно!\nУдаляем <code>{name}</code>... Успешно!')
                    await sleep(0.5)
                else:
                    await message.client.send_file(message.to_id, name)
            except:
                return await message.edit('Такой файл не существует.')
            await message.delete()
        else:
            return await message.edit('Нет аргументов.')
