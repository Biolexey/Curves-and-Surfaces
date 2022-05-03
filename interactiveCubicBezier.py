import numpy as np                       # numpyモジュールのimport (npで)
from myCanvas import MyCanvas            # myCanvasモジュールのimport
from cubicBezierCurve import CubicBezierCurve # cubicBezierCurveモジュールのimport

points = []                              # 制御点のリスト
pickid = -1                              # ピックされた点の番号
NP     = 4                               # 3次ベジエ曲線の制御点数

def norm(v):                             # ベクトルのノルム計算
  '''
  v - ベクトル
  ベクトルの大きさを返す
  '''
  v = np.array(v)                        # numpy.array への変換
  return np.dot(v, v)**0.5               # 内積計算して平方根

def pressed1(event):                     # Button1 pressed コールバック関数
  global canvas, points, pickid          # 大域変数 canvas, points, pickid
  newpnt = canvas.point(event.x, event.y) # プレスされた座標の点を作成
  if len(points) < NP:                   # 制御点数が 4個に満たない場合
    pickid = -1                          # ピックされた点ではない
    points.append(newpnt)                # プレスで作られた点を制御点として追加
    canvas.drawMarker(newpnt)            # 新しい制御点の描画
    if len(points) == NP:                # 制御点数が 4個に到達
      canvas.clear()                     # canvasのクリア
      CubicBezierCurve(canvas, points).drawCurve() # 3次ベジエ曲線の描画
  else:                                  # 制御点数が既に4個で，ピック処理
    pickid, pickdist = (0, norm(newpnt-points[0])) # ピックされた点と距離の初期化
    for i in range(1, len(points)):      # 他の制御点との比較
      dist = norm(newpnt-points[i])      # 制御点との距離
      if dist < pickdist:                # 距離が小さい場合
        pickid, pickdist = (i, dist)     # ピックされた点の更新
    if pickdist > canvas.mr * 5 / canvas.s: # 距離がマーカの大きさより大きい場合
      pickid = -1                        # ピックされた点ではない

def dragged1(event):                     # Button1 dragged コールバック関数
  global canvas, points, pickid          # 大域変数 canvas, points, pickid
  if 0 <= pickid <= NP-1:                # ピックされた点の番号の確認
    points[pickid] = canvas.point(event.x, event.y) # ドラッグされた座標に変更
    canvas.clear()                       # canvasのクリア
    CubicBezierCurve(canvas, points).drawCurve() # 3次ベジエ曲線の描画

def pressed2(event):                     # Button2 pressed コールバック関数
  global canvas, points                  # 大域変数 canvas, points
  points = []                            # 制御点リストの初期化
  canvas.clear()                         # canvasのクリア

def main():                              # main関数
  global canvas                          # 大域変数 canvas
  canvas = MyCanvas()                    # canvasの作成
  canvas.bind('<Button-1>', pressed1)    # Button1 pressed コールバック関数
  canvas.bind('<B1-Motion>', dragged1)   # Button1 dragged コールバック関数
  canvas.bind('<Button-2>', pressed2)    # Button2 pressed コールバック関数
  canvas.mainloop()                      # ルートフレームの実行ループ開始

if __name__ == '__main__':               # 起動の確認 (コマンドラインからの起動)
  main()                                 # main関数の呼出
