import sys                               # sysモジュールのimport
import numpy as np                       # numpyモジュールのimport (npで)
from myCanvas import MyCanvas            # myCanvasモジュールのimport
from parametricCurve import ParametricCurve # parametricCurveモジュールのimport

class CubicBezierCurve(ParametricCurve): # CubicBezierCurveクラスの定義
  def __init__(self, canvas, points):    # 初期化メソッド
    '''
    canvas - 描画するcanvas
    points - 制御点のリスト (またはタプル)
    CubicBezierCurveオブジェクトを初期化する
    '''
    super().__init__(canvas)             # ParametricCurveオブジェクトの初期化
    self.points = points                 # 制御点
  def drawCurve(self, ts = 0, te = 1):   # CubicBezierCurveオブジェクトの描画メソッド
    '''
    ts, te - 描画対象のパラメタ値 (開始,終了)，省略時 0, 1
    3次ベジエ曲線と制御多角形を描画する
    '''
    super().drawCurve(ts, te)            # 3次ベジエ曲線の描画
    self.canvas.drawPolyline(self.points, color='blue') # 制御多角形の描画
    for i in range(len(self.points)):    # 制御点の個数だけ反復
      self.canvas.drawMarker(self.points[i], fill='blue') # 制御点の描画
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を返す
    '''
    return     (1-t)**3     * self.points[0] + \
           3 * (1-t)**2 * t * self.points[1] + \
           3 * (1-t) * t**2 * self.points[2] + \
                       t**3 * self.points[3] # 3次ベジエ曲線上の点を返す

def main():                              # main関数
  N = 4                                  # 3次ベジエ曲線の制御点数
  if len(sys.argv) > 2*N:                # シェル引数がある場合
    pnts = sys.argv[1:]                  # 第1引数以降を制御点の文字列
  else:                                  # シェル引数がない場合
    pnts = input('x0 y0 x1 y1 x2 y2 x3 y3 / [] -> ').split(' ')
                                         # 制御点座標値の文字列を入力
    if len(pnts) < 2*N:                  # 文字列入力が省略された場合
      pnts = ['-0.9', '-0.8', '-0.5', '0.8', '0.3', '0.6', '0.8', '-0.9']
                                         # 省略時の値
  points = []                            # 制御点リストの初期化
  for i in range(N):                     # 制御点 4個分の反復
    points.append(np.array((float(pnts[2*i]), float(pnts[2*i+1]))))
                                         # 制御点データ(タプル)を作成してリストに追加
  canvas = MyCanvas()                    # MyCanvasの作成
  CubicBezierCurve(canvas, points).drawCurve() # 3次ベジエ曲線の描画
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出
