# dashboard

## 目次

- [dashboard](#dashboard)
  - [目次](#目次)
  - [1. セットアップ手順](#1-セットアップ手順)
    - [1-1. パッケージインストール](#1-1-パッケージインストール)
    - [1-2. Amplifyインストール](#1-2-amplifyインストール)
    - [1-3. Amplify セットアップ](#1-3-amplify-セットアップ)
    - [1-4. Amplify 認証機能追加](#1-4-amplify-認証機能追加)
  - [2. 開発画面表示](#2-開発画面表示)
  - [3. コードチェック](#3-コードチェック)
  - [4. ビルド](#4-ビルド)
  - [5. ユニットテスト](#5-ユニットテスト)
  - [6. デプロイ手順](#6-デプロイ手順)
    - [6-1. ビルド](#6-1-ビルド)
    - [6-2. AWSコンソールログイン](#6-2-awsコンソールログイン)
    - [6-3. S3バケットへ移動](#6-3-s3バケットへ移動)
    - [6-4. 古いソース類のバックアップ](#6-4-古いソース類のバックアップ)
    - [6-5. 新ファイル、ディレクトリのアップロード](#6-5-新ファイルディレクトリのアップロード)
    - [6-5. 反映確認](#6-5-反映確認)
  - [7. その他留意事項](#7-その他留意事項)
    - [7-1. ログイン画面](#7-1-ログイン画面)
    - [7-2. API](#7-2-api)

## 1. セットアップ手順

### 1-1. パッケージインストール

```sh
$ yarn
```

### 1-2. Amplifyインストール

```sh
yarn global add @aws-amplify/cli@12.13.1

amplify --version
```

コマンドが存在しない場合、パスを確認

```sh
yarn global bin

# 上のコマンドで出力されたパスが含まれているか確認
echo $PATH
```

パスが通っていない場合、~/.bashrcに以下の行追加

```sh
# 必要であれば".yarn/bin"の部分を自身のパスに置き換える
export PATH="$HOME/.yarn/bin:$PATH"
```

bashを再度立ち上げ確認

```sh
amplify --version
```

### 1-3. Amplify セットアップ

```sh
$ amplify configure

# AWSマネジメントコンソールのログイン画面からログイン
Sign in to your AWS administrator account:
https://console.aws.amazon.com/
Press Enter to continue

# リージョン指定
# ap-northeast-1を選択
Specify the AWS Region
? region:  (Use arrow keys)
❯ us-east-1
  us-east-2
  us-west-1
  us-west-2
  eu-north-1
  eu-south-1
  eu-west-1
(Move up and down to reveal more choices)

# 選択後は以下が表示
? region:  ap-northeast-1
Follow the instructions at
https://docs.amplify.aws/cli/start/install/#configure-the-amplify-cli

# IAMユーザ作成
# 既に作成済みのため何もせずEnter
to complete the user creation in the AWS console
https://console.aws.amazon.com/iamv2/home#/users/create
Press Enter to continue

# 認証情報を入力
Enter the access key of the newly created user:
? accessKeyId: *****************
? secretAccessKey: *************************************

# 任意の値を設定
This would update/create the AWS Profile in your local machine
? Profile Name: userprofile

# 下記が表示されれば完了
Successfully set up the new user.

# 入力した情報が反映されていることを確認
$ cat ~/.aws/credentials

$ amplify init
# y
? Do you want to continue with Amplify Gen 1? (y/N)

# 任意の値を選択
? Why would you like to use Amplify Gen 1? …  (Use arrow keys or type to filter)
❯ I am a current Gen 1 user
  Gen 2 is missing features I need from Gen 1
  I find the Gen 1 CLI easier to use
  Prefer not to answer

# 任意のプロジェクト名を設定
? Enter a name for the project (dashboard)

# 下記設定内容で問題なければY
The following configuration will be applied:

Project information
| Name: xxxxxxxxxxx
| Environment: dev
| Default editor: Visual Studio Code
| App type: javascript
| Javascript framework: vue
| Source Directory Path: src
| Distribution Directory Path: dist
| Build Command: npm run-script build
| Start Command: npm run-script serve

? Initialize the project with the above configuration? (Y/n)
Using default provider  awscloudformation

# 認証方式を選択
? Select the authentication method you want to use: (Use arrow keys)
❯ AWS profile 
  AWS access keys

# 接続するAWSアカウントを選択
For more information on AWS Profiles, see:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html

? Please choose the profile you want to use 
  default 
❯ account_1
  account_2

Adding backend environment dev to AWS Amplify app: xxxxxxxx

Deployment completed.
Deploying root stack sasakitest [ ==========------------------------------ ] 1/4
        DeploymentBucket               AWS::S3::Bucket                CREATE_COMPLETE                Thu Mar 27 2025 13:47:40…     

# 障害時にAmplifyに機密性の低い情報を提供するか選択
? Help improve Amplify CLI by sharing non-sensitive project configurations on failures (y/N)

# 下記が表示されればセットアップ完了
Deployment state saved successfully.
✔ Initialized provider successfully.
✅ Initialized your environment successfully.
✅ Your project has been successfully initialized and connected to the cloud!
Some next steps:

"amplify status" will show you what you've added already and if it's locally configured or deployed
"amplify add <category>" will allow you to add features like user login or a backend API
"amplify push" will build all your local backend resources and provision it in the cloud
"amplify console" to open the Amplify Console and view your project status
"amplify publish" will build all your local backend and frontend resources (if you have hosting category added) and provision it in the cloud


Pro tip:
Try "amplify add api" to create a backend API and then "amplify push" to deploy everything
```

### 1-4. Amplify 認証機能追加

下記を実行時認証関係のリソース作成
```sh
$ amplify add auth

# 下記が表示される
Using service: Cognito, provided by: awscloudformation
 
 The current configured provider is Amazon Cognito. 
 
# Default configurationを選択（詳細設定する場合は Manual configuration を選択）
 Do you want to use the default authentication and security configuration? (Use arrow keys)
❯ Default configuration 
  Default configuration with Social Provider (Federation) 
  Manual configuration 
  I want to learn more. 

# サインイン時の認証方法を選択
 Warning: you will not be able to edit these selections. 
 How do you want users to be able to sign in? 
  Username 
❯ Email 
  Phone Number 
  Email or Phone Number 
  I want to learn more.

 Do you want to configure advanced settings?
❯ No, I am done.

✅ Successfully added auth resource sasakiteste42f7add locally

✅ Some next steps:
"amplify push" will build all your local backend resources and provision it in the cloud
"amplify publish" will build all your local backend and frontend resources (if you have hosting category added) and provision it in the cloud

# 設定内容をデプロイ
$ amplify push
```

上記手順で Amazon Cognito に新規ユーザープールが作成される
作成されたユーザープール内に新規ユーザー作成


## 2. 開発画面表示

```sh
$ yarn dev
```

## 3. コードチェック

```sh
# ESLintによるコードチェック
$ yarn lint
# ESLintのrulesに基づいてコード自動修正
$ yarn lint-fix
```

## 4. ビルド

```sh
$ yarn build
```

distディレクトリ配下にビルドしたファイルが格納される

```
/dashboard/dist
├── assets
├── favicon.ico
└── index.html
```

## 5. ユニットテスト

```sh
yarn test:unit
```

## 6. デプロイ手順

### 6-1. ビルド

[3. コードチェック](#3-コードチェック), [4. ビルド](#3-ビルド)の手順に従い、  
コードチェック後問題なければビルド

### 6-2. AWSコンソールログイン

あらかじめ開発者向けのアカウントを取得したうえで、AWSコンソール画面にログイン  


### 6-3. S3バケットへ移動

ログイン後、コンソールの画面から「S3」を選択、表示されているバケットの一覧から、「汎用バケット」のタブをクリックしたうえで  
ダッシュボードのアプリを格納するバケットを選択  

### 6-4. 古いソース類のバックアップ

`old`ディレクトリ内に移動し、中にあるファイルを全て削除

ルートディレクトリに移動し、`assets`、`favicon.ico`、`index.html`にチェックを入れ、  
「アクション」をクリック、表示されたドロップダウンメニューから「移動」を選択  
送信先の欄に、「送信先タイプ」として「汎用バケット」を指定  
送信先には「S3の参照」から`old`ディレクトリを指定し、画面下にある「移動」をクリック  
  
ルートディレクトリに`old`ディレクトリ以外存在しないことを確認

### 6-5. 新ファイル、ディレクトリのアップロード

削除完了後、同じS3バケットのディレクトリにいることを確認したうえで「アップロード」をクリック  
アップロードの画面で、[6-1. ビルド](#6-1-ビルド)でビルドしたファイル、ディレクトリをまとめて選択して、「アップロード」ボタンをクリック

### 6-5. 反映確認

CloudFront経由、もしくはS3バケットを直接参照し、変更が反映されているか確認する  
CloudFront経由でアクセスする場合、反映に時間がかかる可能性があるため、  
急ぎの確認が必要な場合はCloudFrontのキャッシュをクリアして確認する

## 7. その他留意事項

### 7-1. ログイン画面

ログイン画面はAWS Amplifyを使用してAWSリソースを一括管理している  
関連リソース一覧はAWSコンソールからCloud Formationを参照  
  
ログイン用アカウントはAmazon Cognitoで管理  
ユーザー追加、ユーザー情報変更の際はAWSコンソールからCognitoのユーザプールを編集  

### 7-2. API

API関連のリソースはAWS Amplifyを使用せず、手動で作成  
APIのベースURLは`./src/aws-api-exports.js`を作成しそこに記載している  

`yarn dev`コマンドを実行すると`./.env.development`の情報が読み込まれるため、
自動的に開発用APIを実行する  
ローカル環境で本番用APIを実行したい場合は`./.env.development`の`VITE_ADMIN_API_ROOT_URL`の値を修正する

`yarn build`コマンドを実行すると`./.env.production`の情報が読み込まれるため、
ビルドしたコードにおいては自動的に本番用APIを実行する  
