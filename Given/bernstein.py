import sys                               # sysモジュールのimport
import math                              # mathモジュールのimport
import numpy as np                       # numpyモジュールのimport (npで)
from myCanvas import MyCanvas            # myCanvasモジュールのimport
from parametricCurve import ParametricCurve # parametricCurveモジュールのimport

def binomial(n, i):                      # 2項係数の関数
  '''
  n, i - 2項係数の引数
  nCi (n choose i) の値を返す
  '''
  return math.factorial(n) / (math.factorial(n-i) * math.factorial(i))
                                         # 2項係数を返す
def bernstein(n, i, t):                  # バーンスタイン多項式関数 (2項係数版)
  '''
  n, i - バーンスタイン多項式の次数と番号
  t    - バーンスタイン多項式のパラメタ
  2項係数を利用して，バーンスタイン多項式 B^n_i(t) の値を計算して返す
  B^n_i(t) = nCi t^i (1-t)^{n-i}
  '''
  return binomial(n, i) * t**i * (1-t)**(n-i) # バーンスタイン多項式の値を返す

class Bernstein(ParametricCurve):        # Bernsteinクラスの定義
  def __init__(self, canvas, n, i):      # 初期化メソッド
    '''
    canvas - 描画するcanvas
    n      - バーンスタイン多項式の次数
    i      - バーンスタイン多項式の番号
    BernsteinFunctionオブジェクトを初期化する
    '''
    super().__init__(canvas)             # ParametricCurveオブジェクトの初期化
    self.n, self.i = (n, i)              # バーンスタイン多項式の次数と番号
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を返す
    '''
    return np.array((2.0*t, 2.0*bernstein(self.n, self.i, t)))
                                       # パラメタ t と バーンスタイン多項式の値の組を返す

def bernsteinRec(n, i, t):               # バーンスタイン多項式関数 (再帰版)
  '''
  n, i - バーンスタイン多項式の次数と番号
  t    - バーンスタイン多項式のパラメタ
  バーンスタイン多項式 B^n_i(t)の値を再帰的に計算して返す
  B^n_i(t) = (1-t) B^{n-1}_i(t) + t B^{n-1}_{i-1}(t)
  '''
  if n > 0 and 0 <= i <=n:               # 再帰の場合
    return (1-t)*bernsteinRec(n-1, i, t) + t*bernsteinRec(n-1, i-1, t)
  elif n == 0 and i == 0:                # 終了の場合
    return 1                             # 1を返す
  else:                                  # 範囲外の場合
    return 0                             # 0を返す

class BernsteinRec(Bernstein):           # BernsteinRecクラスの定義
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を返す
    '''
    return np.array((2.0*t, 2.0*bernsteinRec(self.n, self.i, t)))
                                       # パラメタ t と バーンスタイン多項式の値の組を返す
def bernsteinDP(n, t):                   # バーンスタイン多項式関数 (反復版)
  '''
  n - バーンスタイン多項式の次数
  t - バーンスタイン多項式のパラメタ
  バーンスタイン多項式 B^n_i(t)の値(n+1個)を反復(Dynamic Programming)的に計算して返す
  B^n_i(t) = (1-t) B^{n-1}_i(t) + t B^{n-1}_{i-1}(t)
  '''
  B = np.array([1])                      # 0次バーンスタイン多項式値のnp.array
  for r in range(n):                     # 次数回の反復
    B = (1-t)*np.append(B, [0]) + t*np.append([0], B)
  return B                               # n次バーンスタイン多項式値(n+1個)を返す

class BernsteinDP(Bernstein):            # BernsteinDPクラスの定義
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を返す
    '''
    return np.array((2.0*t, 2.0*(bernsteinDP(self.n, t)[self.i])))
                                       # パラメタ t と バーンスタイン多項式の値の組を返す

def main():                              # main関数
  canvas = MyCanvas(r = 2.4)             # MyCanvasの作成
  offset = np.array((-1.0, -1.0))        # 原点(曲線)を左下にずらす
  canvas.drawPolyline([np.array((-1.2, -1.0)), np.array((1.2, -1.0))],
                      color='blue')      # x軸の描画
  canvas.drawPolyline([np.array((-1.0, -1.2)), np.array((-1.0, 1.2))],
                      color='blue')      # y軸の描画
  if len(sys.argv) > 1:                  # シェル引数がある場合
    com = sys.argv[1]                    # 第1引数を次数の文字列
  else:                                  # シェル引数がない場合
    com = input('Bernstein (0:Binomial, 1:Recursion, 2:Iteration) -> ')
                                         # バーンスタイン多項式クラスの文字列を入力
  Classes = [Bernstein, BernsteinRec, BernsteinDP] # バーンスタイン多項式クラスのリスト
  BernsteinClass = Classes[int(com)%len(Classes)] # 算出クラスの決定
  if len(sys.argv) > 2:                  # シェル引数がある場合
    num = sys.argv[2]                    # 第2引数を次数の文字列
  else:                                  # シェル引数がない場合
    num = input('# of degree -> ')       # 次数の文字列を入力
  n = int(num)                           # 次数
  for i in range(n+1):                   # (次数+1)回の反復
    BernsteinClass(canvas, n, i).drawCurve(0, 1, offset) # バーンスタイン多項式の描画
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出
