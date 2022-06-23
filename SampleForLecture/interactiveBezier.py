import sys                               # sysモジュールのimport
from interactivePCCanvas import InteractivePCCanvas
                                         # interactivePCCanvasモジュールのimport
from bezierCurve import DeCasteljauCurve, DeCasteljauDPCurve, \
     BernsteinCurve, BernsteinRecCurve, BernsteinDPCurve
                                         # bezierCurveモジュールのimport

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
  canvas = InteractivePCCanvas(BezierClass) # canvasの作成
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出
