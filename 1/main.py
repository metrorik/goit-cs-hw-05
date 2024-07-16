import asyncio
import aiofiles
import os
from pathlib import Path
import logging

# логування
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_folder: Path, target_folder: Path):
    # читання файлів у вихідній папці та підпапках
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_path = Path(root) / file
            await copy_file(source_path, target_folder)

async def copy_file(source_path: Path, target_folder: Path):
    # копіювання до цільової папки на основі розширення
    file_extension = source_path.suffix.lstrip('.').lower()
    target_path = target_folder / file_extension / source_path.name
    target_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        async with aiofiles.open(source_path, 'rb') as src:
            content = await src.read()
        async with aiofiles.open(target_path, 'wb') as dst:
            await dst.write(content)
    except Exception as e:
        logging.error(f'Помилка при копіюванні файлу {source_path} до {target_path}: {e}')

async def main():
    # запит назв папок
    source_folder_name = input("Введіть назву вихідної папки: ")
    target_folder_name = input("Введіть назву цільової папки: ")

    source_folder = Path(source_folder_name).resolve()
    target_folder = Path(target_folder_name).resolve()

    if not source_folder.is_dir():
        logging.error(f'Вихідна папка не існує: {source_folder}')
        return

    if not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)

    # читання вихідної папки та копіювання файлів до цільової папки
    await read_folder(source_folder, target_folder)

if __name__ == '__main__':
    asyncio.run(main())
