from datetime import datetime, timezone, timedelta


JST = timezone(timedelta(hours=+9), 'JST')

# [サンプル]UNIX秒(UTC)を生成
epoch = int(datetime.now(timezone.utc).strftime('%s%f')) // 1000000

# datetime(JST)に変換
dt = datetime.fromtimestamp(epoch).replace(tzinfo=timezone.utc).astimezone(tz=JST)

# ISO8601表記
print(dt.isoformat()) 

# あるいは任意のフォーマット
print(dt.strftime('%Y-%m-%d %H:%M:%S'))
