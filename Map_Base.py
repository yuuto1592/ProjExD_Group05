import math
import os
import random
import sys
import time
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # この.pyファイルがあるフォルダをカレントディレクトリにするもの

# ======↓定数定義↓======

WIDTH = 1240  # 横幅(x)
HEIGHT = 680  # 縦幅(y)
FPS = 60  # フレーム数
TILE_SIZE = 55
# 移動範囲制限（ボス戦用）
MARGIN = 10  # ボス専用
MOVE_SPEED = 5  # ボス専用
MAX_LIFE = 20  # 体力数指定, ボス専用
# 動作範囲横幅判定
x_left_outline = WIDTH // 25  # ボス専用
x_right_outline = WIDTH - x_left_outline - 1  # ボス専用
# マップのデータ（シード値）を格納しているもの（0：道、移動可能, 1：障害物、移動不可, 2：敵, 3:ボス, 4:ミニゲーム, 5:罠(踏むごとに30ダメージ)）
SEEDS = [
    [  # 最上段
        [  # マップ番号(0, 0) 左上
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            [1, 1, 0, 2, 1, 1, 5, 5, 5, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(0, 1) 真ん中上
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 0, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(0, 2) 右上
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 5, 5, 5, 2, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 2, 1, 1, 1, 1, 5, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 1, 1, 1, 0, 0, 1, 1],
            [1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 2, 1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    ],
    [  # 中央段
        [  # マップ番号(1, 0) 真ん中左
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
            [1, 0, 0, 1, 1, 1, 2, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 2, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # 初期位置 マップ番号(1, 1) 中心
            [1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(1, 2) 真ん中右
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
            [1, 1, 5, 5, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    ],
    [  # 最下段
        [  # マップ番号(2, 0) 左下
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 5, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 5, 5, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(2, 1) 真ん中下
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
            [0, 0, 2, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 5, 0, 0, 1, 1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(2, 2) 右下
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    ],
]

# 色
# ===↓色定義↓===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CHOCOLATE = (200, 150, 50)
PURPLE = (255, 0, 255)
GRAY = (128, 128, 128) 
MAGENTA = (255, 0, 255)
NAVY = (0, 0, 128)
NEON_PINK = (255, 50, 150)
NEON_RED = (255, 50, 50)
# ===↑色定義↑===

# 敵のステータスデータ（モンスター図鑑のようなもの）
MONSTER_DATA = {
    "スライム": {"max_hp": 40, "atk": 10, "weight": 40}, 
    "ゴブリン": {"max_hp": 60, "atk": 20, "weight": 25},
    "ミミック": {"max_hp": 100, "atk": 30, "weight": 20},
    "ゴーレム": {"max_hp": 400, "atk": 30, "weight": 10},
    "ドラゴン": {"max_hp": 500, "atk": 60, "weight": 5} 
}

# ======↑定数定義↑======


# ===↓class定義↓===

class GameMap:
    """
    マップを作成するもの
    """
    def __init__(self, y_num: int, x_num: int):
        """
        マップを作成し、データを初期化する
        引数：縦の分割数int, 横の分割数int
        y_numはHEIGHTを割り切れる値が好ましい, x_numはWIDTHを割り切れる値が好ましい
        """

        self.x_num = x_num
        self.y_num = y_num
        self.wid = WIDTH // x_num
        self.hei = HEIGHT // y_num
        self.map_data = self._create_map_data()
        self.rocks = pg.sprite.Group()  # 岩のグループ作成
        self.minigame_tiles=pg.sprite.Group() #ミニゲームマス表示用のグループ作成
        self.traps = pg.sprite.Group()  # 罠のグループ作成

    def _create_map_data(self) -> list[list[dict]]:
        """
        二次元リストを作成する隠しメソッド
        戻り値：二次元リストマップデータ（list[[データ]]、アクセスlist[縦][横]["データ"]）
        """

        map_data = []  # 大元の二次元リストになるもの
        for row in range(self.y_num):
            row_lis = []  # そのマスのデータを格納するもの
            for col in range(self.x_num):
                cell_data = {
                    # マスの番号
                    "id": (row, col),
                    # マスの中心座標（オブジェクト用）
                    "coor": (self.wid * col + (self.wid // 2), self.hei * row + (self.hei // 2)),
                    # マスのステータス（0：移動可能, 1：移動不可, 2：敵とのバトルイベント）
                    "type": 0
                }
                row_lis.append(cell_data)
            map_data.append(row_lis)
        return map_data

    def get_cell(self, row: int, col: int) -> dict:
        """
        指定した座標のデータを取得するもの
        引数：縦番号int, 横番号int
        返り値：マスの情報（データ）, マスが存在しない場合None
        """
        if 0 <= col < self.x_num and 0 <= row < self.y_num:
            return self.map_data[row][col]
        return None

    def load_map(self, map_y: int, map_x: int):
        """
        マップを生成するもの
        引数：読み込みたいマップの番号map_y(0, 1, 2), map_x(0, 1, 2)
        """
        self.rocks.empty()  # 前のマップの岩を全て削除
        self.minigame_tiles.empty() #前のマップのミニゲームマスをすべて削除
        self.traps.empty()  # 前のマップの罠を消去
        seed = SEEDS[map_y][map_x]  # 指定された座標のマップのデータを取得
        for row in range(self.y_num):
            for col in range(self.x_num):
                if seed[row][col] == 1:  # 岩のマスか判定
                    rock = Rock(self.map_data[row][col]["coor"])  # 岩を生成
                    self.rocks.add(rock)  # 岩を岩グループに追加
                elif seed[row][col] == 4:
                    minigame_tile = MinigameTile(self.map_data[row][col]["coor"]) #ミニゲームマスの見た目生成
                    self.minigame_tiles.add(minigame_tile)
                elif seed[row][col] == 5:  # 5だったら罠を作る
                    trap = Trap(self.map_data[row][col]["coor"]) #罠生成
                    self.traps.add(trap) #罠を罠グループに追加
                self.map_data[row][col]["type"] = seed[row][col]  # seedに沿ってtypeを上書（マップ形成）

    def check_move(self, row: int, col: int) -> int:
        """
        移動できるのかを判定するもの
        引数：移動先の縦番号int, 移動先の横番号int
        戻り値：移動先のマスの"type"int（0：移動可能, 1：移動不可, 2：敵）
        """
        cell = self.get_cell(row, col)  # 移動先のマスのデータを取得
        if cell is None:
            return 1  # マップ外は壁扱いにする
        return cell["type"]  # 移動先のマスのtypeを返す

    def get_enemy_positions(self) -> list[tuple[int, int]]:
        """
        敵が配置されているマスの中心座標を取得する
        戻り値：敵が配置されているマスの中心座標tupleが格納されたlist
        """
        positions = []  # 敵がいるマスの中心座標を格納するもの
        for row in range(self.y_num):
            for col in range(self.x_num):
                if self.map_data[row][col]["type"] == 2:
                    positions.append(self.map_data[row][col]["coor"])
        return positions
    
    def get_boss_positions(self) -> list[tuple[int, int]]:
        """
        ボスが配置されているマスの中心座標を取得する
        戻り値：ボスが配置されているマスの中心座標tupleが格納されたlist
        """
        positions = []  # 敵がいるマスの中心座標を格納するもの
        for row in range(self.y_num):
            for col in range(self.x_num):
                if self.map_data[row][col]["type"] == 3:
                    positions.append(self.map_data[row][col]["coor"])
        return positions
    
    def get_id(self, x: int, y: int) -> tuple[int, int]:
        """
        座標からマス目idを求めるもの
        引数：オブジェクトの中心のx座標, y座標
        戻り値：tuple(行, 列)
        """
        col = x // self.wid
        row = y // self.hei
        return row, col
    
    def update(self, screen: pg.Surface):
        """
        画面に岩などを描画するもの
        引数：画像Surface
        """
        self.rocks.draw(screen)
        self.minigame_tiles.draw(screen)
        self.traps.draw(screen)


class Rock(pg.sprite.Sprite):
    """
    岩に関するもの
    """

    base_image = None  # クラスが読み込まれた時点ではNone
    
    def __init__(self, coor: tuple[int, int]):
        """
        引数：マスの中心座標tuple(x, y)
        """
        super().__init__()
        # 最初だけ岩を読み込む
        if Rock.base_image is None:
            img = pg.image.load("img/rock.png").convert_alpha()  # 現時点仮の岩画像
            Rock.base_image = pg.transform.scale(img, (95, 110))
        self.image = Rock.base_image
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定


class MinigameTile(pg.sprite.Sprite):
    """
    ミニゲームマスの見た目に関するもの
    """
    def __init__(self,coor:tuple[int,int]):
        """
        引数:マスの中心座標,tuple(x,y)
        """
        super().__init__()
        self.image = pg.image.load("img/mark_exclamation.png")  #イベントマス画像
        self.image = pg.transform.scale(self.image,(52,52))
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定
    

class Enemy(pg.sprite.Sprite):
    """
    敵に関するもの
    """

    def __init__(self, coor: tuple[int, int], name=None):
        """
        引数：マスの中心座標tuple(x, y)
        """
        super().__init__()
        if name is None:
            names = list(MONSTER_DATA.keys())
            weights = [data["weight"] for data in MONSTER_DATA.values()]
            name = random.choices(names, weights=weights, k=1)[0]
        data = MONSTER_DATA[name]
        # 敵ステータス
        self.name = name
        self.max_hp = data["max_hp"]
        self.hp = self.max_hp
        self.atk = data["atk"]
        
        raw_image = pg.image.load(f"img/{self.name}.png").convert_alpha()
        self.battle_image = pg.transform.scale(raw_image, (600, 600)) # 戦闘時の画像サイズの変更
        self.map_image = pg.transform.scale(raw_image, (100, 100)) # 画像サイズの変更

        self.image = self.map_image
        self.rect = self.image.get_rect(center=coor)
        self.original_coor = coor


class Boss(pg.sprite.Sprite):
    """
    ラスボスに関するもの
    """

    def __init__(self, coor: tuple[int, int]):
        """
        引数：マスの中心座標tuple(x, y)
        """
        super().__init__()
        self.image = pg.image.load("img/enemy.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (82, 82))
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定


class Player(pg.sprite.Sprite):
    """
    プレイヤーに関するもの
    """
    def __init__(self, coor: tuple[int, int], game_map: GameMap):
        """
        引数：初期配置の中心座標tuple(x, y), GameMapのインスタンス
        """
        super().__init__()
        self.image = pg.image.load("img/player.png").convert_alpha()  # プレイヤー画像
        self.image = pg.transform.scale(self.image, (52, 52))
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定
        self.game_map = game_map
        self.row, self.col = self.game_map.get_id(coor[0], coor[1])  # プレイヤーのいるマスのidを取得
        # ステータス======
        self.name = "勇者"
        self.max_hp = 200
        self.hp = 200
        self.atk = 30
        #================

    def move(self, move_row: int, move_col: int) -> str | None:
        """
        指定された方向へ1マス移動する(idを参照して移動)
        引数：縦の移動量, 横の移動量
        戻り値：マップ外に出た場合は外に出た方向の文字列、それ以外はNone
        """
        next_row = self.row + move_row
        next_col = self.col + move_col

        # 画面外への移動判定（マップ移動）
        if next_row < 0:
            return "UP"
        if next_row >= self.game_map.y_num:
            return "DOWN"
        if next_col < 0:
            return "LEFT"
        if next_col >= self.game_map.x_num:
            return "RIGHT"
        # 移動先の判定（岩ではない場合）
        if self.game_map.check_move(next_row, next_col) != 1:
            self.row = next_row
            self.col = next_col
            self.rect.center = self.game_map.get_cell(self.row, self.col)["coor"]
        return None
    

class Trap(pg.sprite.Sprite):
    """
    罠に関するもの（見える罠）
    今回は毒
    """
    def __init__(self, coor: tuple[int, int]):
        super().__init__()
        self.image = pg.Surface((30, 30))  # プレイヤーより少し小さめのサイズ
        self.image.fill(PURPLE)            # 紫で見えるようにする
        self.rect = self.image.get_rect(center=coor)


class TileTile(pg.sprite.Sprite):
    def __init__(self, x, y, TILE_SIZE, enemy_img):
        super().__init__()
        self.timer = random.randint(20, 10000)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))  
        self.image.fill(CHOCOLATE)
        self.enemy_img = enemy_img
        self.rect = self.image.get_rect() #タイルの作成
        self.rect.x = x
        self.rect.y = y
        
    def update(self, broke_tiles: pg.sprite.Group):
        """
        引数：壊れたアイルを追加する先のグループ
        """
        self.timer -= 1
        if 0< self.timer <= 1000:
            self.image.fill((200, 150, 50))
        elif self.timer <= 0:
            current_x = self.rect.x
            current_y = self.rect.y
            self.kill() #タイルそれぞれのカウントダウンがゼロになったとき、タイルを消す
            broke_tiles.add(TileBroke_Tile(current_x, current_y, TILE_SIZE, self.enemy_img)) #代わりに触ると死亡するタイルをグループに追加
            

class TileBroke_Tile(pg.sprite.Sprite):
    def __init__(self, x, y, TILE_SIZE, enemy_img):
        super().__init__()
        self.timer = random.randint(20, 5000)
        self.image = pg.transform.scale(enemy_img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TileItem(pg.sprite.Sprite):
    def __init__(self, x, y, TILE_SIZE):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE-10, TILE_SIZE-10))  
        self.image.fill(GREEN)  
        self.rect = self.image.get_rect() #itemの作成
        self.rect.x = x
        self.rect.y = y


class TilePlayer(pg.sprite.Sprite):
    """
    ゲームキャラクターに関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self, xy: tuple[int, int]):
        """
        画像Surfaceを生成する
        引数 xy：画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"img/player.png"), 0, 1.5)
        img = pg.transform.flip(img0, True, False)  # デフォルト
        self.imgs = {
            (+1, 0): img0,  # 右
            (+1, -1): pg.transform.rotozoom(img0, 45, 0.9),  # 右上
            (0, -1): pg.transform.rotozoom(img0, 90, 0.9),  # 上
            (-1, -1): pg.transform.rotozoom(img, -45, 0.9),  # 左上
            (-1, 0): img,  # 左
            (-1, +1): pg.transform.rotozoom(img, 45, 0.9),  # 左下
            (0, +1): pg.transform.rotozoom(img0, -90, 0.9),  # 下
            (+1, +1): pg.transform.rotozoom(img0, -45, 0.9),  # 右下
        }
        self.dire = (+1, 0)
        self.image = self.imgs[self.dire]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 10
        self.state = "normal"  # 追加点
        self.hyper_life = 0  # 追加点

    def change_img(self, screen: pg.Surface):
        """
        画像を切り替え，画面に転送する
        引数 screen：画面Surface
        """
        self.image = pg.transform.rotozoom(pg.image.load(f"img/player.png"), 0, 0.9)
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rect.move_ip(self.speed*sum_mv[0], self.speed*sum_mv[1])
        if check_bound(self.rect) != (True, True):
            self.rect.move_ip(-self.speed*sum_mv[0], -self.speed*sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
        self.image = self.imgs[self.dire]  
        screen.blit(self.image, self.rect)


class TilePoint():
    """
    取らなければいけないポイントと今まで取ったポイントを表示するためのクラス
    """
    def __init__(self):
        self.point = 0
        self.fonto = pg.font.Font(None, 40)

    def update(self, screen:pg.Surface, itemnum:int):
        """
        現在のポイントを取得し、とらなければいけないポイントとともに表示する
        """
        txt = self.fonto.render(str(self.point) + "/" + str(int(itemnum*0.6+1)), True, (0, 0, 0))
        screen.blit(txt, (0, 0))


class BossOutline:
    """
    境界線関係のもの
    ボス戦に使用する
    """
    def __init__(self, x: int):
        """
        引数：outlineのx座標
        """
        self.img = pg.Surface((5, HEIGHT))
        self.img.set_colorkey(BLACK)
        pg.draw.line(self.img, MAGENTA, (5 // 2, 0), (5 // 2, HEIGHT))
        self.rct = self.img.get_rect(center = (x, HEIGHT // 2))
    
    def update(self, screen: pg.Surface):
        """
        境界線を表示するもの
        引数：screen（画面Surface）
        """
        screen.blit(self.img, self.rct)


class BossLife(pg.sprite.Sprite):
    """
    体力関係のもの
    ボス戦に使用する
    """
    # 体力表示座標
    x_player_life = WIDTH // 50  # プレイヤーの体力を表示するx座標
    x_enemy_life = WIDTH - (WIDTH // 50) - 1  # 敵の体力を表示するx座標
    y_step = HEIGHT // MAX_LIFE  # 体力を均等に配置するための縦スペースを計算
    life_coor = []  # 体力を表示する座標を格納するもの
    for i in range(MAX_LIFE):
        life_coor.append([
            [x_player_life, i * y_step + (y_step // 2)],
            [x_enemy_life, i * y_step + (y_step // 2)],
        ])

    def __init__(self, coor: tuple[int, int]):
        """
        引数：敵、味方の座標 tuple[int, int]
        """
        super().__init__()
        self.image = pg.image.load("img/heart.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (32, 32))  # サイズ設定
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定


class BossPlayer(pg.sprite.Sprite):
    """
    プレイヤー関係のもの
    ボス戦に使用する
    """
    MOVE_PLAYER = {
        pg.K_UP : (0, -MOVE_SPEED),
        pg.K_DOWN : (0, +MOVE_SPEED),
        pg.K_LEFT : (-MOVE_SPEED, 0),
        pg.K_RIGHT : (+MOVE_SPEED, 0),
        pg.K_w : (0, -MOVE_SPEED),
        pg.K_s : (0, +MOVE_SPEED),
        pg.K_a : (-MOVE_SPEED, 0),
        pg.K_d : (+MOVE_SPEED, 0),
    }

    def __init__(self, outline_left: pg.Rect, outline_right: pg.Rect):
        """
        引数：左側境界線Rect, 右側境界線Rect
        """
        super().__init__()
        self.image = pg.image.load("img/player.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (32, 32))  # サイズ設定
        self.rect = self.image.get_rect(center = (WIDTH // 4, HEIGHT // 2))
        self.radius = 16  # 当たり判定用半径
        self.outline_left = outline_left
        self.outline_right = outline_right

    def update(self, key_lst: list[bool]):
        """
        プレイヤーの移動座標を更新するもの
        引数：key_list
        """
        next_coor = list(self.rect.center)
        for key, mv in self.MOVE_PLAYER.items():
            if key_lst[key]:
                next_coor[0] += mv[0]
                next_coor[1] += mv[1]
        beside, vertical = boss_check_range(self.outline_left, self.outline_right, next_coor)
        # 移動可能かの判定
        if beside:
            self.rect.centerx = next_coor[0]
        if vertical:
            self.rect.centery = next_coor[1]


class BossEnemy(pg.sprite.Sprite):
    """
    敵関係のもの
    ボス戦に使用する
    """
    MOVE_ENEMY = {
        "up" : (0, -(MOVE_SPEED)),
        "down" : (0, MOVE_SPEED),
    }
    
    def __init__(self, outline_left: pg.Rect, outline_right: pg.Rect):
        """
        引数：左側境界線Rect, 右側境界線Rect
        """
        super().__init__()
        self.image = pg.image.load("img/enemy.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (64, 64))  # サイズ設定
        self.rect = self.image.get_rect(center = ((WIDTH // 4)*3, HEIGHT // 2))  # rect.centerに((WIDTH // 4)*3, HEIGHT // 2)を設定
        self.radius = 32  # 当たり判定用半径
        self.outline_left = outline_left
        self.outline_right = outline_right
        if random.random() <= 0.5:
            self.vy = self.MOVE_ENEMY["down"][1]
        else:
            self.vy = self.MOVE_ENEMY["up"][1]

    def update(self) -> tuple[bool, bool]:
        """
        敵を描画するもの
        戻り値：tuple(bool, bool) (横、縦)
        """
        next_coor = list(self.rect.center)
        next_coor[1] += self.vy
        beside, vertical = boss_check_range(self.outline_left, self.outline_right, next_coor)
        # 画面端で反転
        if vertical:
            self.rect.centery = next_coor[1]
        else:
            self.vy *= -1
        return (beside, vertical)
    

class BossBaseBullet(pg.sprite.Sprite):
    """
    弾幕関係のもの
    ボス戦に使用する
    """
    def __init__(self, rect: pg.Rect, color: tuple):
        """
        引数：発射地Rect, 色
        """
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.image.set_colorkey(BLACK)
        pg.draw.circle(self.image, color, (5, 5), 5)
        self.rect = self.image.get_rect(center = rect.center)  # rect.centerにcoorを設定
        self.radius = 5  # 当たり判定用半径
        # 小数の計算結果をストックする
        self.exact_x = float(self.rect.centerx)
        self.exact_y = float(self.rect.centery)

    def update(self):
        """
        弾の座標更新と、画面外に出た時の削除処理
        """
        # 当たり判定のためにint化
        self.rect.centerx = int(self.exact_x)
        self.rect.centery = int(self.exact_y)
        # 画面外判定
        if not ((self.rect.left >= x_left_outline) and (self.rect.right <= x_right_outline) and (self.rect.top >= -50) and (self.rect.bottom <= HEIGHT + 50)):
            self.kill()


class BossDiffusionBullet(BossBaseBullet):
    """
    拡散する弾幕
    ボス戦に使用する
    """
    def __init__(self, rect: pg.Rect, speed: float, diff_num: int, index: int, color: tuple):
        """
        引数：発射元Rect, 速さ（float）, 個数（int）, 弾の番号（int）, 色
        """
        super().__init__(rect, color)
        degree = (360.0 / diff_num) * index  # 弾ごとの角度を計算
        self.vx = speed * math.cos(math.radians(degree))  # x方向の速度を計算
        self.vy = speed * math.sin(math.radians(degree))  # y方向の速度を計算

    def update(self):
        """
        弾幕の座標の計算をして、親のupdateを呼ぶ
        """
        self.exact_x += self.vx  # x座標に加算
        self.exact_y += self.vy  # y座標に加算
        super().update()


class BossPlayerBullet(BossBaseBullet):
    """
    プレイヤーの弾幕(直線)を生成するもの
    ボス戦に使用する
    """
    def __init__(self, rect: pg.Rect, speed: float):
        """
        引数：プレイヤーRect, 速さ
        """
        super().__init__(rect, NAVY)
        self.vx = speed
        self.vy = 0

    def update(self):
        """
        弾幕の座標の計算をして、親のupdateを呼ぶ
        """
        self.exact_x += self.vx  # x座標に加算
        self.exact_y += self.vy  # y座標に加算
        super().update()


class BossCurveBullet(BossBaseBullet):
    """
    曲がるような弾幕を発射させるもの
    ボス戦に使用する
    """
    def __init__(self, target_rect: pg.Rect, rect: pg.Rect, speed: float, color: tuple):
        """
        引数：プレイヤーRect, 敵Rect, 速さ（float）, 色
        """
        super().__init__(rect, color)
        dx = target_rect.centerx - rect.centerx
        dy = target_rect.centery - rect.centery
        self.base_rad = math.atan2(dy, dx)  # プレイヤー方向への角度を計算
        self.current_speed = speed  # 初期速度
        self.max_speed = speed + 5  # 速度上限
        self.accel = 0.1  # 1フレームあたりの加速度
        if random.random() <= 0.5:
            start_error = 45  # 45度上の誤差
            self.curve_speed = -1  # 毎フレームごとに曲げていく値
        else:
            start_error = -45  # 45度下の誤差
            self.curve_speed = 1  # 毎フレームごとに曲げていく値
        self.rad = self.base_rad + math.radians(start_error)  # 角度に誤差を付ける
        self.vx = self.current_speed * math.cos(self.rad)  # x方向の速度を計算
        self.vy = self.current_speed * math.sin(self.rad)  # y方向の速度を計算

    def update(self):
        """
        弾幕の座標の計算をして、親のupdateを呼ぶ
        """
        if self.current_speed < self.max_speed:  # 速度上限まで毎フレーム加速
            self.current_speed += self.accel
            if self.current_speed > self.max_speed:  # 速度上限を超えたら速度上限に速度を固定
                self.current_speed = self.max_speed
        self.rad += math.radians(self.curve_speed)  # 角度を更新
        self.vx = self.current_speed * math.cos(self.rad)  # x方向の速度の更新
        self.vy = self.current_speed * math.sin(self.rad)  # y方向の速度の更新
        self.exact_x += self.vx  # x座標に加算
        self.exact_y += self.vy  # y座標に加算
        super().update()


class BossLinearBullet(BossBaseBullet):
    """
    ある時点でのプレイヤーの座標を取得して、そこへ弾幕を発射させるもの
    ボス戦に使用する
    """
    def __init__(self, target_rect: pg.Rect, rect: pg.Rect, speed: float, color: tuple):
        """
        引数：プレイヤーRect, 敵Rect, 速さ（float）, 色
        """
        super().__init__(rect, color)
        dx = target_rect.centerx - rect.centerx
        dy = target_rect.centery - rect.centery
        rad = math.atan2(dy, dx)  # プレイヤー方向への角度を計算
        self.vx = speed * math.cos(rad)  # x方向の速度を計算
        self.vy = speed * math.sin(rad)  # y方向の速度を計算

    def update(self):
        """
        弾幕の座標の計算をして、親のupdateを呼ぶ
        """
        self.exact_x += self.vx  # x座標に加算
        self.exact_y += self.vy  # y座標に加算
        super().update()


class BossShotgunBullet(BossBaseBullet):
    """
    散弾（中心で拡散）を発射させるもの
    ボス戦に使用する
    """
    def __init__(self, rect: pg.Rect, speed: float, bullet_group: pg.sprite.Group, color: tuple, snd: pg.mixer.Sound):
        """
        引数：敵Rect, 速さ（float）, 敵の弾幕グループ（pygame.sprite.Group）, 色, 弾の効果音
        """
        super().__init__(rect, color)
        self.snd = snd  # 効果音定義
        self.bullet_group = bullet_group
        self.speed = speed
        self.target_x = WIDTH // 2
        self.target_y = HEIGHT // 2
        dx = self.target_x - rect.centerx
        dy = self.target_y - rect.centery
        self.dis = math.hypot(dx, dy)  # 画面中心までの初期距離を計算
        rad = math.atan2(dy, dx)  # 画面中心への角度を計算
        self.vx = speed * math.cos(rad)  # x方向の速度を計算
        self.vy = speed * math.sin(rad)  # y方向の速度を計算

    def update(self):
        """
        弾幕の座標の計算をして、親のupdateを呼ぶ
        """
        # 現時点の位置と中心までの距離を計算
        dist = math.hypot(self.target_x - self.exact_x, self.target_y - self.exact_y)
        breke_num = dist / self.dis  # 速度の減衰率の計算
        # 中心に達したか判定
        if dist <= self.speed:
            diff_num = 24  # 散弾の数
            # 散弾の発生源となるRectの作成
            shot_rect = pg.Rect(int(self.exact_x), int(self.exact_y), 10, 10)
            for i in range(diff_num):
                diffusion_bullet = BossDiffusionBullet(shot_rect, 4, diff_num, i, BLUE)
                self.bullet_group.add(diffusion_bullet)
            self.kill()  # 大元を削除
            self.snd.play()  # 効果音再生
            return

        self.exact_x += self.vx * breke_num  # x座標に加算
        self.exact_y += self.vy * breke_num  # y座標に加算
        super().update()

    
class BossPreviewBullet(BossBaseBullet):
    """
    予告線に沿って高速で弾幕を発射させるもの
    ボス戦に使用する
    """
    def __init__(self, player_rect: pg.Rect, speed: float, color: tuple, line_snd: pg.mixer.Sound, bullet_snd: pg.mixer.Sound, sound_judge: bool):
        """
        引数：プレイヤーの中心座標, 速さ, 色, 予告線効果音, 弾の効果音, 効果音を発生させるかのフラグ(True:鳴らす、False:鳴らさない)
        """
        self.line_snd = line_snd  # 効果音定義（予告線）
        self.bullet_snd = bullet_snd  # 効果音定義（弾）
        self.sound_judge = sound_judge
        start_x = player_rect[0] + random.randint(-200, 200)  # プレイヤーのx座標を基準に発射位置を決定
        self.start_pos = (start_x, -20)  # 発射位置
        initial_rect = pg.Rect(start_x, -20, 10, 10)  # 親クラス初期化用
        super().__init__(initial_rect, color)
        self.radius = 5  # 当たり判定
        target_pos = (player_rect[0] + random.randint(-200, 200), player_rect[1])  # プレイヤー周辺のランダムな位置を目標にする
        dx = target_pos[0] - self.start_pos[0]
        dy = target_pos[1] - self.start_pos[1]
        dist = math.hypot(dx, dy)  # 目標までの距離を計算
        if dist != 0:
            self.preview_vx = (dx / dist) * speed  # 発射時のx方向の速度を計算
            self.preview_vy = (dy / dist) * speed  # 発射時のy方向の速度を計算
        else:  # 0除算回避
            self.preview_vx, self.preview_vy = 0, speed
        # 画面下部に到達するまでのフレーム数を計算
        if self.preview_vy > 0:
            t_y = (HEIGHT - self.start_pos[1]) / self.preview_vy
        else:
            t_y = float('inf')  # 0除算を防ぐ
        # 画面端に到達するまでのフレーム数を計算
        if self.preview_vx > 0:
            t_x = (x_right_outline - self.start_pos[0]) / self.preview_vx
        elif self.preview_vx < 0:
            t_x = (x_left_outline - self.start_pos[0]) / self.preview_vx
        else:
            t_x = float('inf')  # 0除算を防ぐ

        t = min(t_x, t_y)  # 先に下部、端に到達するものを取得

        self.line_end = (
            self.start_pos[0] + self.preview_vx * t,
            self.start_pos[1] + self.preview_vy * t,
        )
        self.vx = 0
        self.vy = 0
        self.tmr = 0
        self.preview_time = 60  # 発射されるまでの時間（予告線を表示する時間）

    def update(self):
        self.tmr += 1
        # 予告時間を過ぎたら弾を発射させる
        if self.tmr == self.preview_time:
            if self.sound_judge:
                self.bullet_snd.play()  # 効果音再生
            self.vx = self.preview_vx  # x方向の速度を設定
            self.vy = self.preview_vy  # y方向の速度を設定

        # 速度を座標に加算
        self.exact_x += self.vx
        self.exact_y += self.vy
        super().update()
    
    def draw_preview_line(self, screen: pg.Surface):
        """
        予告線を表示させるもの
        引数：screen（画面Surface）
        """
        limit_time = self.preview_time - 20
        # 発射の20フレーム前まで予告線を表示
        if self.tmr < limit_time:
            cycle = limit_time // 3  # 点滅の周期
            # 周期ごとに効果音を発生
            if self.tmr % cycle == 0 and self.sound_judge:
                self.line_snd.play()  # 効果音再生
            # 周期の半分は予告線を表示
            if (self.tmr % cycle) < (cycle // 2):
                pg.draw.line(screen, GRAY, self.start_pos, self.line_end, 1)
        
# ===↑class定義↑===


# ===↓関数定義↓===

def get_japanese_font(size: int) -> pg.font.Font:
    """
    日本語表示に対応したフォントを取得するもの
    （pg.font.Font(None, ...)のデフォルトフォントは日本語グリフを持たないため、システムにインストールされている日本語フォントを探して使う）
    引数：フォントサイズint
    戻り値：pg.font.Fontオブジェクト
    """
    candidates = [
        "Yu Gothic", "Meiryo", "MS Gothic", "MS UI Gothic",  # Windows
        "Hiragino Sans", "Hiragino Kaku Gothic ProN",  # Mac
        "Noto Sans CJK JP", "Noto Sans JP", "IPAGothic", "IPAexGothic", "TakaoGothic",  # Linux
    ]
    for name in candidates:
        font_path = pg.font.match_font(name)
        if font_path:
            return pg.font.Font(font_path, size)
    # どれも見つからなかった場合はデフォルトフォント（日本語は文字化けする可能性あり）
    return pg.font.Font(None, size)


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    タイルゲームで使用
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数：プレイヤーなどのRect
    戻り値：横方向、縦方向のはみ出し判定結果（画面内：True / 画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def tile_game(enemy_img) -> str:
    """
    タイルゲーム
    """
    pg.mixer.music.load("sound/boss_bgm.wav")  # BGM定義
    pg.mixer.music.set_volume(0.3)  # BGM音量調整
    pg.mixer.music.play(loops = -1)  # BGMループ
    linear_bullet_snd = pg.mixer.Sound("sound/boss_linear_bullet.wav")  # 効果音定義
    linear_bullet_snd.set_volume(0.5)  # 音量調整

    # pg.display.set_caption("タイル落下ゲーム")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_img, (0 ,0 ,0), pg.Rect(0, 0, WIDTH, HEIGHT))  #黒い矩形を描画
    
    player = TilePlayer((900, 400))
    point = TilePoint()
    tiles = pg.sprite.Group()
    items = pg.sprite.Group()
    broke_tiles = pg.sprite.Group()
    
    cols = WIDTH // (TILE_SIZE+10)
    rows = HEIGHT//(TILE_SIZE+10)
    itemnum = 0
    finish = 0

    for col in range(cols):
            for row in range(rows+1):
                itemor = random.randint(0, 20)
                tiles.add(TileTile((col*(TILE_SIZE+10))-5, (row*(TILE_SIZE+10))-5, TILE_SIZE, enemy_img)) #画面にタイルを作成
                if itemor == 0:
                    items.add(TileItem((col*(TILE_SIZE+10)), (row*(TILE_SIZE+10)), TILE_SIZE)) #画面にアイテムを作成
                    itemnum += 1

    tmr = 0
    clock = pg.time.Clock()
    
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.mixer.music.stop()
                return "QUIT"
            
        for _ in  pg.sprite.spritecollide(player, broke_tiles, True): #プレイヤーと壊れたタイルが接触したか判定
            player.rect.center = (-10000, -10000)  # 消えたように見せかける
            finish = 1

        for item in pg.sprite.spritecollide(player, items, True): #プレイヤーがitemを取得したか判定
            point.point += 1
            linear_bullet_snd.play()
            item.kill()

        if (point.point/itemnum) > 0.6:
            finish = 2
                
        screen.blit(bg_img, [0, 0])
        screen.fill((30, 30, 30))
        
        tiles.update(broke_tiles)
        tiles.draw(screen)
        broke_tiles.update()
        broke_tiles.draw(screen)
        items.update()
        items.draw(screen)
        point.update(screen, itemnum)
        player.update(key_lst, screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if finish == 1: #gameover判定
            time.sleep(1)
            items.empty()
            broke_tiles.empty()
            tiles.empty()
            pg.mixer.music.stop()
            return "LOSE"
        elif finish == 2:   #クリア判定
            time.sleep(1)
            items.empty()
            broke_tiles.empty()
            tiles.empty()
            pg.mixer.music.stop()
            return "WIN"


def draw_center_text(screen: pg.Surface, font: pg.font.Font, text: str, color: tuple, y_offset: int = 0):
    """
    画面中央（縦方向にy_offsetずらした位置）に文字列を描画するもの
    引数：画面Surface, フォント, 表示文字列, 色tuple, 縦方向のずらし量int
    """
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(surf, rect)


def show_instruction(screen: pg.Surface, clock: pg.time.Clock, title: str, subtitle: str, duration: int = 1200):
    """
    ミニゲーム開始前の「お題」演出を表示するもの（メイドインワリオ風）
    引数：画面Surface, Clock, 大見出し文字列, 補足文字列, 表示時間ミリ秒int
    """
    font_title = get_japanese_font(110)
    font_sub = get_japanese_font(40)
    start_time = pg.time.get_ticks()
    while pg.time.get_ticks() - start_time < duration:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.fill(BLACK)
        draw_center_text(screen, font_title, title, WHITE, -30)
        draw_center_text(screen, font_sub, subtitle, WHITE, 60)
        pg.display.update()
        clock.tick(FPS)


def microgame_mash(screen: pg.Surface, clock: pg.time.Clock) -> bool:
    """
    スペースキーを連打するミニゲーム
    制限時間内に規定回数スペースキーを押せたらクリア
    戻り値：クリアしたかどうかbool
    """
    show_instruction(screen, clock, "連打！", "スペースキーを連打しろ！")

    font_big = get_japanese_font(90)
    font_small = get_japanese_font(40)
    TIME_LIMIT = 3000  # 制限時間（ミリ秒）
    NEED_COUNT = 25  # 必要な連打回数
    count = 0

    start_time = pg.time.get_ticks()
    while True:
        elapsed = pg.time.get_ticks() - start_time
        if elapsed >= TIME_LIMIT or count >= NEED_COUNT:
            break

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                count += 1

        screen.fill(BLACK)
        draw_center_text(screen, font_big, f"{count} / {NEED_COUNT}", WHITE, -60)
        draw_center_text(screen, font_small, f"残り {(TIME_LIMIT - elapsed) / 1000:.1f}秒", WHITE, 60)
        pg.display.update()
        clock.tick(FPS)

    return count >= NEED_COUNT


def microgame_dodge(screen: pg.Surface, clock: pg.time.Clock) -> bool:
    """
    ←→キーで落下してくるブロックを避けるミニゲーム
    制限時間の間ブロックに当たらなければクリア
    戻り値：クリアしたかどうかbool
    """
    show_instruction(screen, clock, "よけろ！", "←→キーでブロックを避けろ！")

    TIME_LIMIT = 9000  # 制限時間（ミリ秒）
    SPEED = 6  # プレイヤーの移動速度
    BLOCK_SPEED = 6  # ブロックの落下速度
    SPAWN_INTERVAL = 50  # ブロック生成間隔（ミリ秒）

    player_rect = pg.Rect(0, 0, 40, 40)
    player_rect.centerx = WIDTH // 2
    player_rect.bottom = HEIGHT - 20
    player_img = pg.image.load("img/player.png").convert_alpha()
    player_img = pg.transform.scale(player_img, (40, 40))
    blocks: list[pg.Rect] = []
    spawn_timer = 0

    start_time = pg.time.get_ticks()
    while pg.time.get_ticks() - start_time < TIME_LIMIT:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # プレイヤー移動
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player_rect.x -= SPEED
        if keys[pg.K_RIGHT]:
            player_rect.x += SPEED
        player_rect.x = max(0, min(WIDTH - player_rect.width, player_rect.x))

        # ブロック生成
        spawn_timer += clock.get_time()
        if spawn_timer >= SPAWN_INTERVAL:
            spawn_timer = 0
            block_x = random.randint(0, WIDTH - 40)
            blocks.append(pg.Rect(block_x, -40, 40, 40))

        # ブロック移動と画面外削除
        for block in blocks:
            block.y += BLOCK_SPEED
        blocks = [block for block in blocks if block.top < HEIGHT]

        # 当たり判定
        hitbox = player_rect.inflate(-10, -10)
        for block in blocks:
            if hitbox.colliderect(block):
                return False  # 当たったら即失敗

        screen.fill(BLACK)
        screen.blit(player_img, player_rect)
        for block in blocks:
            pg.draw.rect(screen, RED, block)
        pg.display.update()
        clock.tick(FPS)

    return True  # 制限時間を耐えきったらクリア


def show_result(screen: pg.Surface, clock: pg.time.Clock, is_clear: bool, duration: int = 1000):
    """
    ミニゲーム終了後の「CLEAR!/MISS...」演出を表示するもの
    引数：画面Surface, Clock, クリアしたかbool, 表示時間ミリ秒int
    """
    font = get_japanese_font(100)
    text = "CLEAR!" if is_clear else "MISS..."
    color = GREEN if is_clear else RED
    start_time = pg.time.get_ticks()
    while pg.time.get_ticks() - start_time < duration:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.fill(BLACK)
        draw_center_text(screen, font, text, color)
        pg.display.update()
        clock.tick(FPS)


def run_minigame(screen: pg.Surface, clock: pg.time.Clock) -> bool:
    """
    MINIGAMESからランダムに1つ選んで実行し、結果演出まで行うもの
    引数：画面Surface, Clock
    戻り値：クリアしたかどうかbool
    """
    MINIGAMES = [microgame_mash, microgame_dodge]  # ミニゲーム一覧（増やす場合はここに追加）
    game_func = random.choice(MINIGAMES)
    is_clear = game_func(screen, clock)
    show_result(screen, clock, is_clear)
    return is_clear


def boss_check_range(outline_left_rct: pg.Rect, outline_right_rct: pg.Rect, coor: list) -> tuple[bool, bool]:
    """
    移動範囲制限関数
    ボス戦に使用する
    引数：左側境界線Rect, 右側境界線Rect, 座標list[x, y]
    戻り値：判定結果タプル（横判定結果, 縦判定結果）
    True：範囲内 / False：範囲外
    """
    beside, vertical = True, True
    if (outline_right_rct.left - MARGIN < coor[0]) or (outline_left_rct.right + MARGIN > coor[0]):  # 横判定
        beside = False
    if (MARGIN > coor[1]) or (HEIGHT - MARGIN < coor[1]):  # 縦判定
        vertical = False
    return (beside, vertical)


# ボス戦（弾幕ゲー）用関数
def lastbattle(screen: pg.Surface, clock: pg.time.Clock, player_life: int) -> bool | str:
    """
    ボス戦の弾幕ゲーを処理する関数
    引数：画像Surface, pg.time.Clock, プレイヤーの体力
    戻り値：True, 終了ならstr（QUIT）
    """
    bg_image = pg.image.load("img/boss_back.png").convert_alpha()  # 背景画像
    boss_bg = pg.transform.scale(bg_image, (WIDTH, HEIGHT))  # 背景画像を画面サイズに合わせる
    pg.mixer.music.load("sound/boss_bgm.wav")  # BGM定義
    pg.mixer.music.set_volume(0.3)  # BGM音量調整
    pg.mixer.music.play(loops = -1)  # BGMループ
    linear_bullet_snd = pg.mixer.Sound("sound/boss_linear_bullet.wav")  # 効果音定義
    linear_bullet_snd.set_volume(0.5)  # 音量調整
    curve_bullet_snd = pg.mixer.Sound("sound/boss_curve_bullet.wav")  # 効果音定義
    curve_bullet_snd.set_volume(0.7)  # 音量調整
    diffusion_bullet_snd = pg.mixer.Sound("sound/boss_diffusion_bullet.wav")  # 効果音定義
    shotgun_bullet_snd = pg.mixer.Sound("sound/boss_shotgun_bullet.wav")  # 効果音定義
    shotgun_bullet_snd.set_volume(0.7)  # 音量調整
    player_bullet_snd = pg.mixer.Sound("sound/boss_player_bullet.wav")  # 効果音定義
    player_bullet_snd.set_volume(0.5)  # 音量調整
    preview_line_snd = pg.mixer.Sound("sound/boss_linear_bullet.wav")  # 効果音定義（予告線）
    preview_bullet_snd = pg.mixer.Sound("sound/boss_preview_bullet.wav")  # 効果音定義
    outline_left = BossOutline(x_left_outline)  # 左側境界線
    outline_right = BossOutline(x_right_outline)  # 右側境界線
    # 敵
    enemy = pg.sprite.GroupSingle()
    enemy.add(BossEnemy(outline_left.rct, outline_right.rct))
    # プレイヤー
    player = pg.sprite.GroupSingle()
    player.add(BossPlayer(outline_left.rct, outline_right.rct))
    enemy_bullets = pg.sprite.Group()  # 弾幕描画(敵)
    player_bullets = pg.sprite.Group()  # 弾幕描画(プレイヤー)
    # 体力描画
    player_lifes = pg.sprite.Group()  # プレイヤーの体力用Group
    enemy_lifes = pg.sprite.Group()  # 敵の体力用Group
    # 変数定義
    for coors in BossLife.life_coor:
        player_lifes.add(BossLife(coors[0]))
        enemy_lifes.add(BossLife(coors[1]))
    tmr = 0  # 1フレームごとのカウント
    # 体力調整
    for _ in range(MAX_LIFE - max(1, int(player_life // 10))):
        player_lifes.sprites()[0].kill()
    span = 0  # 弾のスパン
    mag = 1  # 弾の数増加用
    # bool型定義(判定)
    space_judge = False  # プレイヤーの攻撃フラグ

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "QUIT"

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    space_judge = True  # プレイヤーの攻撃判定

        screen.blit(boss_bg, (0, 0))
        outline_left.update(screen)
        outline_right.update(screen)
        # プレイヤー移動処理
        Key_lst = pg.key.get_pressed()
        player.update(Key_lst)
        player_rct = player.sprite.rect  # プレイヤーのRectを取得
        player.draw(screen)
        # 敵移動処理
        bound_check = enemy.sprite.update()  # 戻り値があるため格納(未使用)
        enemy_rct = enemy.sprite.rect  # 敵のRectを取得
        enemy.draw(screen)
        # 弾処理(プレイヤー)
        if space_judge:  # プレイヤーがスペースを押したら攻撃弾を発射
            player_bullet = BossPlayerBullet(player_rct, 10)
            player_bullets.add(player_bullet)
            player_bullet_snd.play()  # 効果音再生
            space_judge = False  # 連続での発射を防ぐ
        player_bullets.update()
        # 弾処理(敵)
        # 予告弾
        if tmr % 360 == 0:
            for i in range(8):
                sound_judge = (i == 0)  # 最初だけ効果音を鳴らす
                preview_bullet = BossPreviewBullet(player_rct.center, 50, RED, preview_line_snd, preview_bullet_snd, sound_judge)
                enemy_bullets.add(preview_bullet)
        # 散弾
        if tmr % 300 == 0:
            shotgun_bullet = BossShotgunBullet(enemy_rct, 5, enemy_bullets, BLUE, shotgun_bullet_snd)
            enemy_bullets.add(shotgun_bullet)
        # 拡散弾
        if tmr % (120 - span) == 0:
            diff_num_lis = [14, 16, 18, 20]  # 拡散弾の数の候補
            diff_num = random.choice(diff_num_lis)  # 拡散弾の数（毎回ランダム）
            for i in range(diff_num * mag):
                diffusion_bullet = BossDiffusionBullet(enemy_rct, 3, diff_num * mag, i, GOLD)
                enemy_bullets.add(diffusion_bullet)
            diffusion_bullet_snd.play()  # 効果音再生
        # 直線弾
        if tmr % (90 - span) in [0, 5, 10]:  # 三連で発射
            linear_bullet = BossLinearBullet(player_rct, enemy_rct, 4, NEON_RED)
            linear_bullet_snd.play()  # 効果音再生
            enemy_bullets.add(linear_bullet)
        # 曲線弾
        if tmr % (60 - span) in [3, 8, 13]:  # 三連で発射
            curve_bullet = BossCurveBullet(player_rct, enemy_rct, 6, NEON_PINK)
            curve_bullet_snd.play()  # 効果音再生
            enemy_bullets.add(curve_bullet)
        enemy_bullets.update()
        player_bullets.draw(screen)
        enemy_bullets.draw(screen)
        for bullet in enemy_bullets.sprites():
            if hasattr(bullet, "draw_preview_line"):  # もしbulletが"draw_preview_line"を持っていれば予告線を表示する
                bullet.draw_preview_line(screen)
        # ダメージ処理(プレイヤー)
        if pg.sprite.spritecollide(player.sprite, enemy_bullets, True, pg.sprite.collide_circle):  # 円での当たり判定
            if len(player_lifes) > 0:
                player_lifes.sprites()[0].kill()
            if len(player_lifes) == 0:  # 負け
                pg.mixer.music.stop()  # BGMストップ
                game_over(screen)  # ゲームオーバー画面表示
                break
        # ダメージ処理(敵)
        if pg.sprite.spritecollide(enemy.sprite, player_bullets, True, pg.sprite.collide_circle):  # 円での当たり判定
            if len(enemy_lifes) > 0:
                enemy_lifes.sprites()[0].kill()
                if len(enemy_lifes) <= (MAX_LIFE // 4):
                    span = 30  # 第四段階（弾の感覚が狭まる）
                elif len(enemy_lifes) <= (MAX_LIFE // 2):
                    mag = 2 # 第三段階（弾の数が増える）
                elif len(enemy_lifes) <= (MAX_LIFE // 4)*3:
                    span = 15  # 第二段階（弾の感覚が狭まる）
            if len(enemy_lifes) == 0:  # 勝ち
                pg.mixer.music.stop()  # BGMストップ
                game_clear(screen)  # ゲームクリア画面表示
                break
        # 体力処理
        player_lifes.draw(screen)
        enemy_lifes.draw(screen)

        pg.display.update()
        tmr += 1
        clock.tick(FPS)
    return True


def game_over(screen: pg.Surface):
    """
    GAMEOVER画面を表示するもの
    引数：画像Surface
    """
    snd = pg.mixer.Sound("sound/gameover.wav")  # 効果音定義（GAME OVER音）
    fonto = pg.font.Font(None, 100)
    txt = fonto.render("GAME OVER", True, RED)
    txt_rect = txt.get_rect(center = (WIDTH // 2, HEIGHT // 2))  # テキストを画面の中央に配置
    screen.fill(BLACK)
    screen.blit(txt, txt_rect)
    snd.play()  # 効果音再生
    pg.display.update()
    pg.time.wait(2000)


def game_clear(screen: pg.Surface):
    """
    GAMECLEAR画面を表示するもの
    引数：画像Surface
    """
    snd = pg.mixer.Sound("sound/gameclear.wav")  # 効果音定義（GAME CLEAR音）
    fonto = pg.font.Font(None, 100)
    txt = fonto.render("GAME CLEAR", True, GOLD)
    txt_rect = txt.get_rect(center = (WIDTH // 2, HEIGHT // 2))  # テキストを画面の中央に配置
    screen.fill(BLUE)
    screen.blit(txt, txt_rect)
    snd.play()  # 効果音再生
    pg.display.update()
    pg.time.wait(2000)

# ===↑関数定義↑===


def main():
    pg.display.set_caption("ごちゃまぜRPG")

    # ===↓変数定義↓===
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    fonto = pg.font.SysFont(None, 40)
    bg_image = pg.image.load("img/back1.png").convert_alpha()  # 背景画像
    map_background = pg.transform.scale(bg_image, (WIDTH, HEIGHT))  # 背景画像を画面サイズに合わせる
    game_map = GameMap(10, 20)  # マップ作成 
    current_map_x = 1  # マップ初期x座標 
    current_map_y = 1  # マップ初期y座標 
    # マップ番号(1, 1) 中心
    game_map.load_map(current_map_y, current_map_x)  # マップロード
    move_snd = pg.mixer.Sound("sound/move.wav")  # 効果音定義
    move_snd.set_volume(0.1)  # 音量調整
    trap_snd = pg.mixer.Sound("sound/trap_damage.wav")  # 効果音定義
    enemys = pg.sprite.Group()  # 敵のグループ作成
    bossgp = pg.sprite.Group()
    # 敵の座標読み込み
    for coor in game_map.get_enemy_positions():
        enemys.add(Enemy(coor))
    # ボスの座標読み込み
    for coor in game_map.get_boss_positions():
        bossgp.add(Boss(coor))
    start_coor = game_map.get_cell(5, 10)["coor"]  # 初期位置
    player = Player(start_coor, game_map)  # プレイヤー定義
    players = pg.sprite.GroupSingle(player)  # プレイヤー用グループ（単体）
    game_state = "MAP"
    battle_phase = "COMMAND"
    battle_message = ""
    next_turn = "PLAYER"
    battle_cursor = 0
    current_enemy = None
    font = pg.font.SysFont("msgothic", 40)
    damage_tmr = 0 # ダメージを表示するタイマー
    last_buttle_judge = False  # ボス戦を終了したかの判定
    enemy_event_judge = False  # イベントの連続発生を防ぐ判定（敵）
    minigame_event_judge = False  # イベントの連続発生を防ぐ判定（ミニゲーム）
    # ===↑変数定義↑===

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return # 終了判定

            # プレイヤー移動処理
            if game_state == "MAP":
                if event.type == pg.KEYDOWN:
                    move: str | None = None  # マップ移動の詳細を格納する変数
                    if event.key == pg.K_UP:
                        move = player.move(-1, 0)
                        move_snd.play()
                    elif event.key == pg.K_DOWN:
                        move = player.move(1, 0)
                        move_snd.play()
                    elif event.key == pg.K_LEFT:
                        move = player.move(0, -1)
                        move_snd.play()
                    elif event.key == pg.K_RIGHT:
                        move = player.move(0, 1)
                        move_snd.play()
                    # マップ移動処理
                    if move:
                        if move == "UP" and current_map_y > 0:
                            current_map_y -= 1
                            player.row = game_map.y_num - 1  # 下端
                        elif move == "DOWN" and current_map_y < 2:
                            current_map_y += 1
                            player.row = 0  # 上端
                        elif move == "LEFT" and current_map_x > 0:
                            current_map_x -= 1
                            player.col = game_map.x_num - 1  # 右端
                        elif move == "RIGHT" and current_map_x < 2:
                            current_map_x += 1
                            player.col = 0  # 左端
                        else:
                            continue
                        # 新しいマップをロード
                        game_map.load_map(current_map_y, current_map_x)
                        enemys.empty()  # 移動前のマップに表示されている敵を削除
                        bossgp.empty()  # 移動前のマップに表示されているボスを削除
                        # 敵の座標読み込み
                        for coor in game_map.get_enemy_positions():
                            enemys.add(Enemy(coor))
                        # ボスの座標読み込み
                        for coor in game_map.get_boss_positions():
                            bossgp.add(Boss(coor))
                        # プレイヤーを更新
                        player.rect.center = game_map.get_cell(player.row, player.col)["coor"]
                    if game_map.check_move(player.row, player.col) == 2:  # 移動した先が敵かの判定
                        if not enemy_event_judge:  # 連続発生を防ぐ
                            enemy_event_judge = True
                            # 現在戦う敵を取得
                            current_enemy = pg.sprite.spritecollideany(player, enemys)
                            if current_enemy:
                                if random.random() <= 0.5:
                                    # ここにバトルイベントなどを追加
                                    game_state = "BATTLE"
                                    battle_phase = "COMMAND"
                                    current_enemy.image = current_enemy.battle_image
                                    current_enemy.rect = current_enemy.image.get_rect(center=(640, 300))
                                else:
                                    result = tile_game(current_enemy.image)
                                    if result == "QUIT":  # ゲーム終了
                                        return
                                    elif result == "WIN":
                                        row, col = game_map.get_id(current_enemy.original_coor[0], current_enemy.original_coor[1])
                                        game_map.map_data[row][col]["type"] = 0  # 敵を倒したのでマスのtypeを0に変更
                                        current_enemy.kill()
                    else:  # 敵から離れたら再度敵と戦えるように
                        enemy_event_judge = False
                    if game_map.check_move(player.row, player.col) == 3:
                        last_buttle_judge = lastbattle(screen, clock, player.hp)  # 戦いを終えていたらしたらTrue（終了したらQUIT）
                        if last_buttle_judge == "QUIT":
                            return
                    if game_map.check_move(player.row, player.col) == 4:
                        if not minigame_event_judge:  # 連続発生を防ぐ
                            minigame_event_judge = True
                            if run_minigame(screen,clock) == True:
                                if player.hp <= 200:
                                    player.hp = 200
                    else:
                        minigame_event_judge = False
                    if game_map.check_move(player.row, player.col) == 5:
                            player.hp -= 30
                            damage_tmr = 60  # ダメージを表示するタイマー
                            trap_snd.play()
            elif game_state == "BATTLE":
                if event.type == pg.KEYDOWN:
                    # 1. コマンド選択フェーズ
                    if battle_phase == "COMMAND":
                        if event.key == pg.K_UP: battle_cursor = 0
                        elif event.key == pg.K_DOWN: battle_cursor = 1
                        elif event.key == pg.K_RETURN:
                            if battle_cursor == 0: # たたかう
                                current_enemy.image = current_enemy.battle_image
                                current_enemy.rect = current_enemy.image.get_rect(center=(640, 300))
                                # プレイヤー攻撃計算
                                is_crit = random.random() < 0.08
                                dmg = int(player.atk * random.uniform(0.9, 1.1) * (1.5 if is_crit else 1.0))
                                current_enemy.hp = max(0, current_enemy.hp - dmg)
                                battle_message = f"クリティカル！" if is_crit else f"{player.name}の攻撃！"
                                battle_message += f" {dmg}のダメージ！"
                                battle_phase = "MESSAGE"
                                next_turn = "WIN" if current_enemy.hp <= 0 else "ENEMY"
                            else: # にげる
                                battle_message = "無事に逃げ切った！"
                                battle_phase = "MESSAGE"
                                next_turn = "ESCAPE"

                    # 2. メッセージ送りフェーズ
                    elif battle_phase == "MESSAGE":
                        if event.key == pg.K_RETURN:
                            if next_turn == "ENEMY":
                                # 敵の攻撃計算
                                is_crit = random.random() < 0.08
                                dmg = int(current_enemy.atk * random.uniform(0.9, 1.1) * (1.5 if is_crit else 1.0))
                                player.hp = max(0, player.hp - dmg)
                                battle_message = f"クリティカル！" if is_crit else f"{current_enemy.name}の攻撃！"
                                battle_message += f" {dmg}のダメージ！"
                                next_turn = "LOSE" if player.hp <= 0 else "PLAYER"
                            elif next_turn == "PLAYER":
                                battle_phase = "COMMAND"
                            elif next_turn == "WIN":
                                row, col = game_map.get_id(current_enemy.original_coor[0], current_enemy.original_coor[1])
                                game_map.map_data[row][col]["type"] = 0  # 敵を倒したのでマスのtypeを0に変更
                                game_state = "MAP"
                                current_enemy.kill()
                            elif next_turn == "ESCAPE":
                                current_enemy.image = current_enemy.map_image
                                current_enemy.rect = current_enemy.image.get_rect(center=current_enemy.original_coor)
                                game_state = "MAP"
                            elif next_turn == "LOSE":
                                break

        # --- 描画処理 ---
        screen.fill(BLACK if game_state == "BATTLE" else WHITE) # バトル中は黒背景に
        if player.hp <= 0:
            game_over(screen)
            break
        # ボス戦を終えていたら終了
        if last_buttle_judge:
            break

        if game_state == "MAP":
            screen.blit(map_background, (0, 0))
            game_map.update(screen)  # 岩を描画
            enemys.draw(screen)  # 敵を描画
            bossgp.draw(screen)  # ボスを描画
            players.draw(screen)  # プレイヤーを描画
            if damage_tmr > 0:  # ダメージを表示
                damage_txt = fonto.render("-30", True, RED)
                screen.blit(damage_txt, (player.rect.right, player.rect.top - 20))
                damage_tmr -= 1
            hp_txt = fonto.render(f"HP: {player.hp}", True, RED)
            screen.blit(hp_txt, (10, 10))
        elif game_state == "BATTLE":
            # バトルUIの描画
            if current_enemy:
                screen.blit(current_enemy.image, current_enemy.rect)
            
            if current_enemy:
                enemy_name_txt = font.render(f"{current_enemy.name}", True, WHITE)
                enemy_hp_txt = font.render(f"HP: {current_enemy.hp}/{current_enemy.max_hp}", True, WHITE)
                screen.blit(enemy_name_txt, (800, 100))
                screen.blit(enemy_hp_txt, (800, 150))

            # プレイヤーの情報を表示
            pg.draw.rect(screen, WHITE, (50, 500, 1140, 150), 3)
            player_hp_txt = font.render(f"{player.name} HP: {player.hp}/{player.max_hp}", True, WHITE)
            screen.blit(player_hp_txt, (100, 520))
            
            if battle_phase == "COMMAND":
                screen.blit(font.render("たたかう", True, WHITE), (800, 520))
                screen.blit(font.render("にげる", True, WHITE), (800, 580))
                # カーソル
                y = 520 if battle_cursor == 0 else 580
                pg.draw.polygon(screen, WHITE, [(750, y), (750, y+30), (780, y+15)])
            elif battle_phase == "MESSAGE":
                # メッセージの描画
                msg_txt = font.render(battle_message, True, WHITE)
                screen.blit(msg_txt, (100, 580))
                # メッセージ送り案内
                guide_txt = font.render("Press Enter", True, (200, 200, 200))
                screen.blit(guide_txt, (1000, 630))

        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()