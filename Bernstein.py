import numpy as np                       # numpyモジュールのimport (npで)
from myCanvas import MyCanvas            # myCanvasモジュールのimport
from BezierCurve import BezierCurve      # cubicBezierCurveモジュールのimport
from parametricCurve import ParametricCurve # parametricCurveモジュールのimport
import math                              # mathモジュールのimport

def combination(n, i):                   #コンビネーションの計算
  return math.factorial(n)//(math.factorial(n-i)*math.factorial(i))

order = int(input("Input the Bernstein's order -> "))#次元数の入力
NP = order+1                             # n次ベジエ曲線の制御点数

class DrawBernstein(ParametricCurve):

    def __init__(self, canvas, n):
        super().__init__(canvas)
        self.n = n

    def draw(self, ts = 0, te = 1):
        for i in range(self.n):
            super().drawBernstein(i, ts, te)
            print(i)

    def bernsteinfunc(self, n, i, t):      # Bernstein多項式の計算
        """
        Bernstein多項式にパラメータtを代入した値を返す
        """
        return combination(n, i) * t**i * (1-t)**(n-i)

    def evaluate(self, i, t):                 # 曲線上の点座標計算メソッド
        """
        t - パラメタ値
        与えられたパラメタ値に対する点の座標値(ワールド座標系)を返す
        """
        return self.bernsteinfunc(self.n, i, t)

def main():                              # main関数
  global canvas                          # 大域変数 canvas
  canvas = MyCanvas()                    # canvasの作成
  DrawBernstein(canvas, NP).draw()
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出