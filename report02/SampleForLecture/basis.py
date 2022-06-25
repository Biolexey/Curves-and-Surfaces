import sys                               # sysモジュールのimport
import math                              # mathモジュールのimport
import numpy as np                       # numpyモジュールのimport (npで)
from myCanvas import MyCanvas            # myCanvasモジュールのimport
from parametricCurve import ParametricCurve # parametricCurveモジュールのimport

def N(r, knot, i, u):                    # ノット重複を許容するBasis関数
  if r > 0:
    if knot[i+1] == knot[i+r+1] and knot[i] == knot[i+r]:  
      return 0 

    elif knot[i] == knot[i+r]:  
      return (knot[i+r+1]-u)*N(r-1,knot,i+1,u)/(knot[i+r+1]-knot[i+1])

    elif knot[i+1] == knot[i+r+1]:  
      return (u-knot[i])*N(r-1,knot,i,u)/(knot[i+r]-knot[i])  
        
    else:  
      return (u-knot[i])*N(r-1,knot,i,u)/(knot[i+r]-knot[i])\
            +(knot[i+r+1]-u)*N(r-1,knot,i+1,u)/(knot[i+r+1]-knot[i+1])

  else:
    if knot[i]<=u<knot[i+1]:
      return 1
    else:
      return 0

def N2(r, knot, i, u):                  # ノット重複を許容しないBasis関数
  if r > 0:
    if i<0 and i+r+1>len(knot)-1:
      return 0

    elif i<0:
      return (knot[i+r+1]-u)*N2(r-1,knot,i+1,u)/(knot[i+r+1]-knot[i+1])

    elif i+r+1>len(knot)-1:
      return (u-knot[i])*N2(r-1,knot,i,u)/(knot[i+r]-knot[i])
      
    else:
      return (u-knot[i])*N2(r-1,knot,i,u)/(knot[i+r]-knot[i])\
            +(knot[i+r+1]-u)*N2(r-1,knot,i+1,u)/(knot[i+r+1]-knot[i+1])

  else:
    if knot[i]<=u<knot[i+1]:
      return 1
    else:
      return 0

class Basis(ParametricCurve):            # Basisクラスの定義
  def __init__(self, canvas, n, knot, i):# 初期化メソッド

    super().__init__(canvas)             # ParametricCurveオブジェクトの初期化
    self.n, self.knot, self.i = n, knot, i   

  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を返す
    '''
    return np.array((t, N(self.n, self.knot, self.i, t)))
                                         # パラメタ t と Basis多項式の値の組を返す

def main():                              # main関数
  if len(sys.argv) > 1:                  # シェル引数がある場合
    knot = sys.argv[1]                   # 第1引数を次数の文字列
  else:                                  # シェル引数がない場合
    knot = list(map(int, input('Input the Knot -> ').split()))
  
  if len(sys.argv) > 2:                  # シェル引数がある場合
    num = sys.argv[2]                    # 第2引数を次数の文字列
  else:                                  # シェル引数がない場合
    num = input('# of degree -> ')       # 次数の文字列を入力

  canvas = MyCanvas(r = 5)             # MyCanvasの作成
  offset = np.array((-2, -2))            # 原点(曲線)を左下にずらす
  canvas.drawPolyline([np.array((-2, -2)), np.array((2, -2))],
                      color='blue')      # x軸の描画
  canvas.drawPolyline([np.array((-2, -2)), np.array((-2, 2))],
                      color='blue')      # y軸の描画

  n = int(num)                           # 次数
  for i in range(len(knot)-n-1):         # 反復
    Basis(canvas, n, knot, i).drawCurve(knot[0], knot[-1], offset, nop = 2000) # basis多項式の描画
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出
