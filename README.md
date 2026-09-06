# KEIBA LAB / keiba-predictor2

オッズ・人気・投票行動・予想印を使わず、客観的な競走データだけで各馬の勝率を推定する競馬予測アプリです。

## 現在のMVP

- Next.js 16 / TypeScriptによるVercel対応UI
- 推定勝率・3着内率・能力分析のサンプル画面
- オッズ等の混入を拒否する予測ポリシーとテスト
- LightGBMの時系列分割ベースライン
- GitHub Actionsによる型検査・ポリシーテスト・ビルド

画面上の馬名・レース・予測値は、UI開発用の架空データです。

## 予測ポリシー

モデル入力では、単勝・複勝・最終オッズ、人気順位、投票割合、確定配当、予想印、SNS評価を禁止します。収支検証に使う場合も予測処理から分離します。

## ローカル起動

```bash
npm install
npm run dev
```

## 検証

```bash
npm run typecheck
npm run test:policy
npm run build
```

## 機械学習

`ml/train.py` は `data/processed/training.csv` を日付順に分割し、LightGBMモデルを生成します。CSVには `race_date`、`race_id`、`horse_id`、`finished_first` と客観的特徴量が必要です。

## 次の開発項目

1. 正式なデータ提供元と利用条件の決定
2. データ取り込み・正規化パイプライン
3. レース単位の時系列バックテスト
4. 予測結果JSONを生成するGitHub Actions
5. Vercelへの接続と公開

予測は的中や利益を保証するものではありません。
