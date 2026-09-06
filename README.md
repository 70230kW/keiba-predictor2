# KEIBA LAB / keiba-predictor2

客観的な競走データだけを使う競馬予測アプリの開発基盤。
**実データ未接続・モデル未学習。画面の馬名、レース、予測値は架空サンプルです。**

## v0.2
- 黒・チャコール・ゴールドのレスポンシブ画面
- CSVひな形のダウンロード（画面下部）
- 共通CSVの欠損・重複・数値・列検査
- 当日より前の戦績のみから特徴量を生成
- 特徴量許可リストをPythonとTypeScriptで共有
- 日付単位の学習／検証／最終評価分割、評価指標の出力
- GitHub Actionsによる検証。Vercel既存連携設定は変更なし

## Web
```bash
npm ci
npm run dev
npm run typecheck
npm run test:policy
npm run build
```

## CSV取り込み・学習
Python 3.10以上。取込と取込テストは標準ライブラリのみで実行できます。
```bash
python -m ml.pipeline /path/to/licensed-results.csv --output data/processed/training.csv
python -m unittest ml.test_pipeline
pip install -r ml/requirements.txt
python -m unittest ml.test_training
python -m ml.train
```
[入力仕様・制限・時点管理](docs/data-contract.md)を必ず確認してください。
実データ、学習済みモデル、認証情報は公開リポジトリに含めません。
学習成果物と指標はartifacts/に保存します。既存ファイルは上書きしません。
合成データのテストは動作確認専用で、予測精度の裏付けにはなりません。

## オッズ除外方針
オッズ・人気・投票行動・配当・予想印・SNS評価を予測入力に使いません。
未知列も拒否する明示的許可リストです。当該レース結果は目的変数のみで使用します。
収支検証を追加する場合も、市場データは予測経路から分離します。

## 次の工程
1. データ提供元と個人利用・公開条件の確認（契約は別途判断）
2. 取得元固有の変換処理、実データで学習
3. 確率校正・レース単位評価・時系列バックテストの拡充
4. 予測出力と画面の接続、運用の自動化

WebへのCSVアップロード、DB永続化、リアルタイム取得、自動投票は未実装です。
予測は的中や利益を保証しません。
