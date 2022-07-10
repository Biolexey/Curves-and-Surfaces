import sys                               # sysモジュールのimport
from polynomialCurve import PolynomialCurve
                                         # polynomialCurveモジュールのimport

class BsplineCurve(PolynomialCurve):     # クラスの定義
  def drawCurve(self, ts = 0, te = 1):   # Bsplineオブジェクトの描画メソッド
    '''
    ts, te - 描画対象のパラメタ値 (開始,終了)，省略時 0, 1
    ベジエ曲線と制御多角形を描画する
    '''
    super().drawCurve(ts, te)            # ここではとりあえず描画する。上位クラスで場合分け。
  
class SubdivisionBspline(BsplineCurve):  # ダミークラス
  def evaluate(self, t, j):
    return t