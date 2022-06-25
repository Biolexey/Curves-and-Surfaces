import sys                               # sysモジュールのimport
import numpy as np                       # numpyモジュールのimport (npで)
from myCanvas import MyCanvas            # myCanvasモジュールのimport
from parametricCurve import ParametricCurve # parametricCurveモジュールのimport

class PolynomialCurve(ParametricCurve):  # PolynomialCurveクラスの定義
  def __init__(self, canvas, points):    # 初期化メソッド
    '''
    canvas - 描画するcanvas
    points - 制御点のリスト (またはタプル)
    PolynomialCurveオブジェクトを初期化する
    '''
    super().__init__(canvas)             # ParametricCurveオブジェクトの初期化
    self.points = points                 # 制御点
    self.n      = len(points) - 1        # 次数 (制御点数-1)

  def drawPolygon(self):                 # 制御多角形の描画メソッド
    '''
    制御多角形を描画する
    '''
    if len(self.points) > 1:             # 制御点数が2つ以上の場合
      self.canvas.drawPolyline(self.points, color='blue') # 制御多角形の描画
    for i in range(len(self.points)):    # 制御点の個数だけ反復
      self.canvas.drawMarker(self.points[i], fill='blue') # 制御点の描画

  def drawCurve(self, ts, te):           # 曲線と制御多角形の描画メソッド
    '''
    ts, te - 描画対象のパラメタ値 (開始,終了)
    多項式曲線と制御多角形を描画する
    '''
    super().drawCurve(ts, te)            # 曲線の描画
    self.drawPolygon()                   # 制御多角形の描画

def PCMain(PCClass, offset=0):           # PCMain関数
  N = 2                                  # 多項式曲線の最少制御点数 (2個)
  if len(sys.argv) > 2*N+offset:         # シェル引数がある場合
    pnts = sys.argv[(offset+1):]         # 第(offset+1)引数以降を制御点の文字列
  else:                                  # シェル引数がない場合
    pnts = input('x0 y0 x1 y1 ... / [] -> ').split(' ')
                                         # 制御点座標値の文字列を入力
    if len(pnts) < 2*N:                  # 文字列入力が省略された場合
      pnts = ['-0.9', '-0.8', '-0.5', '0.8', '0.3', '0.6', '0.8', '-0.9']
                                         # 省略時の値
  points = []                            # 制御点リストの初期化
  for i in range(len(pnts)//2):          # 制御点数分の反復
    points.append(np.array((float(pnts[2*i]), float(pnts[2*i+1]))))
                                         # 制御点データ(タプル)を作成してリストに追加
  canvas = MyCanvas()                    # MyCanvasの作成
  PCClass(canvas, points).drawCurve()    # 多項式曲線の描画
  canvas.mainloop()                      # ルートフレームの実行ループ開始

