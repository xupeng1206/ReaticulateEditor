"""
Audio         xupeng
Eamil         874582705@qq.com / 15601598009@163.com
github        https://github.com/xupeng1206

"""

import sys
import os
from subprocess import run
from reaper_python import *
from multiprocessing import Process

def main():
    reaper_resource_path = RPR_GetResourcePath()
    editor_path = os.path.join(reaper_resource_path, "Scripts", "ReaticulateEditor", "reaticulate_editor.py")
    cmd = f"python {editor_path} {reaper_resource_path}"
    os.system(cmd)


if __name__ == '__main__':
    p = Process(target=main)
    p.start()
    p.join()
