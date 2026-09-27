import ctypes
import os
from pathlib import Path

try:
    import PySide6

    pyside6_path = Path(PySide6.__file__).parent
    print(f"PySide6 путь: {pyside6_path}")
except ImportError:
    print("PySide6 не найден")
    exit(1)

# Проверяем .pyd файлы (это Python-модули)
pyd_files = [
    "QtCore.pyd",
    "QtGui.pyd",
    "QtWidgets.pyd"
]

print("\nПроверка .pyd файлов:")

for pyd_name in pyd_files:
    pyd_path = pyside6_path / pyd_name

    if not pyd_path.exists():
        print(f"❌ {pyd_name} не найден")
        continue

    print(f"\nПробуем загрузить {pyd_name}...")
    try:
        # .pyd загружается как обычная DLL
        handle = ctypes.CDLL(str(pyd_path))
        print(f"✅ {pyd_name} загружен успешно")

        # Проверяем, есть ли функция PyInit_* (нужна для Python)
        # Имя функции зависит от версии Python
        import sys

        init_func = f"PyInit_{pyd_name.replace('.pyd', '')}"
        try:
            func = getattr(handle, init_func)
            print(f"   Функция {init_func} найдена")
        except AttributeError:
            print(f"   ⚠️ Функция {init_func} не найдена (это проблема!)")

    except Exception as e:
        print(f"❌ ОШИБКА при загрузке {pyd_name}: {e}")
        if hasattr(e, 'winerror'):
            print(f"   Код ошибки Windows: {e.winerror}")