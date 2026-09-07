# Windows JV-Link Collector

JRA-VAN Data Lab.の取得処理を、Vercelおよび予測モデルから分離するクライアントです。

## 前提

- 日本語版Windowsの対応バージョン（64bit構成を採用）
- Python 3.14 64bit
- JRA-VAN Data Lab.契約とサービスキー
- 公式JV-LinkおよびJRA-VAN SDK 5.0.0以降
- SDKの利用条件・配布条件への同意

サービスキー、認証情報、SDKバイナリ、取得したJV-Dataはこのリポジトリへ追加しません。

## 出力契約

最初の実装は `public/templates/results.csv` と同じ列へ変換し、`ml.pipeline` に渡します。
変換時には取得日時、データ種別、JV-Data仕様バージョン、最終取得キーを非公開ログに記録します。
同一レコードを再取得しても結果が変わらないよう、レースIDと馬IDで重複を排除します。

## 未実装

SDK導入済みWindows環境が用意されるまで、JV-Linkの呼び出しコードは追加しません。
VercelからJV-Linkを呼ぶ構成、ログイン自動化、HTMLスクレイピング、自動投票は対象外です。

## 準備確認

`JRA_VAN_SDK_PATH` にSDKの展開先を設定して、Windows PowerShellで実行します。
サービスキーそのものを環境変数へ設定する必要はありません。

```powershell
$env:JRA_VAN_SDK_PATH = "C:\path\to\JRA-VAN-SDK"
py -3.14 collector\windows\preflight.py
py -3.14 -m unittest collector.windows.test_preflight
```

準備確認はOS、Pythonのビット数・バージョン、SDKフォルダー、共通スキーマだけを検査し、JV-Linkへ通信しません。
