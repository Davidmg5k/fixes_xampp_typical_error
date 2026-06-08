import os
import sys
import shutil

def fixer():
    base_path = r"C:\xampp\mysql"
    data_path = os.path.join(base_path, "data")
    data_old_path = os.path.join(base_path, "data_old")
    backup_path = os.path.join(base_path, "backup")

    print("=== FIX XAMPP MYSQL ===")

    # 1. Renombrar data -> data_old
    if os.path.exists(data_path):
        if os.path.exists(data_old_path):
            print("❌ ERROR: La carpeta 'data_old' ya existe. Elimínala o muévela antes.")
            sys.exit(1)
        os.rename(data_path, data_old_path)
        print("✔ Renombrado 'data' a 'data_old'")
    else:
        print("ℹ No existía 'data'. Continuando...")

    # 2. Crear nueva carpeta data
    os.makedirs(data_path, exist_ok=True)
    print("✔ Carpeta 'data' creada")

    # 3. Copiar contenido de backup → data
    if not os.path.exists(backup_path):
        print("❌ ERROR: La carpeta 'backup' no existe. No se puede continuar.")
        sys.exit(1)

    for item in os.listdir(backup_path):
        src = os.path.join(backup_path, item)
        dst = os.path.join(data_path, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    print("✔ Copiado contenido de 'backup' hacia 'data'")

    # 4. Copiar ibdata1 y carpetas permitidas desde data_old
    exclusions = {"mysql", "performance_schema", "phpmyadmin"}

    ibdata = os.path.join(data_old_path, "ibdata1")
    if os.path.exists(ibdata):
        shutil.copy2(ibdata, os.path.join(data_path, "ibdata1"))
        print("✔ Copiado 'ibdata1'")
    else:
        print("⚠ 'ibdata1' no existe en data_old")

    for item in os.listdir(data_old_path):
        if item in exclusions:
            continue
        
        src = os.path.join(data_old_path, item)
        dst = os.path.join(data_path, item)

        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"✔ Copiada carpeta '{item}'")

    # 5. ELIMINAR CARPETA data_old
    try:
        shutil.rmtree(data_old_path)
        print("🗑️  Carpeta 'data_old' eliminada correctamente.")
    except Exception as e:
        print(f"⚠ No se pudo eliminar 'data_old': {e}")

    print("\n🎉 PROCESO COMPLETADO CORRECTAMENTE\n")
