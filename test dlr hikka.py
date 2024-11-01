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
            if reply.text:
                # Если это текст, сохраняем его в файл
                text = reply.text
                fname = f'{name or message.id+reply.id}.txt'
                with open(fname, 'w') as file:
                    file.write(text)
                
                # Отправляем файл в "Избранное"
                await message.client.send_file('me', fname)
                os.remove(fname)  # Удаляем файл после отправки
                await message.edit('Текст успешно отправлен в Избранное.')
            else:
                # Если это файл, скачиваем и отправляем
                ext = reply.file.ext
                fname = f'{name or message.id+reply.id}{ext}'
                await message.client.download_media(reply, fname)
                
                # Отправляем файл в "Избранное"
                await message.client.send_file('me', fname)
                os.remove(fname)  # Удаляем файл после отправки
                await message.edit('Файл успешно отправлен в Избранное.')
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