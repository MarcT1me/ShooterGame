from loguru import logger
import os
import subprocess
from Engine.data import config, constants


def __copy(*, patch: str, name: str):
    try:
        os.makedirs(rf'{config.File.APPLICATION_path}/Engine/data/{patch}') if patch != "../../" else Ellipsis
    except FileExistsError as _:
        pass
    finally:
        with open(rf'{config.File.__ENGINE_DATA__}/{patch if patch != "../../" else ""}/{name}', 'rb') as f1:
            with open(rf'{config.File.APPLICATION_path}/Engine/data/{patch}/{name}', 'wb') as f2:
                f2.write(f1.read())


def create_project():
    logger.debug("CREATNG ENGINE PROJECT")
    try:
        for p, n in constants.__copy_arr:
            __copy(patch=p, name=n)
        os.makedirs(rf'{config.File.APPLICATION_path}/presets')
        logger.success("PROJECT CREATED")
    except Exception as e:
        logger.exception(e.args[0])
    return start()


def build(*, patch: str = config.File.APPLICATION_path, name: str = 'main.pyw'):
    def __f(i: str): return 'MainData.IS_RELEASE = YES  # YES\n' if 'IS_RELEASE' in i else i
    
    with open(rf'{patch}/Engine/data/settings.engconf', 'r') as f_r:
        data = ''.join(map(__f, f_r.readlines()))
    with open(rf'{patch}/Engine/data/settings.engconf', 'w') as f_w:
        f_w.write(data)
    
    cmd = f'pyinstaller --name \"{config.MainData.APPLICATION_name}\" ' + \
          f'--icon=\"{patch}/{config.File.APPLICATION_ICO_dir}/{config.File.APPLICATION_ICO_name}\" ' + \
          f'--add-data \"C:/Program Files/Python311/Lib/site-packages/glcontext;glcontext\" ' + \
          f'--add-data \"C:/Program Files/Python311/Lib/site-packages/toml;toml\" ' + \
          f'--add-data \"{patch}/Engine/data;../Engine/data\" ' + \
          f'--add-data \"{patch}/presets;../presets\" ' + \
          f'\"{patch}/{name}\"'
    
    result = subprocess.run(cmd, capture_output=True, text=True, check=False, shell=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)


class start:
    def __add__(self, other):
        logger.warning("START AFTER CREATING\n")
        from main import mainloop, QuantumGame
        mainloop(QuantumGame)
