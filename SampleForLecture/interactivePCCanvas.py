import numpy as np                       # numpyモジュールのimport (npで)
from myCanvas import MyCanvas            # myCanvasモジュールのimport

def norm(v):                             # ベクトルのノルム計算
  '''
  v - ベクトル
  ベクトルの大きさを返す
  '''
  v = np.array(v)                        # numpy.array への変換
  return np.dot(v, v)**0.5               # 内積計算して平方根

class InteractivePCCanvas(MyCanvas):     # InteractivePCCanvasクラスの定義
  def __init__(self, pCurve):            # 初期化メソッド
    '''
    pCurve - 描画に用いる多項式曲線のクラス
    InteractiveBSCanvasオブジェクトを初期化する
    '''
    super().__init__()                   # MyCanvasオブジェクトの初期化
    self.pCurve = pCurve                 # 表示する多項式曲線のクラス
    self.pickid = -1                     # ピックされた点の番号
    self.points = []                     # 制御点のリスト
    self.bind('<Button-1>', self.pressed1) # Button1 pressed コールバックメソッド
    self.bind('<Button-2>', self.pressed2) # Button2 pressed コールバックメソッド
    self.bind('<B2-Motion>', self.dragged2) # Button2 dragged コールバックメソッド
    self.bind('<Shift-Button-1>', self.pressed3)
                                      # Shift+Button1 pressed コールバックメソッド
    #self.bind('<Button-3>', self.pressed3) # Button3 pressed コールバックメソッド
    print('<Usage>')                     # 利用法の表示
    print('Button-1: Add a new control point') # 制御点の追加
    print('Button-2: Pick and drag a control point') # 制御点の移動
    print('Shift-Button-1: Clear all')   # 画面消去

  def pressed1(self, event):             # Button1 pressed コールバックメソッド
    '''
    event - イベントオブジェクト
    Button1がプレスされた位置を記録して曲線を描画する
    '''
    newpnt = self.point(event.x, event.y) # プレスされた座標の点を作成
    self.pickid = -1                     # ピックされた点ではない
    self.points.append(newpnt)           # プレスで作られた点を制御点として追加
    self.clear()                         # canvasのクリア
    self.pCurve(self, self.points).drawCurve() # 多項式曲線の描画

  def pressed2(self, event):             # Button2 pressed コールバックメソッド
    '''
    event - イベントオブジェクト
    Button2がプレスされた位置に近い制御点を選択する
    '''
    newpnt = self.point(event.x, event.y) # プレスされた座標の点を作成
    self.pickid, pickdist = (0, norm(newpnt-self.points[0]))
                                         # ピックされた点と距離の初期化
    for i in range(1, len(self.points)): # 他の制御点との比較
      dist = norm(newpnt-self.points[i]) # 制御点との距離
      if dist < pickdist:                # 距離が小さい場合
        self.pickid, pickdist = (i, dist) # ピックされた点の更新
    if pickdist > self.mr * 5 / self.s:  # 距離がマーカの大きさより大きい場合
      self.pickid = -1                   # ピックされた点ではない

  def dragged2(self, event):             # Button2 dragged コールバックメソッド
    '''
    event - イベントオブジェクト
    Button2がドラッグされた位置に制御点を移動して曲線を描画する
    '''
    if 0 <= self.pickid < len(self.points): # ピックされた点の番号の確認
      self.points[self.pickid] = self.point(event.x, event.y)
                                         # ドラッグされた座標に変更
      self.clear()                       # canvasのクリア
      self.pCurve(self, self.points).drawCurve() # 多項式曲線の描画

  def pressed3(self, event):             # Button3 pressed コールバックメソッド
    '''
    event - イベントオブジェクト
    制御点を初期化して画面をクリアする
    '''
    self.points = []                     # 制御点リストの初期化
    self.clear()                         # canvasのクリア
