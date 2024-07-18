import argparse
import asyncio
import aiofiles
from pathlib import Path
import logging

# логування
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# рекурсивне читання підпапок та файлів
async def read_folder(source_folder: Path, target_folder: Path):
    for item in source_folder.iterdir():
        if item.is_dir():
            await read_folder(item, target_folder)
        else:
            await copy_file(item, target_folder)

# копіювання файлів на основі розширення
async def copy_file(source_path: Path, target_folder: Path):
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


# запуск та обробка аргументів командного рядка
async def main(source_folder: Path, target_folder: Path):
    if not source_folder.is_dir():
        logging.error(f'Вихідна папка не існує: {source_folder}')
        return

    if not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)

    await read_folder(source_folder, target_folder)



if __name__ == '__main__':
    # Створення об'єкту ArgumentParser для обробки аргументів командного рядка
    parser = argparse.ArgumentParser(description="Асинхронне копіювання та сортування файлів за розширеннями.")
    parser.add_argument('source_folder', type=str, help='Шлях до вихідної папки.')
    parser.add_argument('target_folder', type=str, help='Шлях до цільової папки.')
    args = parser.parse_args()

    source_folder = Path(args.source_folder).resolve()
    target_folder = Path(args.target_folder).resolve()

    asyncio.run(main(source_folder, target_folder))
