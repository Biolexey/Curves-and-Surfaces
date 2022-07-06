import sys                               # sysモジュールのimport
import numpy as np                       # numpyモジュールのimport (npで)
from polynomialCurve import PolynomialCurve, PCMain
                                         # polynomialCurveモジュールのimport
from interactivePCCanvas import InteractivePCCanvas
                                         # interactivePCCanvasモジュールのimport

class Lagrange(PolynomialCurve):
  def drawCurve(self, ts = 0, te = 1):   # Lagrange補間オブジェクトの描画メソッド
    super().drawCurve(ts, te)            # Lagrange曲線の描画


class Aitken(Lagrange):                  # Aitkenによる描画メソッド
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド

    return self.AitP(len(self.points)-1, t, 0)# Lagrange補間曲線上の点を返す

  def AitP(self, r, t, i):               # 再帰的アルゴリズムの評価メソッド
    if r > 0:                            # 再帰的計算 (次数 > 0)
      return (self.knots[i+r]-t)*self.AitP(r-1, t, i)/(self.knots[i+r]-self.knots[i])\
            +(t-self.knots[i])*self.AitP(r-1, t, i+1)/(self.knots[i+r]-self.knots[i])
    else:                                # 制御点 (次数 = 0)
      return self.points[i]    

class Polynomial(Lagrange):              # Lagrange Polyによる描画メソッド
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    ret = 0
    for i in range(len(self.points)):
      ret += self.points[i]*self.poly(t, i)
    return ret

  def poly(self, t, j):                  # Lagrange Polynomialの評価メソッド
    ret = 1
    for i in range(len(self.knots)):
      if i != j:
        ret *= (t-self.knots[i])/(self.knots[j]-self.knots[i])
    return ret


def main():                              # main関数
  if len(sys.argv) > 1:                  # シェル引数がある場合
    com = sys.argv[1]                    # 第1引数を次数の文字列
  else:                                  # シェル引数がない場合
    com = input('0: Aitken, 1: Lagrange Polynominal -> ')
                                         # Lagrange曲線クラスの文字列を入力
  Classes = [Aitken, Polynomial]         # Lagrange曲線クラスのリスト
  Class = Classes[int(com)%len(Classes)] # 算出クラスの決定
  canvas = InteractivePCCanvas(Class, 1, 1)# canvasの作成
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出
