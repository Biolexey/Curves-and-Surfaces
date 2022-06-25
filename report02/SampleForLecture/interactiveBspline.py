import sys                               # sysモジュールのimport
from interactivePCCanvas import InteractivePCCanvas
                                         # interactivePCCanvasモジュールのimport
from BsplineCurve import BsplinedeBoor, Bsplinebasis

def main():                              # main関数
  if len(sys.argv) > 1:                  # シェル引数がある場合
    com = sys.argv[1]                    # 第1引数を次数の文字列
  else:                                  # シェル引数がない場合
    com = input('0: de Boor, 1: B-spline Basis Func -> ')
                                         # Bspline曲線描画クラスの文字列を入力
  #prm = list(map(int, input("Put the parameter t ->").split()))
  order = int(input("# of degree -> "))  # 次元数入力
  Classes = [BsplinedeBoor, Bsplinebasis]# Bspline曲線クラスのリスト
  Class = Classes[int(com)%len(Classes)] # 算出クラスの決定
  canvas = InteractivePCCanvas(Class, order)    # canvasの作成
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出