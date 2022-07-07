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
  def __init__(self, pCurve, order, mode):            # 初期化メソッド
    '''
    pCurve - 描画に用いる多項式曲線のクラス
    InteractiveBSCanvasオブジェクトを初期化する
    '''
    super().__init__()                   # MyCanvasオブジェクトの初期化
    self.pCurve = pCurve                 # 表示する多項式曲線のクラス
    self.pickid = -1                     # ピックされた点の番号
    self.points = []                     # 制御点のリスト
    self.knots = []                      # ノットのリスト
    self.bind('<Button-1>', self.pressed1) # Button1 pressed コールバックメソッド
    self.bind('<Button-2>', self.pressed2) # Button2 pressed コールバックメソッド
    self.bind('<B2-Motion>', self.dragged2) # Button2 dragged コールバックメソッド
    self.bind("<Button-3>", self.pressed3) # Button3 pressed コールバックメソッド
    self.bind('<Shift-Button-1>', self.pressed4)
                                      # Shift+Button1 pressed コールバックメソッド
    self.num = 0                         # つぎのノットの数字
    self.order = order                   # 次元数
    self.mode = mode                     # 再分割の手法
    #self.bind('<Button-3>', self.pressed3) # Button3 pressed コールバックメソッド
    print('<Usage>')                     # 利用法の表示
    print('Button-1: Add a new control point') # 制御点の追加
    print('Button-2: Pick and drag a control point') # 制御点の移動
    print("Button-3: Make control points TWICE")
    print('Shift-Button-1: Clear all')   # 画面消去

  def pressed1(self, event):             # Button1 pressed コールバックメソッド
    '''
    event - イベントオブジェクト
    Button1がプレスされた位置を記録して曲線を描画する
    '''
    newpnt = self.point(event.x, event.y) # プレスされた座標の点を作成
    self.pickid = -1                     # ピックされた点ではない
    if len(self.points) < 2:
      self.points.append(newpnt)         # プレスで作られた点を制御点として追加
    elif len(self.points) == 2:
      self.points.append(newpnt)
      self.points.append(self.points[0])
    else:
      self.points = self.points[:-1]
      self.points.append(newpnt)
      self.points.append(self.points[0])
    
    if self.num == 0:                    # 最初の点の時にはノットを次元数分だけ追加し、numをorderで初期化
      self.knots = [i for i in range(self.order+1)]
      self.num = self.order+1
    else:                                # それ以外は順次ノットを追加していく
      self.knots.append(self.num)
      self.num += 1
    
    self.clear()                         # canvasのクリア
    self.pCurve(self, self.points, self.order, self.knots).drawCurve(ts=self.knots[0], te=self.knots[-1]) # 多項式曲線の描画

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
      self.pCurve(self, self.points, self.order, self.knots).drawCurve(ts=self.knots[0], te=self.knots[-1]) # 多項式曲線の描画
  
  def pressed3(self, event):             # Button3 pressed コールバックメソッド
    newpoints = []
    if self.mode == 0:                   # 普通の再分割
      if self.order == 1:
        for i in range(len(self.points)-1):
          newpoints.append(self.points[i])
          newpoints.append(0.5*self.points[i] + 0.5*self.points[i+1])
          self.knots.append(self.num)
          self.num += 1
        newpoints.append(newpoints[0])
        self.points = newpoints            # 点を更新
        
      elif self.order == 2:
        for i in range(len(self.points)-1):
          newpoints.append(3*self.points[i]/4 + self.points[i+1]/4)
          newpoints.append(self.points[i]/4 + 3*self.points[i+1]/4)
          self.knots.append(self.num)
          self.num += 1
        newpoints.append(newpoints[0])
        self.points = newpoints            # 点を更新
      
      else:
        for i in range(len(self.points)-1):
          if i == 0:
            newpoints.append(self.points[-2]/8 + 6*self.points[i]/8 + self.points[i+1]/8)
            newpoints.append(self.points[i]/2 + self.points[i+1]/2)
          else:
            newpoints.append(self.points[i-1]/8 + 6*self.points[i]/8 + self.points[i+1]/8)
            newpoints.append(self.points[i]/2 + self.points[i+1]/2)
          self.knots.append(self.num)
          self.num += 1
        newpoints.append(newpoints[0])
        self.points = newpoints            # 点を更新

    else:                                  # 4点スキーマ
      for i in range(len(self.points)-1):
          if i == 0:
            newpoints.append(self.points[i])
            newpoints.append(-self.points[-2]/16 + 9*self.points[i]/16 + 9*self.points[i+1]/16 + -self.points[i+2]/16)
          elif i == len(self.points)-2:
            newpoints.append(self.points[i])
            newpoints.append(-self.points[i-1]/16 + 9*self.points[i]/16 + 9*self.points[i+1]/16 + -self.points[1]/16)
          else:
            newpoints.append(self.points[i])
            newpoints.append(-self.points[i-1]/16 + 9*self.points[i]/16 + 9*self.points[i+1]/16 + -self.points[i+2]/16)
          self.knots.append(self.num)
          self.num += 1
      newpoints.append(newpoints[0])
      self.points = newpoints            # 点を更新

    
    self.clear()                         # canvasのクリア
    self.pCurve(self, self.points, self.order, self.knots).drawCurve(ts=self.knots[0], te=self.knots[-1]) # 多項式曲線の描画
  
  def pressed4(self, event):             # Button3 pressed コールバックメソッド
    '''
    event - イベントオブジェクト
    制御点を初期化して画面をクリアする
    '''
    self.points = []                     # 制御点リストの初期化
    self.knots = []
    self.num = 0
    self.clear()                         # canvasのクリア
