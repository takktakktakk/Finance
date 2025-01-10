from datetime import datetime, timezone, timedelta


JST = timezone(timedelta(hours=+9), 'JST')

# [サンプル]時刻を表す文字列(JST)を生成
now = datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')

# datetime(UTC)に変換
dt = datetime.strptime(now, '%Y-%m-%d %H:%M:%S').astimezone(tz=JST).replace(tzinfo=JST).astimezone(tz=timezone.utc)

# UNIX時間(UTC)
print(int(dt.strftime('%s%f')) // 1000000)
