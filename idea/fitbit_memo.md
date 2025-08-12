## Fitbit可視化アプリの構想
- まずはログイン機能はつけない
- 一方で、API叩くためのトークン取得は簡単にしたい
  - Swaggerを参考にする

## API探索
### Sleep
#### https://api.fitbit.com/1.2/user/-/sleep/list.json
レスポンスデータを `./data/fitbit_sleep_list.json` に格納している

- sleepという配列の中に日ごとの記録が入っている

#### https://api.fitbit.com/1.2/user/-/sleep/date/2025-07-20.json
レスポンスデータは `../data_visualization/data/get.json` を参照

使えそうなデータは以下の通り
- dateOfSleep: 起きた時間の日付になるっぽい
- startTime
- endTime


#### https://api.fitbit.com/1.2/user/-/sleep/goal.json
`./data/goal.json` を参照

これはおそらく目標設定のデータかな

- minDuration
  - 目標睡眠時間
- bedtime
  - 目標就寝時間
- wakeupTime
  - 目標起床時間
- updatedOn