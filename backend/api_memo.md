## auth

- @ ログイン      (POST /auth/login)
- @ (ログアウト)  (GET /auth/logout)

### エラー

- 1000: invalid e-mail address or password
  メールアドレスかパスワードが異なる
- 1001: no active user
  ログインしていない

## users

- @ 新規登録 (POST /users)
- @ 特定のユーザーの情報の取得 (GET /users/{user_id})
- @ 自分の取得 (GET /me)

### エラー

- 2000: specified user not found
  ユーザーが見つからない
- 2001: e-mail already registered
  メールアドレスがすでに登録されている

## lives

- @ ライブ検索 (GET /lives?q={title}&popularity={number_of_users})
  - タイトルで検索
  - 登録者数でフィルタ
    - ホットなライブをこれでとる
- @ 特定のライブの情報を取得 (GET /lives/{live_id})
- @ 参加登録 (POST /lives/registration)

### エラー

- 3000: specified live not found
  ライブが見つからない
- 3001: invalid user specified
  自分ではないユーザー ID で登録しようとしている
- 3002: invalid live ticket
  ライブのチケット番号が有効ではない

## directmessages

- @ ユーザーに送信 (POST /directmessages)
- @受信したメッセージを一覧 (GET /directmessages?central={central_user_id}&target={target_user_id})

### エラー
- 4000: invalid sender specified
  自分ではないユーザー ID で登録しようとしている
- 4001: invalid receiver specified
  送信先のユーザーが存在しない
- 4002: receiver not followed by sender
  送信者が送信先のユーザーをフォローしていない
- 4003: invalid central specified
  会話の中心となる人物が自分ではない
- 4004: no ff relation between central and target
  会話の中心となる人物とターゲットとの間に FF 関係がない

## posts

- @新しく投稿 (POST /posts)
- @特定のライブの投稿を一覧 (GET /posts?live={live_id}&author={author_id})

### エラー

- 5000: invalid author specified
  自分ではないユーザー ID から投稿しようとした
- 5001: live not found
  投稿先の部屋 (ライブ) が存在しない
- 5002: reply target not found
  リプライ先が存在しない

## follows

- @ ユーザーをフォロー (POST /follows)
- @ ユーザーのフォロワーを検索 (GET /follows?user={user_id}target={target_user_id})
- @ ユーザーのフォローを解除 (DELETE /follows/{follow_id})

### エラー

- 6000: already followed
  すでにフォローしている
- 6001: invalid user specified
  自分ではないユーザーからフォローしようとした
- 6002: user not found
  対象となるユーザーがみつからない
- 6003: specified follow is not created by user
  他人がしたフォローを削除しようとした
- 6004: follow not found
  解除するフォローがみつからない

## goods

- @ 投稿にいいね (POST /goods)
- @ いいねを一覧 (GET /goods?user={user_id}&post={post_id})
- @ いいねを削除 (DELETE /goods/{good_id})

### エラー

- 7000: good already done
  すでにいいねしている
- 7001: invalid user specified
  自分ではないユーザーからいいねしようとした
- 7002: user not found
  対象となるユーザーがみつからない
- 7005: post not found
  対象となる投稿がみつからない
- 7003: specified good is not created by user
  他人がしたいいねを削除しようとした
- 7004: good not found
  解除するいいねがみつからない
