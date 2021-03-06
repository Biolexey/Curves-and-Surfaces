import sys                               # sysモジュールのimport
import numpy as np                       # numpyモジュールのimport (npで)
from bernstein import bernstein, bernsteinRec, bernsteinDP
                                         # bernsteinモジュールのimport
from polynomialCurve import PolynomialCurve, PCMain
                                         # polynomialCurveモジュールのimport

class DeCasteljauCurve(PolynomialCurve): # DeCasteljauCurveクラスの定義
  def drawCurve(self, ts = 0, te = 1):   # DeCasteljauCurveオブジェクトの描画メソッド
    '''
    ts, te - 描画対象のパラメタ値 (開始,終了)，省略時 0, 1
    ベジエ曲線と制御多角形を描画する
    '''
    super().drawCurve(ts, te)            # ベジエ曲線の描画
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を
    de Cateljauアルゴリズムを再帰的に計算して返す
    '''
    return self.recursion(self.n, 0, t)  # ベジエ曲線上の点を返す
  def recursion(self, r, i, t):          # de Casteljau アルゴリズムの評価メソッド
    '''
    r - 次数
    i - 番号
    t - パラメタ値
    再帰的な評価を行い，de Casteljau 点を返す
    '''
    if r > 0:                            # 再帰的計算 (次数 > 0)
      return (1 - t)*self.recursion(r-1, i, t) + t*self.recursion(r-1, i+1, t)
    else:                                # 制御点 (次数 = 0)
      return self.points[i]

class DeCasteljauDPCurve(DeCasteljauCurve): # DeCasteljauDPCurveクラスの定義
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を
    de Cateljauアルゴリズムを反復(Dynamic Programming)的に計算して返す
    '''
    pnt = np.array(self.points)          # 制御点のコピー
    for r in range(self.n):              # 次数回の反復
      pnt = (1-t)*pnt[:-1] + t*pnt[1:]   # r次の点リスト (1つ少ない)
    return pnt[0]                        # ベジエ曲線上の点を返す

class BernsteinCurve(DeCasteljauCurve):  # BernsteinCurveクラスの定義
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を
    berstein関数によるバーンスタイン関数値で計算して返す
    '''
    B = np.array([bernstein(self.n, i, t) for i in range(self.n+1)])
                                         # n次バーンスタイン多項式値のnp.array
    return B.dot(np.array(self.points))  # バーンスタイン多項式による点の計算

class BernsteinRecCurve(DeCasteljauCurve): # BernsteinRecCurveクラスの定義
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を
    bersteinRec関数によるバーンスタイン関数値で計算して返す
    '''
    B = np.array([bernsteinRec(self.n, i, t) for i in range(self.n+1)])
                                         # n次バーンスタイン多項式値のnp.array
    return B.dot(np.array(self.points))  # バーンスタイン多項式による点の計算

class BernsteinDPCurve(DeCasteljauCurve): # BernsteinDPCurveクラスの定義
  def evaluate(self, t):                 # 曲線上の点座標計算メソッド
    '''
    t - パラメタ値
    与えられたパラメタ値に対する点の座標値(ワールド座標系)を
    bersteinDP関数によるバーンスタイン関数値リストで計算して返す
    '''
    B = bernsteinDP(self.n, t)           # n次バーンスタイン多項式値のnp.array
    return B.dot(np.array(self.points))  # バーンスタイン多項式による点の計算

def main():                              # main関数
  if len(sys.argv) > 1:                  # シェル引数がある場合
    com = sys.argv[1]                    # 第1引数を次数の文字列
  else:                                  # シェル引数がない場合
    print('0:Recursive de Casteljau, 1:Iterative de Casteljau, 2:Binomial Bernstein')
    com = input('3:Recursive Bernstein, 4:Iterative Bernstein -> ')
                                         # ベジエ曲線クラスの文字列を入力
  Classes = [DeCasteljauCurve, DeCasteljauDPCurve, BernsteinCurve, \
             BernsteinRecCurve, BernsteinDPCurve] # ベジエ曲線クラスのリスト
  BezierClass = Classes[int(com)%len(Classes)] # 算出クラスの決定
  PCMain(BezierClass, offset=1)          # 多項式main関数の呼出

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出
