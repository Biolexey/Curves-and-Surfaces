import sys                               # sysモジュールのimport
import numpy as np                       # numpyモジュールのimport (npで)
from myCanvas import MyCanvas            # myCanvasモジュールのimport
from parametricCurve import ParametricCurve # parametricCurveモジュールのimport
import math                              # mathモジュールのimport

def combination(n, i):                   #コンビネーションの計算
  return math.factorial(n)//(math.factorial(n-i)*math.factorial(i))

class BezierCurve(ParametricCurve): # BezierCurveクラスの定義

  def __init__(self, canvas, points, mode):    # 初期化メソッド
    '''
    canvas - 描画するcanvas
    points - 制御点のリスト (またはタプル)
    BezierCurveオブジェクトを初期化する
    '''
    super().__init__(canvas)             # ParametricCurveオブジェクトの初期化
    self.points = points                 # 制御点
    self.n = len(points)-1               # 次元数
    self.mode = mode                     # 計算モード

  def drawCurve(self, ts = 0, te = 1):   # BezierCurveオブジェクトの描画メソッド
    '''
    ts, te - 描画対象のパラメタ値 (開始,終了)，省略時 0, 1
    3次ベジエ曲線と制御多角形を描画する
    '''
    super().drawCurve(ts, te)            # n次ベジエ曲線の描画
    self.canvas.drawPolyline(self.points, color='blue') # 制御多角形の描画
    for i in range(len(self.points)):    # 制御点の個数だけ反復
      self.canvas.drawMarker(self.points[i], fill='blue') # 制御点の描画

  def bernsteinfunc(self, n, i, t):      # Bernstein多項式の計算
    """
    Bernstein多項式にパラメータtを代入した値を返す
    """
    return combination(n, i) * t**i * (1-t)**(n-i)

  def recursive(self, n, t):             # 再帰的にde Casteljau点を求めるメソッド
    if n == 1:                           # 最下層の時に用いるのは与えられた点集合
      pnts = self.points
    else:                                # 途中時点で用いるのは一個下層の点集合
      pnts = self.recursive(n-1, t)
    ret = []
    for i in range(len(pnts)-1):
      ret.append(pnts[i]*(1-t)+pnts[i+1]*t)# tにより内分点を計算し格納
    return ret                           # 計算結果を上層へ返す

  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    """
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を返す
    """
    if self.mode == 1:                   # 再帰的なモデル
      return self.recursive(self.n, t)[0]# n回分の再帰結果を返す

    if self.mode == 2:                   # 反復的なモデル
      prepnts = self.points              # 被計算点を格納
      for _ in range(self.n):            # 指定次元数に達するまで繰り返し       
        postpnts = []                    # 計算結果点リストを初期化
        for i in range(len(prepnts)-1):  # 被計算リストを全走査
          postpnts.append(prepnts[i]*(1-t)+prepnts[i+1]*t)# 計算結果格納
        prepnts = postpnts               # 被計算リストを更新
      return prepnts[0]                  # 最終的な計算結果を返す

    if self.mode == 3:                   # Bernstein多項式を用いるモデル
      ret = sum([self.bernsteinfunc(self.n, i, t)*self.points[i] for i in range(self.n+1)])
      return ret 