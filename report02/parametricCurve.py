import numpy as np                       # numpyモジュールのimport (npで)

class ParametricCurve(object):           # ParametricCurveクラスの定義
  def __init__(self, canvas):            # 初期化メソッド
    '''
    canvas - 描画するcanvas
    ParametricCurveオブジェクトを初期化する
    '''
    self.canvas = canvas                 # canvasの設定

  def drawCurve(self, ts = 0, te = 0, offset = np.array((0, 0)), nop = 128):
                                         # ParametricCurveオブジェクトの描画メソッド
    '''
    ts, te - 描画対象のパラメタ値 (開始,終了)，省略時 0, 0
    offset - 平行移動ベクトル，省略時 (0, 0)
    nop    - 描画セグメント数，省略時 128
    曲線を離散化して線分列として描画する
    '''
    dt = (te - ts) / nop                 # 1セグメントに相当するパラメタ
    prevPnt = self.evaluate(ts) + offset # 最初の点の座標 (ワールド座標系)
    prevIn  = self.canvas.inside(prevPnt) # 最初の点が表示領域内にあるか否か
    for i in range(nop):                 # 線分列の数だけ反復
      currPnt = self.evaluate(ts + dt*(i+1)) + offset # 次の点の座標 (ワールド座標系)
      currIn  = self.canvas.inside(currPnt) # 次の点が表示領域内にあるか否か
      if prevIn or currIn:               # 両端点のいずれかが表示領域内にある
        self.canvas.drawPolyline([prevPnt, currPnt]) # 線分を表示する
      prevPnt, prevIn = (currPnt, currIn) # 次の点を現在の点にする

  def drawBernstein(self, I,  ts = 0, te = 0, offset = np.array((0, 0)), nop = 512):
                                         # ParametricCurveオブジェクトの描画メソッド
    '''
    ts, te - 描画対象のパラメタ値 (開始,終了)，省略時 0, 0
    offset - 平行移動ベクトル，省略時 (0, 0)
    nop    - 描画セグメント数，省略時 128
    曲線を離散化して線分列として描画する
    '''
    dt = (te - ts) / nop                 # 1セグメントに相当するパラメタ
    prevPnt = self.evaluate(I, ts) + offset # 最初の点の座標 (ワールド座標系)
    prevIn  = self.canvas.inside(prevPnt) # 最初の点が表示領域内にあるか否か
    for i in range(nop):                 # 線分列の数だけ反復
      currPnt = self.evaluate(I, ts + dt*(i+1)) + offset # 次の点の座標 (ワールド座標系)
      currIn  = self.canvas.inside(currPnt) # 次の点が表示領域内にあるか否か
      if prevIn or currIn:               # 両端点のいずれかが表示領域内にある
        self.canvas.drawPolyline([prevPnt, currPnt]) # 線分を表示する
      prevPnt, prevIn = (currPnt, currIn) # 次の点を現在の点にする