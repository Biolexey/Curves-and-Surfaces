import sys                               # sysモジュールのimport
from interactivePCCanvas import InteractivePCCanvas
                                         # interactivePCCanvasモジュールのimport
from BsplineCurve import BsplinedeBoor, Bsplinebasis, SubdivisionBspline

def main():                              # main関数
  if len(sys.argv) > 1:                  # シェル引数がある場合
    mode = sys.argv[1]                   # 第1引数を次数の文字列
  else:                                  # シェル引数がない場合
    mode = int(input("Normal Subdivision: 0, Four Points Scheme: 1 -> "))

  if mode == 1:                          # 4点スキーマの際にはorderは関係ない
    order = 0
  else:
    order = int(input("# of degree -> "))# 次元数入力
  canvas = InteractivePCCanvas(SubdivisionBspline, order, mode)# canvasの作成
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出