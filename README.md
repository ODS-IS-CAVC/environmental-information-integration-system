# 環境情報連携システム

![環境情報連携システム構成イメージ](./EnvironmentalInformationIntegrationSystem_arch.drawio.svg)

- [環境情報連携システム](#環境情報連携システム)
  - [概要](#概要)
  - [前提](#前提)
  - [ライセンス](#ライセンス)
    - [利用ライブラリ及び動作確認済みバージョン](#利用ライブラリ及び動作確認済みバージョン)
      - [Python(バックエンド)](#pythonバックエンド)
      - [TypeScript(フロントエンド)](#typescriptフロントエンド)
  - [問合せ及び要望に関して](#問合せ及び要望に関して)
  - [免責事項](#免責事項)

## 概要

道路上に設置した路側デバイス(カメラやLiDAR等)の情報を収集・管理・提供するクラウドシステムです。  
データを収集・提供するWeb APIと蓄積するデータベースおよび可視化するダッシュボードによって構成されます。  
データを収集・提供するWeb APIの仕様は本リポジトリの[ドキュメント](./API/doc/environmentalInformationIntegrationSystem.html)を参照ください。

## 前提

- クラウド
  - [AWS(Amazon Web Services)](https://aws.amazon.com/jp/what-is-aws/)
    - 主な利用サービス
      - Lambda
        - APIバックエンド処理  
          [API/lambda](./API/lambda)にソースコードを格納
      - API Gateway
        - API管理・監視  
          [API Gateway](./API/APIGateway)にCloudFormationテンプレートを格納
      - DynamoDB
        - 路側データ蓄積  
          [DynamoDB.yml](./DB/DynamoDB.yml)にテーブル構成等のCoudFormationテンプレートを格納
      - ElastiCahe
        - 最新路側データのキャッシュ  
          [elastiCache.yml](./DB/elastiCache.yml)にテーブル構成等のCoudFormationテンプレートを格納
      - Amplify
        - ダッシュボード構築  
          [dashboard](./dashboard)にソースコードを格納
- 使用言語
  - [Python](https://www.python.org/)
    - version: 3.12
  - [TypeScript](https://www.typescriptlang.org/)
    - version: 5.6.3

## ライセンス

本リポジトリは[MITライセンス](./LICENSE)で提供されています。

### 利用ライブラリ及び動作確認済みバージョン

#### Python(バックエンド)

- [awswrangler](https://pypi.org/project/awswrangler/)
  - version: 2.15.1
  - License: [Apache 2.0](https://github.com/aws/aws-sdk-pandas/blob/main/LICENSE.txt)
- [pandas](https://pypi.org/project/pandas/)
  - version: 1.2.3
  - License: [BSD](https://github.com/pandas-dev/pandas/blob/main/LICENSE)
- [redis](https://pypi.org/project/redis/)
  - version: 5.2.0
  - License: [MIT](https://github.com/redis/redis-py/blob/master/LICENSE)
- [requests](https://pypi.org/project/requests/)
  - version: 2.32.3
  - License: [Apache 2.0](https://github.com/psf/requests/blob/main/LICENSE)

#### TypeScript(フロントエンド)

- [@aws-amplify/ui-vue](https://classic.yarnpkg.com/en/package/@aws-amplify/ui-vue)
  - version: 4.2.26
  - License: [Apache 2.0](https://github.com/aws-amplify/amplify-ui/blob/4e9ec647d1b734791c43e117479a4c4dfbd29736/LICENSE)
- [aws-amplify](https://classic.yarnpkg.com/en/package/aws-amplify)
  - version: 6.10.3
  - License: [Apache 2.0](https://github.com/aws-amplify/amplify-js/blob/main/LICENSE)
- [loglevel](https://classic.yarnpkg.com/en/package/loglevel)
  - version: 1.9.2
  - License: [MIT](https://github.com/pimterry/loglevel/blob/main/LICENSE-MIT)
- [pinia](https://classic.yarnpkg.com/en/package/pinia)
  - version: 2.3.0
  - License: [MIT](https://github.com/vuejs/pinia/blob/v3/LICENSE)
- [vue](https://classic.yarnpkg.com/en/package/vue)
  - version: 3.5.13
  - License: [MIT](https://github.com/vuejs/core/blob/main/LICENSE)
- [vue-router](https://classic.yarnpkg.com/en/package/vue-router)
  - version: 4.5.0
  - License: [MIT](https://github.com/vuejs/router/blob/main/LICENSE)
- [vuetify](https://classic.yarnpkg.com/en/package/vuetify)
  - version: 3.7.5
  - License: [MIT](https://github.com/vuetifyjs/vuetify/blob/master/LICENSE.md)

## 問合せ及び要望に関して

本リポジトリは主に配布目的の運用となるため、IssueやPull Requestに関しては受け付けておりません。

## 免責事項

本リポジトリの内容は予告なく変更・削除する可能性があります。  
本リポジトリの利用により生じた損失及び損害等について、いかなる責任も負わないものとします。
