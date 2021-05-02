"""
Audio         xupeng
Eamil         874582705@qq.com / 15601598009@163.com
github        https://github.com/xupeng1206

"""

import os
import platform
from reaper_python import *

def main():
    reaper_resource_path = RPR_GetResourcePath()
    editor_path = os.path.join(reaper_resource_path, "Scripts", "ReaticulateEditor", "reaticulate_editor.py")
    system_type = platform.system()
    if system_type == "Window":
        cmd = f'start cmd /c python {editor_path} {reaper_resource_path}'
    elif system_type == "Darwin":  # mac os 10.15.7
        cmd = f"python {editor_path} {reaper_resource_path} &"
    elif system_type == "Linux":
        cmd = f"python {editor_path} {reaper_resource_path} &"
    else:
        cmd = f"python {editor_path} {reaper_resource_path} &"
    os.system(cmd)


if __name__ == '__main__':
    main()
