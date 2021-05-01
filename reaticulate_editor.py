"""
Audio         xupeng
Eamil         874582705@qq.com / 15601598009@163.com
github        https://github.com/xupeng1206

"""
import sys
import os
import re
import itertools
from pathlib import Path
from copy import deepcopy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime


reaper_resource_path = sys.argv[1]

reabank_file_path = os.path.join(reaper_resource_path, "Data", "Reaticulate.reabank")
folder_icon_path = os.path.join(reaper_resource_path, "Scripts", "ReaticulateEditor", "icons", "folder.jpeg")
item_icon_path = os.path.join(reaper_resource_path, "Scripts", "ReaticulateEditor", "icons", "item.jpeg")

g_icons = [
    'accented-half',
    'accented-quarter',
    'acciaccatura-quarter',
    'alt-circle',
    'alt-gypsy',
    'alt-gypsy-eighth',
    'alt-gypsy-harmonics',
    'alt-tremolo-gypsy-harmonics',
    'alt-wave',
    'alt-wave-double',
    'alt-wave-double-stopped',
    'alt-wave-double-tr',
    'alt-x',
    'blend',
    'bow-down',
    'bow-up',
    'col-legno',
    'col-legno-loose',
    'col-legno-whole',
    'con-sord',
    'con-sord-blend',
    'con-sord-bow-down',
    'con-sord-bow-up',
    'con-sord-sul-pont',
    'con-sord-sul-pont-bow-up',
    'cresc-f-half',
    'cresc-half',
    'cresc-m-half',
    'cresc-mf-half',
    'cresc-mp-half',
    'cresc-p-half',
    'cresc-quarter',
    'crescendo',
    'cuivre',
    'dblstop-5th',
    'dblstop-5th-eighth',
    'decrescendo',
    'esp-half',
    'fall',
    'fanfare',
    'flautando',
    'flautando-con-sord',
    'flautando-con-sord-eighth',
    'frozen',
    'frozen-eighth',
    'fx',
    'ghost-eighth',
    'harmonics',
    'harmonics-natural',
    'harmonics-natural-eighth',
    'harp-pdlt',
    'harp-pdlt2',
    'legato',
    'legato-blend-generic',
    'legato-bowed',
    'legato-bowed2',
    'legato-con-sord',
    'legato-fast',
    'legato-flautando',
    'legato-gliss',
    'legato-portamento',
    'legato-portamento-con-sord',
    'legato-portamento-flautando',
    'legato-runs',
    'legato-slow',
    'legato-slow-blend',
    'legato-slurred',
    'legato-sul-c',
    'legato-sul-g',
    'legato-sul-pont',
    'legato-tremolo',
    'legato-vibrato',
    'list',
    'marcato',
    'marcato-half',
    'marcato-quarter',
    'multitongued',
    'no-rosin',
    'note-eighth',
    'note-half',
    'note-quarter',
    'note-sixteenth',
    'note-whole',
    'phrase',
    'phrase-tremolo',
    'phrase-tremolo-cresc',
    'pizz',
    'pizz-b',
    'pizz-bartok',
    'pizz-c',
    'pizz-con-sord',
    'pizz-mix',
    'pizz-sul-pont',
    'rest-quarter',
    'riccochet',
    'rip',
    'rip-downward',
    'run-major',
    'run-minor',
    'sfz',
    'spiccato',
    'spiccato-breath',
    'spiccato-brushed',
    'spiccato-brushed-con-sord',
    'spiccato-brushed-con-sord-sul-pont',
    'spiccato-feathered',
    'staccatissimo-stopped',
    'staccato',
    'staccato-breath',
    'staccato-con-sord',
    'staccato-dig',
    'staccato-harmonics',
    'staccato-harmonics-half',
    'staccato-overblown',
    'staccato-sfz',
    'stopped',
    'sul-c',
    'sul-g',
    'sul-pont',
    'sul-tasto',
    'sul-tasto-super',
    'sul-tasto-super-eighth',
    'tenuto-eighth',
    'tenuto-half',
    'tenuto-quarter',
    'tremolo',
    'tremolo-150',
    'tremolo-150-con-sord',
    'tremolo-180',
    'tremolo-180-con-sord',
    'tremolo-con-sord',
    'tremolo-con-sord-sul-pont',
    'tremolo-ghost',
    'tremolo-harmonics',
    'tremolo-harmonics-a',
    'tremolo-harmonics-b',
    'tremolo-measured',
    'tremolo-slurred',
    'tremolo-sul-pont',
    'trill',
    'trill-maj2',
    'trill-maj3',
    'trill-min2',
    'trill-min3',
    'trill-perf4',
    'vibrato',
    'vibrato-con-sord',
    'vibrato-molto',
    'vibrato-rachmaninoff',
]

g_text_color = {
    "default": '#666666',
    'short': '#6c30c6',
    'short-light': "#9630c6",
    'short-dark': '#533bca',
    'legato': '#218561',
    'legato-dark': '#1c5e46',
    'legato-light': '#49ba91',
    'long': '#305fc6',
    'long-light': '#4474e1',
    'long-dark': '#2c4b94',
    'textured': '#9909bd',
    'fx': '#883333',
}

g_color_text = dict(zip(g_text_color.values(), g_text_color.keys()))


g_note_num = {}
num_group = -1
num_start = 0
while num_start < 128:
    for note in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']:
        g_note_num[f'{note}{str(num_group)}'] = str(num_start)
        num_start += 1
    num_group += 1


g_num_note = dict(zip(g_note_num.values(), g_note_num.keys()))


class FileUtil:

    path = ''
    bank_split = "//----------------------------------------------------------------------------"

    @classmethod
    def parse_file(cls, path):
        cls.path = path
        file_content = ''
        with open(path, "r") as f:
            file_content = f.read()

        if not file_content:
            return {}

        ret = {}
        banks = file_content.split(cls.bank_split)[1:] if cls.bank_split in file_content else []
        for bank in banks:
            lines = bank.split('\n')
            lines = [x.strip() for x in lines if x.strip() != '']
            lines = [x.strip('\n') for x in lines if x.strip() != '']
            bank_line_found = False
            bank_info = {}
            full_name = ''
            for line in lines:
                if bank_line_found:

                    if line.startswith('//!'):
                        line = line[3:].strip()
                        art_info = {}
                        k_vs = line.split(' ')
                        k_vs = [x.strip() for x in k_vs if x != '']
                        for k_v in k_vs:
                            if k_v.startswith("c="):
                                art_info['c'] = k_v.split('c=')[-1].strip()
                            if k_v.startswith("i="):
                                art_info['i'] = k_v.split('i=')[-1].strip()
                            if k_v.startswith("g="):
                                art_info['g'] = k_v.split('g=')[-1].strip()
                            if k_v.startswith("o="):
                                art_info['o'] = []
                                o_vals = k_v.split('o=')[-1].strip()
                                controls = o_vals.split('/')
                                controls = [x.strip() for x in controls if x != '']
                                for control in controls:
                                    control_k_v = control.split(':')
                                    control_prefix = control_k_v[0]
                                    ch = ''
                                    if '@' in control_prefix:
                                        control_type = control_prefix.split('@')[0]
                                        ch = control_prefix.split('@')[1]
                                    else:
                                        control_type = control_prefix
                                    control_args = control_k_v[1]
                                    control_info = {}
                                    control_info['type'] = control_type
                                    if ch:
                                        control_info['chancel'] = ch
                                    control_info['args'] = control_args
                                    art_info['o'].append(control_info)
                        bank_info['list'].append(art_info)
                    else:
                        art_no = line.split(' ')[0]
                        art_name = line[len(art_no):].strip()
                        bank_info['list'][-1]['no'] = art_no
                        bank_info['list'][-1]['name'] = art_name
                else:
                    if line.startswith('//!'):
                        line = line[3:].strip()
                        bank_g = cls.find_bank_g(line)
                        if bank_g:
                            bank_info['g'] = bank_g
                        bank_m = cls.find_bank_m(line)
                        if bank_m:
                            bank_info['m'] = bank_m
                        bank_n = cls.find_bank_n(line)
                        if bank_n:
                            bank_info['n'] = bank_n
                    elif line.startswith("Bank"):
                        patterns = line.split(' ')
                        patterns = [x.strip() for x in patterns if x != '']
                        msb = patterns[1]
                        lsb = patterns[2]
                        new_line_str = ' '.join(patterns)
                        new_line_prefix = ' '.join(['Bank', str(msb), str(lsb)])
                        bank_name = new_line_str[len(new_line_prefix):].strip()
                        bank_info['msb'] = str(msb)
                        bank_info['lsb'] = str(lsb)
                        bank_info['bank_name'] = bank_name
                        if 'n' not in bank_info:
                            bank_info['n'] = bank_name
                        bank_info['list'] = []
                        full_name = f'{bank_info["g"]}/{bank_info["n"]}'
                        bank_line_found = True
                    else:
                        print('error format, not support!!!')
            if full_name:
                ret[full_name] = bank_info

        return ret

    @classmethod
    def save_file(cls, data):
        os.rename(cls.path, f'{cls.path}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}')
        with open(cls.path, "w") as f:
            for full_name, vals in data.items():
                f.write(cls.bank_split + '\n')
                g = vals.get('g', '')
                n = vals.get('n', '')
                m = vals.get('m', '')
                msb = vals['msb']
                lsb = vals['lsb']
                bank_name = vals.get('bank_name', '')
                f.write(f'//! g="{g}" n="{n}"\n')
                f.write(f'//! m="{m}"\n')
                f.write(f'Bank {msb} {lsb} {bank_name if bank_name else n}\n')
                f.write('\n')
                for art in vals['list']:
                    art_no = art['no']
                    art_name = art['name']
                    art_c = art['c']
                    art_i = art['i']
                    art_g = art.get('g', '1')
                    art_o = art['o']

                    action_texts = []
                    for action in art_o:
                        if 'channel' in action:
                            action_text = f'{action["type"] if "type" in action else ""}@{action["channel"]}:{action["args"] if "args" in action else ""}'
                        else:
                            action_text = f'{action["type"] if "type" in action else ""}:{action["args"] if "args" in action else ""}'
                            if action_text == ":":
                                continue
                        action_texts.append(action_text)
                    actions_text = "o=" + '/'.join(action_texts)

                    f.write(f'//! c={art_c} i={art_i} g={art_g} {actions_text}\n')
                    f.write(f'{art_no} {art_name}\n')

                f.write('\n')


    @classmethod
    def find_bank_g(cls, line):
        pattern = re.compile(r'g="(.*?)"')
        rets = pattern.findall(line)
        if rets:
            return rets[0].strip()
        else:
            return ''

    @classmethod
    def find_bank_n(cls, line):
        pattern = re.compile(r'n="(.*?)"')
        rets = pattern.findall(line)
        if rets:
            return rets[0].strip()
        else:
            return ''

    @classmethod
    def find_bank_m(cls, line):
        pattern = re.compile(r'm="(.*?)"')
        rets = pattern.findall(line)
        if rets:
            return rets[0].strip()
        else:
            return ''


class ReaticulateEditor(QWidget):

    tree_nodes = {}
    data = {}
    ori_data = {}

    next_msb = "64"
    next_lsb = "0"

    selected_full_name = ""
    selected_art_index = None
    selected_art_data = {}

    components_full_name_input = None
    components_art_no_input = None
    components_art_name_input = None
    components_art_icon_input = None
    components_art_color_label = None
    components_art_group_input = None
    components_art_control_list = []

    def __init__(self, data, *args, **kwargs):
        super().__init__()
        self.data = data
        self.ori_data = deepcopy(self.data)
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ReaticulateEditor')
        self.setGeometry(200, 200, 1300, 700)
        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)

        self.left_tree = self.ui_left()
        self.grid_layout.addWidget(self.left_tree, 0, 0)

        self.middle_list = self.ui_middle()
        self.grid_layout.addWidget(self.middle_list, 0, 1)

        self.right_editor = self.ui_articulation_editor()
        self.grid_layout.addWidget(self.right_editor, 0, 2)

        spliter = QLabel()
        spliter.setFixedHeight(1)
        spliter.setStyleSheet('background-color: rgb(192,192,192);')
        self.grid_layout.addWidget(spliter, 1, 0, 1, 3)

        self.grid_layout.addWidget(self.ui_total_botton(), 2, 0, 1, 3)

    def ui_total_botton(self):
        wight = QWidget()
        wight.setContentsMargins(0, 0, 0, 0)
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(0, 0, 0, 0)

        btn0 = QPushButton('Check Data In Memory')
        btn0.clicked.connect(self.action_check_data_in_memory)
        editor_layout.addWidget(btn0)

        btn1 = QPushButton('Reload Data From File')
        btn1.clicked.connect(self.action_reload_from_file)
        editor_layout.addWidget(btn1)

        btn2 = QPushButton('Save Data To File')
        btn2.clicked.connect(self.action_save_to_file)
        editor_layout.addWidget(btn2)

        wight.setLayout(editor_layout)
        return wight

    def ui_left(self):
        wight = QWidget()
        wight.setContentsMargins(0, 0, 0, 0)
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)

        layout_main.addWidget(self.ui_bank_list())
        layout_main.addWidget(self.ui_left_bottom())
        wight.setLayout(layout_main)
        return wight

    def ui_bank_list(self):
        self.bank_tree = QTreeWidget()
        self.bank_tree.setColumnCount(4)
        self.bank_tree.setHeaderLabels(['Path', 'MSB', 'LSB', 'Full Name'])
        self.bank_tree.setColumnWidth(0, 200)
        self.bank_tree.setColumnWidth(1, 40)
        self.bank_tree.setColumnWidth(2, 40)
        self.bank_tree.setContentsMargins(0, 0, 0, 0)

        root = QTreeWidgetItem(self.bank_tree)
        for i in range(4):
            ft = QFont()
            ft.setPointSize(10)
            root.setFont(i, ft)
        root.setText(0, 'Librarys')
        root.setIcon(0, QIcon(folder_icon_path))
        self.tree_nodes[''] = root

        for line in self.data.keys():
            names = line.split('/')
            for index in range(len(names)):
                key = '/'.join(names[:index + 1])
                if key not in self.tree_nodes:
                    parent_key = '/'.join(names[:index])
                    current_item = QTreeWidgetItem()
                    for i in range(4):
                        ft = QFont()
                        ft.setPointSize(10)
                        current_item.setFont(i, ft)
                    current_item.setText(0, names[index])
                    current_item.setIcon(0, QIcon(folder_icon_path))
                    if index == len(names) - 1:
                        current_item.setText(1, self.data[line]['msb'])
                        current_item.setText(2, self.data[line]['lsb'])
                        current_item.setText(3, key)
                        current_item.setIcon(0, QIcon(item_icon_path))
                    self.tree_nodes[parent_key].addChild(current_item)
                    self.tree_nodes[key] = current_item

        self.bank_tree.clicked.connect(self.action_bank_list_item_clicked)
        return self.bank_tree

    def ui_left_bottom(self):
        wight = QWidget()
        wight.setContentsMargins(0, 0, 0, 0)
        wight.adjustSize()
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)

        editor_up = QHBoxLayout()
        editor_up.setContentsMargins(0, 0, 0, 0)

        laber = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber.setFont(ft)
        laber.setText("Full Name:")
        laber.setFixedWidth(70)
        laber.setScaledContents(True)
        laber.setAlignment(Qt.AlignVCenter)
        laber.adjustSize()
        editor_up.addWidget(laber)

        self.components_full_name_input = QLineEdit()
        editor_up.addWidget(self.components_full_name_input)

        layout_main.addLayout(editor_up)


        editor_down = QHBoxLayout()
        editor_down.setContentsMargins(0, 0, 0, 0)

        btn1 = QPushButton('New Bank')
        btn1.clicked.connect(self.action_new_bank)
        editor_down.addWidget(btn1)

        btn2 = QPushButton('Delete Selected Bank')
        btn2.clicked.connect(self.action_del_selected_bank)
        editor_down.addWidget(btn2)
        layout_main.addLayout(editor_down)

        wight.setLayout(layout_main)
        return wight

    def ui_middle(self):
        wight = QWidget()
        wight.setContentsMargins(0, 0, 0, 0)
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)

        layout_main.addWidget(self.ui_articulation_list())
        layout_main.addWidget(self.ui_middle_bottom())
        wight.setLayout(layout_main)
        return wight

    def ui_articulation_list(self):
        wight = QWidget()
        wight.setContentsMargins(0, 0, 0, 0)
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)

        infoWidget = self.ui_articulation_bank_info()

        self.art_list_widget = QListWidget()
        self.art_list_widget.setGeometry(QRect(0, 0, 300, 300))
        self.art_list_widget.setObjectName("articulation_list")

        bank_arts = self.data[self.selected_full_name]['list'] if self.selected_full_name in self.data else []
        for index, item_data in enumerate(bank_arts):
            item = QListWidgetItem()
            item.index = index
            item.bank_full_name = self.selected_full_name
            item.data = item_data
            item.setSizeHint(QSize(200, 60))
            widget = self.ui_articulation_item(item_data)
            self.art_list_widget.addItem(item)
            self.art_list_widget.setItemWidget(item, widget)
        self.art_list_widget.clicked.connect(self.action_articulation_item_clicked)

        layout_main.addWidget(infoWidget)
        layout_main.addWidget(self.art_list_widget)
        wight.setLayout(layout_main)
        return wight

    def ui_articulation_bank_info(self):
        wight = QWidget()
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(10, 2, 10, 2)
        text = f"Full Name:  /{self.selected_full_name}" if self.selected_full_name else "Full Name:"
        laber = QLabel(text)
        ft = QFont()
        ft.setPointSize(10)
        laber.setFont(ft)
        layout_main.addWidget(laber)

        wight.setLayout(layout_main)
        return wight

    def ui_articulation_item(self, data):

        wight = QWidget()

        layout_main = QHBoxLayout()

        map_l = QLabel()
        map_l.setFixedSize(40, 40)
        maps = QPixmap(item_icon_path).scaled(40, 40)
        map_l.setPixmap(maps)

        layout_main.addWidget(map_l)

        layout_right = QVBoxLayout()

        no_and_name_layout = QHBoxLayout()

        no = QLabel(str(data['no']))
        no.setFixedWidth(15)
        no.setAlignment(Qt.AlignVCenter)
        name = QLabel(data['name'])
        name.setAlignment(Qt.AlignVCenter)

        group = QLabel(f"[{data['g']}]" if 'g' in data else '1')
        group.setFixedWidth(18)
        group.setAlignment(Qt.AlignVCenter)

        no_and_name_layout.addWidget(no)
        no_and_name_layout.addWidget(group)
        no_and_name_layout.addWidget(name)

        actions = data['o']
        action_texts = []
        for action in actions:
            if 'channel' in action:
                action_text = f'{action["type"] if "type" in action else ""}@{action["channel"]}:{action["args"] if "args" in action else ""}'
            else:
                action_text = f'{action["type"] if "type" in action else ""}:{action["args"] if "args" in action else ""}'
                if action_text == ":":
                    continue
            action_texts.append(action_text)
        actions_text = "o=" + '/'.join(action_texts)

        right_down = QLabel(actions_text)
        layout_right.addLayout(no_and_name_layout)
        layout_right.addWidget(right_down)

        layout_main.addLayout(layout_right)
        wight.setLayout(layout_main)
        return wight

    def ui_middle_bottom(self):

        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(0, 0, 0, 0)

        btn1 = QPushButton('New Articulation')
        btn1.clicked.connect(self.action_new_articulation)
        editor_layout.addWidget(btn1)

        btn2 = QPushButton('Delete Selected Articulation')
        btn2.clicked.connect(self.action_del_selected_articulation)
        editor_layout.addWidget(btn2)

        wight.setLayout(editor_layout)
        return wight

    def ui_articulation_editor(self, enable=False):

        wight = QWidget()
        wight.setContentsMargins(0, 0, 0, 0)

        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)

        self.r_listWidget = QListWidget()
        self.r_listWidget.setObjectName("articulation_editor")

        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_line_desc_title("Common Options")
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_line_desc_detail()
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_icon_detail()
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_color_detail()
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_group_detail()
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_line_desc_title("Control Actions")
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_add_action()
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

        actions = self.selected_art_data.get('o', [])
        for action in actions:
            widget = None
            type = action['type']
            if type == "cc":
                widget = self.ui_art_cc_control(action)
            elif type == "note":
                widget = self.ui_art_note_control(action)
            elif type == "note-hold":
                widget = self.ui_art_note_hold_control(action)
            else:
                pass
            if widget:
                item = QListWidgetItem()
                item.setSizeHint(QSize(50, 40))
                self.r_listWidget.addItem(item)
                self.r_listWidget.setItemWidget(item, widget)

        layout_main.addWidget(self.r_listWidget)
        layout_main.addWidget(self.ui_editor_bottom())
        wight.setLayout(layout_main)
        wight.setEnabled(enable)
        return wight

    def ui_art_line_desc_title(self, label_name):
        wight = QWidget()
        wight.adjustSize()
        label_title = QHBoxLayout()
        label_title.setContentsMargins(0, 0, 0, 0)

        laber = QLabel()
        ft = QFont()
        ft.setPointSize(20)
        laber.setFont(ft)
        laber.setText(label_name)
        laber.setScaledContents(True)
        laber.setAlignment(Qt.AlignCenter)
        laber.setStyleSheet('background-color: rgb(192,192,192);')
        laber.adjustSize()
        label_title.addWidget(laber)

        wight.setLayout(label_title)
        return wight

    def ui_art_line_desc_detail(self):
        no_val = self.selected_art_data.get('no', None)
        name_val = self.selected_art_data.get("name", None)


        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(10, 2, 10, 2)

        laber_no = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_no.setFont(ft)
        laber_no.setText("No:")
        laber_no.setFixedWidth(50)
        laber_no.setScaledContents(True)
        laber_no.setAlignment(Qt.AlignVCenter)
        laber_no.adjustSize()
        editor_layout.addWidget(laber_no)

        self.components_art_no_input = QLineEdit()
        self.components_art_no_input.setFixedWidth(50)
        if no_val is not None:
            self.components_art_no_input.setText(str(no_val))
        editor_layout.addWidget(self.components_art_no_input)

        laber_name = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_name.setFont(ft)
        laber_name.setText("Name:")
        laber_name.setMargin(5)
        laber_name.setScaledContents(True)
        laber_name.setAlignment(Qt.AlignVCenter)
        laber_name.adjustSize()
        editor_layout.addWidget(laber_name)

        self.components_art_name_input = QLineEdit()
        if name_val is not None:
            self.components_art_name_input.setText(name_val)
        editor_layout.addWidget(self.components_art_name_input)

        wight.setLayout(editor_layout)
        return wight

    def ui_art_icon_detail(self):
        icon_val = self.selected_art_data.get("i", None)

        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(10, 2, 10, 2)

        laber_icon = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_icon.setFont(ft)
        laber_icon.setText("Icon:")
        laber_icon.setFixedWidth(50)
        laber_icon.setScaledContents(True)
        laber_icon.setAlignment(Qt.AlignVCenter)
        laber_icon.adjustSize()
        editor_layout.addWidget(laber_icon)

        self.components_art_icon_input = QComboBox()
        icons = g_icons
        self.components_art_icon_input.addItems(icons)
        if icon_val is not None:
            self.components_art_icon_input.setCurrentIndex(icons.index(icon_val) if icon_val in icons else 78)
        else:
            self.components_art_icon_input.setCurrentIndex(78)
        editor_layout.addWidget(self.components_art_icon_input)

        wight.setLayout(editor_layout)
        return wight

    def ui_art_color_detail(self):

        color = self.selected_art_data.get('c', "#928179")

        if color in g_text_color:
            color_laber = color
            color = g_text_color[color]
        else:
            color_laber = color

        if color:
            if color[0] != '#':
                color = "#928179"
            if len(color) != 7:
                color = "#928179"
            for char in color[1:]:
                if char not in "0123456789abcdefABCDEF":
                    color = "#928179"
                    break

        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(10, 2, 10, 2)

        laber_color = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_color.setFont(ft)
        laber_color.setText("Color:")
        laber_color.setFixedWidth(50)
        laber_color.setScaledContents(True)
        laber_color.setAlignment(Qt.AlignVCenter)
        laber_color.adjustSize()
        editor_layout.addWidget(laber_color)

        dlg_color = QPushButton('select color')
        dlg_color.clicked.connect(self.action_choose_color)
        self.components_art_color_label = QLabel(color_laber)
        self.components_art_color_label.setAlignment(Qt.AlignCenter)
        self.components_art_color_label.setStyleSheet(f'background-color: {color};')
        editor_layout.addWidget(dlg_color)
        editor_layout.addWidget(self.components_art_color_label)

        wight.setLayout(editor_layout)
        return wight

    def ui_art_group_detail(self):
        group_val = self.selected_art_data.get('g', '1')

        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(10, 2, 10, 2)

        laber_group = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_group.setFont(ft)
        laber_group.setText("Group:")
        laber_group.setFixedWidth(50)
        laber_group.setScaledContents(True)
        laber_group.setAlignment(Qt.AlignVCenter)
        laber_group.adjustSize()
        editor_layout.addWidget(laber_group)

        self.components_art_group_input = QComboBox()
        items = [str(x) for x in range(1, 5)]
        self.components_art_group_input.addItems(items)
        self.components_art_group_input.setCurrentIndex(items.index(str(group_val)) if str(group_val) in items else 0)
        editor_layout.addWidget(self.components_art_group_input)

        wight.setLayout(editor_layout)
        return wight

    def ui_art_add_action(self):
        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(10, 2, 10, 2)

        btn_add_cc = QPushButton('+ CC')
        btn_add_cc.clicked.connect(self.action_add_cc_control)

        btn_add_note = QPushButton('+ Note')
        btn_add_note.clicked.connect(self.action_add_note_control)

        btn_add_note_hold = QPushButton('+ NoteHold')
        btn_add_note_hold.clicked.connect(self.action_add_note_hold_control)

        editor_layout.addWidget(btn_add_cc)
        editor_layout.addWidget(btn_add_note)
        editor_layout.addWidget(btn_add_note_hold)

        wight.setLayout(editor_layout)
        return wight

    def ui_art_cc_control(self, data):
        ch = data.get('channel', 'all')
        cc = data.get('args', "1,127")
        if ',' not in cc:
            cc = "1,127"
        cc_no = cc.split(',')[0]
        cc_val = cc.split(',')[1]

        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(10, 2, 10, 2)

        laber_cc = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_cc.setFont(ft)
        laber_cc.setText("CC:")
        laber_cc.setFixedWidth(50)
        laber_cc.setScaledContents(True)
        laber_cc.setAlignment(Qt.AlignVCenter)
        laber_cc.adjustSize()
        editor_layout.addWidget(laber_cc)

        comb_cc = QComboBox()
        cc_nos = [str(x) for x in range(0, 128)]
        comb_cc.addItems(cc_nos)
        comb_cc.setCurrentIndex(cc_nos.index(cc_no) if cc_no in cc_nos else 1)
        editor_layout.addWidget(comb_cc)

        laber_out = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_out.setFont(ft)
        laber_out.setText("Out:")
        laber_out.setFixedWidth(30)
        laber_out.setScaledContents(True)
        laber_out.setAlignment(Qt.AlignVCenter)
        laber_out.adjustSize()
        editor_layout.addWidget(laber_out)

        cc_out_value = QLineEdit()
        cc_out_value.setText(cc_val)
        editor_layout.addWidget(cc_out_value)

        laber_ch = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_ch.setFont(ft)
        laber_ch.setText("CH:")
        laber_ch.setFixedWidth(30)
        laber_ch.setScaledContents(True)
        laber_ch.setAlignment(Qt.AlignVCenter)
        laber_ch.adjustSize()
        editor_layout.addWidget(laber_ch)

        comb_ch = QComboBox()
        chs = ['all'] + [str(x) for x in range(1, 17)]
        comb_ch.addItems(chs)
        comb_ch.setCurrentIndex(chs.index(ch) if ch in chs else 0)
        comb_ch.setFixedWidth(70)
        editor_layout.addWidget(comb_ch)

        btn_del = QPushButton('X')
        btn_del.setFixedWidth(30)
        btn_del.setContentsMargins(0, 0, 0, 0)
        btn_del.setStyleSheet(f'color: #ff6633;')
        btn_del.clicked.connect(self.action_del_control)
        editor_layout.addWidget(btn_del)

        wight.setLayout(editor_layout)

        self.components_art_control_list.append({
            'type': 'cc',
            'cc_no': comb_cc,
            'cc_val': cc_out_value,
            'ch': comb_ch,
        })

        return wight

    def ui_art_note_control(self, data):

        ch = data.get('channel', 'all')
        note = data.get('args', "1,127")
        if ',' in note:
            note_num = note.split(',')[0]
            note_val = note.split(',')[1]
        else:
            note_num = note.strip()
            note_val = '127'

        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(10, 2, 10, 2)

        laber_note = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_note.setFont(ft)
        laber_note.setText("Note:")
        laber_note.setFixedWidth(50)
        laber_note.setScaledContents(True)
        laber_note.setAlignment(Qt.AlignVCenter)
        laber_note.adjustSize()
        editor_layout.addWidget(laber_note)

        current_note = g_num_note[note_num]
        comb_note = QComboBox()
        notes = list(g_note_num.keys())
        comb_note.addItems(notes)
        comb_note.setCurrentIndex(notes.index(current_note) if current_note in notes else 'C-1')
        editor_layout.addWidget(comb_note)

        laber_out = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_out.setFont(ft)
        laber_out.setText("Vel:")
        laber_out.setFixedWidth(30)
        laber_out.setScaledContents(True)
        laber_out.setAlignment(Qt.AlignVCenter)
        laber_out.adjustSize()
        editor_layout.addWidget(laber_out)

        note_vel_out = QLineEdit()
        note_vel_out.setText(note_val)
        editor_layout.addWidget(note_vel_out)

        laber_ch = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_ch.setFont(ft)
        laber_ch.setText("CH:")
        laber_ch.setFixedWidth(30)
        laber_ch.setScaledContents(True)
        laber_ch.setAlignment(Qt.AlignVCenter)
        laber_ch.adjustSize()
        editor_layout.addWidget(laber_ch)

        comb_ch = QComboBox()
        chs = ['all'] + [str(x) for x in range(1, 17)]
        comb_ch.addItems(chs)
        comb_ch.setCurrentIndex(chs.index(ch) if ch in chs else 0)
        comb_ch.setFixedWidth(70)
        editor_layout.addWidget(comb_ch)

        btn_del = QPushButton('X')
        btn_del.setFixedWidth(30)
        btn_del.setContentsMargins(0, 0, 0, 0)
        btn_del.setStyleSheet(f'color: #ff6633;')
        btn_del.clicked.connect(self.action_del_control)
        editor_layout.addWidget(btn_del)

        wight.setLayout(editor_layout)

        self.components_art_control_list.append({
            'type': 'note',
            'note': comb_note,
            'vel': note_vel_out,
            'ch': comb_ch,
        })

        return wight

    def ui_art_note_hold_control(self, data):

        ch = data.get('channel', 'all')
        note = data.get('args', "1,127")
        if ',' in note:
            note_num = note.split(',')[0]
            note_val = note.split(',')[1]
        else:
            note_num = note.strip()
            note_val = '127'

        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(10, 2, 10, 2)

        laber_note = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_note.setFont(ft)
        laber_note.setText("Note-Hold:")
        laber_note.setFixedWidth(95)
        laber_note.setScaledContents(True)
        laber_note.setAlignment(Qt.AlignVCenter)
        laber_note.adjustSize()
        editor_layout.addWidget(laber_note)

        current_note = g_num_note[note_num]
        comb_note = QComboBox()
        notes = list(g_note_num.keys())
        comb_note.addItems(notes)
        comb_note.setCurrentIndex(notes.index(current_note) if current_note in notes else 'C-1')
        editor_layout.addWidget(comb_note)

        laber_out = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_out.setFont(ft)
        laber_out.setText("Vel:")
        laber_out.setFixedWidth(30)
        laber_out.setScaledContents(True)
        laber_out.setAlignment(Qt.AlignVCenter)
        laber_out.adjustSize()
        editor_layout.addWidget(laber_out)

        note_vel_out = QLineEdit()
        note_vel_out.setText(note_val)
        editor_layout.addWidget(note_vel_out)

        laber_ch = QLabel()
        ft = QFont()
        ft.setPointSize(10)
        laber_ch.setFont(ft)
        laber_ch.setText("CH:")
        laber_ch.setFixedWidth(30)
        laber_ch.setScaledContents(True)
        laber_ch.setAlignment(Qt.AlignVCenter)
        laber_ch.adjustSize()
        editor_layout.addWidget(laber_ch)

        comb_ch = QComboBox()
        chs = ['all'] + [str(x) for x in range(1, 17)]
        comb_ch.addItems(chs)
        comb_ch.setCurrentIndex(chs.index(ch) if ch in chs else 0)
        comb_ch.setFixedWidth(70)
        editor_layout.addWidget(comb_ch)

        btn_del = QPushButton('X')
        btn_del.setFixedWidth(30)
        btn_del.setContentsMargins(0, 0, 0, 0)
        btn_del.setStyleSheet(f'color: #ff6633;')
        btn_del.clicked.connect(self.action_del_control)
        editor_layout.addWidget(btn_del)

        wight.setLayout(editor_layout)

        self.components_art_control_list.append({
            'type': 'note-hold',
            'note': comb_note,
            'vel': note_vel_out,
            'ch': comb_ch,
        })

        return wight

    def ui_editor_bottom(self):

        wight = QWidget()
        wight.adjustSize()
        editor_layout = QHBoxLayout()
        editor_layout.setContentsMargins(0, 0, 0, 0)

        btn1 = QPushButton('Cancel Edit')
        btn1.clicked.connect(self.action_cancel_edit)

        btn2 = QPushButton('Save This Articulation')
        btn2.clicked.connect(self.action_save_articulation)

        editor_layout.addWidget(btn1)
        editor_layout.addWidget(btn2)

        wight.setLayout(editor_layout)
        return wight

    def action_bank_list_item_clicked(self):
        item = self.sender().currentItem()
        self.selected_full_name = item.text(3)
        if self.selected_full_name:
            middle_list = self.ui_middle()
            if hasattr(self, 'middle_list'):
                self.grid_layout.removeWidget(self.middle_list)
            self.grid_layout.addWidget(middle_list, 0, 1)
            self.middle_list = middle_list
        else:
            item.setExpanded(not item.isExpanded())

        self.selected_art_index = None
        self.selected_art_data = {}
        self.clean_selected_components()

        right_editor = self.ui_articulation_editor()
        if hasattr(self, 'right_editor'):
            self.grid_layout.removeWidget(self.right_editor)
        self.grid_layout.addWidget(right_editor, 0, 2)
        self.right_editor = right_editor

    def action_articulation_item_clicked(self):
        item = self.sender().currentItem()
        self.selected_art_index = item.index
        self.selected_art_data = item.data
        self.clean_selected_components()
        if self.selected_full_name and self.selected_art_index is not None:
            right_editor = self.ui_articulation_editor(True)
            if hasattr(self, 'right_editor'):
                self.grid_layout.removeWidget(self.right_editor)
            self.grid_layout.addWidget(right_editor, 0, 2)
            self.right_editor = right_editor

    def action_choose_color(self):
        color = QColorDialog.getColor()
        self.components_art_color_label.setText(color.name())
        self.components_art_color_label.setStyleSheet(f'background-color: {color.name()};')

    def action_add_cc_control(self):
        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_cc_control({})
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

    def action_add_note_control(self):
        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_note_control({})
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

    def action_add_note_hold_control(self):
        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 40))
        widget = self.ui_art_note_hold_control({})
        self.r_listWidget.addItem(item)
        self.r_listWidget.setItemWidget(item, widget)

    def action_del_control(self):
        item = self.sender().parent()
        row = self.r_listWidget.indexAt(item.pos()).row()

        self.r_listWidget.takeItem(row)
        self.components_art_control_list.remove(self.components_art_control_list[row-7])

    def action_cancel_edit(self):
        self.clean_selected_components()
        enable_flg = bool(self.selected_full_name and self.selected_art_index is not None)
        right_editor = self.ui_articulation_editor(enable_flg)
        if hasattr(self, 'right_editor'):
            self.grid_layout.removeWidget(self.right_editor)
        self.grid_layout.addWidget(right_editor, 0, 2)
        self.right_editor = right_editor

    def action_save_articulation(self):
        no = self.components_art_no_input.text()
        name = self.components_art_name_input.text()
        icon = self.components_art_icon_input.currentText()
        color = self.components_art_color_label.text()
        group = self.components_art_group_input.currentText()

        out_event = []
        for item in self.components_art_control_list:
            control = {}
            control_type = item['type']
            if control_type == "cc":
                control['type'] = 'cc'
                control['args'] = f"{item['cc_no'].currentText()},{item['cc_val'].text()}"
                ch = item['ch'].currentText()
                if ch != "all":
                    control["channel"] = ch
            elif control_type == "note":
                control['type'] = 'note'
                note = g_note_num[item['note'].currentText()]
                vel = item['vel'].text()
                control['args'] = f"{note},{vel}"
                ch = item['ch'].currentText()
                if ch != "all":
                    control["channel"] = ch
            elif control_type == "note-hold":
                control['type'] = 'note-hold'
                note = g_note_num[item['note'].currentText()]
                vel = item['vel'].text()
                control['args'] = f"{note},{vel}"
                ch = item['ch'].currentText()
                if ch != "all":
                    control["channel"] = ch
            else:
                pass
            out_event.append(control)

        art_detail = {
            "no": no,
            "name": name,
            "i": icon,
            "c": color,
            "g": group,
            "o": out_event
        }
        self.data[self.selected_full_name]['list'][self.selected_art_index] = art_detail
        self.selected_art_data = self.data[self.selected_full_name]['list'][self.selected_art_index]
        self.clean_selected_components()

        middle_list = self.ui_middle()
        if hasattr(self, 'middle_list'):
            self.grid_layout.removeWidget(self.middle_list)
        self.grid_layout.addWidget(middle_list, 0, 1)
        self.middle_list = middle_list

        right_editor = self.ui_articulation_editor(True)
        if hasattr(self, 'right_editor'):
            self.grid_layout.removeWidget(self.right_editor)
        self.grid_layout.addWidget(right_editor, 0, 2)
        self.right_editor = right_editor

    def action_new_bank(self):
        full_name = self.components_full_name_input.text()
        if full_name in self.data or '/' not in full_name:
            return
        g = "/".join(full_name.split('/')[:-1])
        n = full_name.split('/')[-1]
        next_msb, next_lsb = self.cal_msb_lsb()
        self.data[full_name] = {
            'g': g,
            'n':  n,
            'm': '',
            'bank_name': n,
            'msb': next_msb,
            'lsb': next_lsb,
            'list': []
        }
        self.refresh_all()
        self.selected_full_name = full_name
        self.selected_art_index = None
        self.selected_art_data = {}
        self.clean_selected_components()

        self.bank_tree.setCurrentItem(self.tree_nodes[self.selected_full_name])

        middle_list = self.ui_middle()
        if hasattr(self, 'middle_list'):
            self.grid_layout.removeWidget(self.middle_list)
        self.grid_layout.addWidget(middle_list, 0, 1)
        self.middle_list = middle_list

        right_editor = self.ui_articulation_editor()
        if hasattr(self, 'right_editor'):
            self.grid_layout.removeWidget(self.right_editor)
        self.grid_layout.addWidget(right_editor, 0, 2)
        self.right_editor = right_editor

    def action_del_selected_bank(self):
        if self.selected_full_name in self.data:
            del self.data[self.selected_full_name]
            self.refresh_all()

    def action_new_articulation(self):
        if self.selected_full_name:
            arts = self.data[self.selected_full_name]['list']
            next_no = "127"
            no_used = [x['no'] for x in arts]
            for no in range(1, 128):
                if str(no) not in no_used:
                    next_no = str(no)
                    break

            self.data[self.selected_full_name]['list'].append(
                {
                    "no": next_no,
                    "name": "New Art",
                    "c": '#aaaaaa',
                    'i': "note-eighth",
                    'g': "1",
                    "o": [
                    ]
                }
            )

            self.selected_art_index = len(self.data[self.selected_full_name]['list']) -1
            self.selected_art_data = self.data[self.selected_full_name]['list'][self.selected_art_index]
            self.clean_selected_components()

            middle_list = self.ui_middle()
            if hasattr(self, 'middle_list'):
                self.grid_layout.removeWidget(self.middle_list)
            self.grid_layout.addWidget(middle_list, 0, 1)
            self.middle_list = middle_list

            self.art_list_widget.setCurrentRow(self.selected_art_index)

            right_editor = self.ui_articulation_editor(True)
            if hasattr(self, 'right_editor'):
                self.grid_layout.removeWidget(self.right_editor)
            self.grid_layout.addWidget(right_editor, 0, 2)
            self.right_editor = right_editor

    def action_del_selected_articulation(self):
        if self.selected_full_name and self.selected_art_index is not None:
            del self.data[self.selected_full_name]['list'][self.selected_art_index]

            self.selected_art_index = None
            self.selected_art_data = {}
            self.clean_selected_components()

            middle_list = self.ui_middle()
            if hasattr(self, 'middle_list'):
                self.grid_layout.removeWidget(self.middle_list)
            self.grid_layout.addWidget(middle_list, 0, 1)
            self.middle_list = middle_list

            right_editor = self.ui_articulation_editor(False)
            if hasattr(self, 'right_editor'):
                self.grid_layout.removeWidget(self.right_editor)
            self.grid_layout.addWidget(right_editor, 0, 2)
            self.right_editor = right_editor

    def action_check_data_in_memory(self):
        del_full_names = []
        for full_name, bank_info in self.data.items():
            del_art_indexes = []
            for art_index, art_info in enumerate(bank_info['list']):
                del_control_indexes = []
                for control_index, control_info in enumerate(art_info['o']):

                    if control_info['type'] == "cc":
                        if ',' in control_info['args'] and all(control_info['args'].split(',')):
                            continue
                        else:
                            del_control_indexes.append(control_index)
                    if control_info['type'] == 'note' or control_info['type'] == 'note-hole':

                        pass
                art_info['o'] = [x for x_index, x in enumerate(art_info['o']) if x_index not in del_control_indexes]
                if not all([art_info['no'], art_info['name'], art_info['o']]):
                    del_art_indexes.append(art_index)
            bank_info['list'] = [x for x_index, x in enumerate(bank_info['list']) if x_index not in del_art_indexes]
            if not bank_info['list']:
                del_full_names.append(full_name)

        for del_full_name in del_full_names:
            del self.data[del_full_name]

        self.refresh_all()

    def action_reload_from_file(self):
        self.data = deepcopy(self.ori_data)
        self.refresh_all()

    def action_save_to_file(self):
        self.action_check_data_in_memory()
        FileUtil.save_file(self.data)

    def clean_selected_components(self):
        self.components_art_no_input = None
        self.components_art_name_input = None
        self.components_art_icon_input = None
        self.components_art_color_label = None
        self.components_art_group_input = None
        self.components_art_control_list = []

    def cal_msb_lsb(self):
        msb_range = [str(x) for x in range(64, 128)]
        lsb_range = [str(x) for x in range(1, 128)]
        msb_lsb_used = [(bank['msb'], bank['lsb']) for bank in self.data.values()]
        for msb_lsb in itertools.product(msb_range, lsb_range):
            if msb_lsb not in msb_lsb_used:
                return msb_lsb[0], msb_lsb[1]
        return "127", "127"

    def refresh_all(self):
        self.selected_full_name = ""
        self.selected_art_index = None
        self.selected_art_data = {}
        self.clean_selected_components()
        self.tree_nodes = {}

        left_tree = self.ui_left()
        if hasattr(self, "left_tree"):
            self.grid_layout.removeWidget(self.left_tree)
        self.grid_layout.addWidget(left_tree, 0, 0)
        self.left_tree = left_tree

        middle_list = self.ui_middle()
        if hasattr(self, 'middle_list'):
            self.grid_layout.removeWidget(self.middle_list)
        self.grid_layout.addWidget(middle_list, 0, 1)
        self.middle_list = middle_list

        right_editor = self.ui_articulation_editor(False)
        if hasattr(self, 'right_editor'):
            self.grid_layout.removeWidget(self.right_editor)
        self.grid_layout.addWidget(right_editor, 0, 2)
        self.right_editor = right_editor


def main():
    if Path(reabank_file_path).is_file():
        app = QApplication(sys.argv)
        data = FileUtil.parse_file(reabank_file_path)
        editor = ReaticulateEditor(data=data)
        editor.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
