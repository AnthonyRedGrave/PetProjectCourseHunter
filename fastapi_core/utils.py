import aiofiles
import os


async def upload_file(path, filename, in_file):
    filename = filename.replace(" ", "")
    try:
        out_file = await aiofiles.open(f"{path}/{filename}", 'wb+')
    except FileNotFoundError:
        os.makedirs(path)
        out_file = await aiofiles.open(f"{path}/{filename}", 'wb+')
    content = await in_file.read()  # async read
    await out_file.write(content)  # async write
    out_file_name = os.path.basename(f"{path}/{filename}")
    return out_file_name