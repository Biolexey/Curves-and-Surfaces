import sys                               # sysモジュールのimport
from interactivePCCanvas import InteractivePCCanvas
                                         # interactivePCCanvasモジュールのimport
from BsplineCurve import BsplinedeBoor, Bsplinebasis, SubdivisionBspline

def main():                              # main関数
  if len(sys.argv) > 1:                  # シェル引数がある場合
    order = sys.argv[1]                    # 第1引数を次数の文字列
  else:                                  # シェル引数がない場合
    order = int(input("# of degree -> "))# 次元数入力
                                         # Bspline曲線描画クラスの文字列を入力 
  canvas = InteractivePCCanvas(SubdivisionBspline, order)# canvasの作成
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出