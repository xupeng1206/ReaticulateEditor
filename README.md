# ReaticulateEditor Quick Start
## 1. install
```
0. make sure you already install the Reaticulate, and backup you own Reaticulate.reabank 

1. git clone git@github.com:xupeng1206/ReaticulateEditor.git

2. put the script into reaper resource folder like this:

└── ReaperResourceFolder
    └── Scripts
        └── ReaticulateEditor
            ├── README.md
            ├── Reaticulate_example.reabank
            ├── icons
            │   ├── folder.jpeg
            │   └── item.jpeg
            ├── reaticulate_editor.py
            └── xup_start_Reaticulate_Editor.py

3. enable python in reaper, see: https://forum.reaget.com/t/topic/175

4. pip install pyqt5 -i https://mirrors.aliyun.com/pypi/simple

5. load xup_start_Reaticulate_Editor.py in reaper's action_list

6. run xup_start_Reaticulate_Editor.py action in reaper
```

## 2.  Reaticulate.reabank Supported Format in ReaticulateEditor

```
Example:

//----------------------------------------------------------------------------
//! g="Ample Sound" n="Ample Bass J II"
//! m="Set patch to UACC"
Bank 70 1 ABJ - Basic Articulations

//! c=long i=fx g=2 o=note:105,127
127 Tap Player ON

//! c=long i=fx g=2 o=cc:64,127
127 Tap Player ON


only support tag: 
bank_level: g n msb lsb bank_name
art_level: c i g o(note cc note-hold [@,])

not support tag:
chase clone pitch ...
```

## 3. video tutorial
comming sure ...