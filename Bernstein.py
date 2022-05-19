import numpy as np                       # numpyモジュールのimport (npで)
from myCanvas import MyCanvas            # myCanvasモジュールのimport
from BezierCurve import BezierCurve      # cubicBezierCurveモジュールのimport
from parametricCurve import ParametricCurve # parametricCurveモジュールのimport
import math                              # mathモジュールのimport

def combination(n, i):                   #コンビネーションの計算
  return math.factorial(n)//(math.factorial(n-i)*math.factorial(i))

order = int(input("Input the Bernstein's order -> "))#次元数の入力

class DrawBernstein(ParametricCurve):    # Bernstein多項式描画クラス

    def __init__(self, canvas, n):       # 初期化メソッド
        super().__init__(canvas)
        self.n = n                       # 次元数

    def draw(self, ts = 0, te = 1):
        for i in range(self.n+1):        # 次元数分関数があるので全て表示
            super().drawBernstein(i, ts, te)
        super().drawBernstein(0, ts, te) # Bernstein多項式プロット関数

    def bernsteinfunc(self, n, i, t):    # Bernstein多項式の計算
        """
        Bernstein多項式にパラメータtを代入した値を返す
        """
        return combination(n, i) * t**i * (1-t)**(n-i)

    def evaluate(self, i, t):            # 曲線上の点座標計算メソッド
        """
        t - パラメタ値
        与えられたパラメタ値に対する点の座標値(ワールド座標系)を返す
        """
        return [t, self.bernsteinfunc(self.n, i, t)]

def main():                              # main関数
  global canvas                          # 大域変数 canvas
  canvas = MyCanvas(xo=0,yo=600,r=1)     # canvasの作成(offsetと拡大率は指定)
  canvas.clear()
  DrawBernstein(canvas, order).draw()    # Bernstein描画クラス内のdrawメソッド呼び出し
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出