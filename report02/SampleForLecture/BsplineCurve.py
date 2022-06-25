import sys
from cv2 import detail_BlocksCompensator                               # sysモジュールのimport
import numpy as np
from pandas import describe_option                       # numpyモジュールのimport (npで)
from polynomialCurve import PolynomialCurve
                                         # polynomialCurveモジュールのimport
from basis import N2

class BsplineCurve(PolynomialCurve):     # クラスの定義
  def drawCurve(self, ts = 0, te = 1):   # Bsplineオブジェクトの描画メソッド
    '''
    ts, te - 描画対象のパラメタ値 (開始,終了)，省略時 0, 1
    ベジエ曲線と制御多角形を描画する
    '''
    super().drawCurve(ts, te)            # ここではとりあえず描画する。上位クラスで場合分け。

class BsplinedeBoor(BsplineCurve):
  def evaluate(self, t, j):   
    
    return self.deboor(self.knots, self.order, j+self.order-1, t)

  def deboor(self, knot, r, i, t):
    if r == 0:
      return self.points[i+1]
    else:
      return (knot[i+self.order-r+1]-t)*self.deboor(knot, r-1, i-1, t)/(knot[i+self.order-r+1]-knot[i])\
                         +(t-knot[i])*self.deboor(knot, r-1, i, t)/(knot[i+self.order-r+1]-knot[i])

class Bsplinebasis(BsplineCurve):        # Basis関数による描画メソッド
  def evaluate(self, t, j):   
    ret = 0
    for k in range(self.order+1):
        ret += self.points[j+k]*N2(self.order, self.knots, j+k-1, t)
    return ret