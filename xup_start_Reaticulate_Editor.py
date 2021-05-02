"""
Audio         xupeng
Eamil         874582705@qq.com / 15601598009@163.com
github        https://github.com/xupeng1206

"""

import os
import platform
from reaper_python import *
import subprocess

win_vbs_script_tpl = """
set objShell=wscript.createObject("wscript.shell")
iReturn=objShell.Run("cmd /c python {editor_path} {reaper_resource_path}", 0, FALSE) 
"""


def main():
    reaper_resource_path = RPR_GetResourcePath()
    editor_path = os.path.join(reaper_resource_path, "Scripts", "ReaticulateEditor", "reaticulate_editor.py")
    vbs_path = os.path.join(reaper_resource_path, "Scripts", "ReaticulateEditor", "reaticulate_editor.vbs")
    system_type = platform.system()
    if system_type == "Windows":
        vbs_content = win_vbs_script_tpl.format(
            editor_path=editor_path,
            reaper_resource_path=reaper_resource_path
        )
        with open(vbs_path, 'w') as f:
            f.writelines(vbs_content)
        cmd = f"start {vbs_path}"
    elif system_type == "Darwin":  # mac os 10.15.7
        cmd = f"python {editor_path} {reaper_resource_path} &"
    elif system_type == "Linux":
        cmd = f"python {editor_path} {reaper_resource_path} &"
    else:
        cmd = f"python {editor_path} {reaper_resource_path} &"
    subprocess.run(cmd, shell=True)
    

if __name__ == '__main__':
    main()
