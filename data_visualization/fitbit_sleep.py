import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

# ページ設定
st.set_page_config(
    page_title="Fitbit 睡眠データダッシュボード",
    page_icon="😴",
    layout="wide"
)

# ダミーデータ生成関数
@st.cache_data
def generate_dummy_sleep_data(days=30):
    """Fitbitの睡眠データを模したダミーデータを生成"""
    
    dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]
    
    data = []
    for date in dates:
        # 就寝時間（22:00-25:00の間でランダム）
        bedtime_hour = random.uniform(20, 23)
        bedtime = date.replace(hour=int(bedtime_hour), minute=int((bedtime_hour % 1) * 60))
        
        # 起床時間（6:00-9:00の間でランダム）
        wakeup_hour = random.uniform(6, 9)
        wakeup = (date + timedelta(days=1)).replace(hour=int(wakeup_hour), minute=int((wakeup_hour % 1) * 60))
        
        # 総睡眠時間（6-9時間）
        total_sleep = random.uniform(6, 9)
        
        # 睡眠段階の時間（分）
        deep_sleep = random.uniform(60, 120)  # 深い睡眠
        light_sleep = random.uniform(180, 300)  # 浅い睡眠
        rem_sleep = random.uniform(60, 120)  # REM睡眠
        awake_time = random.uniform(10, 40)  # 覚醒時間
        
        # 睡眠効率（85-98%）
        sleep_efficiency = random.uniform(85, 98)
        
        # 睡眠スコア（60-95）
        sleep_score = random.uniform(60, 95)
        
        data.append({
            'date': date.date(),
            'bedtime': bedtime,
            'wakeup': wakeup,
            'total_sleep_hours': total_sleep,
            'deep_sleep_minutes': deep_sleep,
            'light_sleep_minutes': light_sleep,
            'rem_sleep_minutes': rem_sleep,
            'awake_minutes': awake_time,
            'sleep_efficiency': sleep_efficiency,
            'sleep_score': sleep_score,
            'time_to_fall_asleep': random.uniform(5, 30)  # 入眠時間（分）
        })
    
    return pd.DataFrame(data)

# 時間軸での睡眠パターン可視化
def create_sleep_timeline(df):
    """睡眠・起床時間のタイムライン表示"""
    fig = go.Figure()
    
    for i, row in df.iterrows():
        # 就寝時間と起床時間を時間（小数）に変換
        bedtime_hours = row['bedtime'].hour + row['bedtime'].minute / 60
        wakeup_hours = row['wakeup'].hour + row['wakeup'].minute / 60
        
        # 翌日にまたがる場合の処理（起床時間が就寝時間より小さい場合）
        if wakeup_hours < bedtime_hours:
            wakeup_hours += 24
        
        # 就寝時間から起床時間までのバー
        fig.add_trace(go.Scatter(
            x=[row['date'], row['date']],
            y=[bedtime_hours, wakeup_hours],
            mode='lines',
            line=dict(color='darkblue', width=8),
            name='睡眠時間' if i == 0 else "",
            showlegend=i == 0,
            hovertemplate=f"日付: {row['date']}<br>就寝: {row['bedtime'].strftime('%H:%M')}<br>起床: {row['wakeup'].strftime('%H:%M')}<br>睡眠時間: {row['total_sleep_hours']:.1f}時間<extra></extra>"
        ))
    
    # Y軸の目盛りを時間表示にカスタマイズ
    yticks = []
    ytick_labels = []
    for hour in range(18, 36):  # 18時から翌日12時まで
        display_hour = hour if hour < 24 else hour - 24
        yticks.append(hour)
        ytick_labels.append(f"{display_hour:02d}:00")
    
    fig.update_layout(
        title="睡眠パターン（就寝・起床時間）",
        xaxis_title="日付",
        yaxis_title="時間",
        height=600,
        yaxis=dict(
            tickvals=yticks,
            ticktext=ytick_labels,
            range=[18, 36]  # 18時から翌日12時まで
        ),
        xaxis=dict(type='category')
    )
    
    return fig

# 睡眠段階の円グラフ
def create_sleep_stages_pie(df):
    """直近の睡眠段階を円グラフで表示"""
    latest_data = df.iloc[-1]
    
    labels = ['深い睡眠', '浅い睡眠', 'REM睡眠', '覚醒']
    values = [
        latest_data['deep_sleep_minutes'],
        latest_data['light_sleep_minutes'],
        latest_data['rem_sleep_minutes'],
        latest_data['awake_minutes']
    ]
    colors = ['#1f77b4', '#87ceeb', '#ff7f0e', '#d62728']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors,
        textinfo='label+percent',
        textfont_size=12
    )])
    
    fig.update_layout(
        title=f"睡眠段階の割合（{latest_data['date']}）",
        height=400
    )
    
    return fig

# 睡眠トレンドの可視化
def create_sleep_trends(df):
    """睡眠指標のトレンド表示"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('総睡眠時間', '睡眠効率', '睡眠スコア', '入眠時間'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # 総睡眠時間
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['total_sleep_hours'], 
                  name='総睡眠時間', line=dict(color='blue')),
        row=1, col=1
    )
    
    # 睡眠効率
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['sleep_efficiency'], 
                  name='睡眠効率', line=dict(color='green')),
        row=1, col=2
    )
    
    # 睡眠スコア
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['sleep_score'], 
                  name='睡眠スコア', line=dict(color='orange')),
        row=2, col=1
    )
    
    # 入眠時間
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['time_to_fall_asleep'], 
                  name='入眠時間', line=dict(color='red')),
        row=2, col=2
    )
    
    fig.update_xaxes(title_text="日付")
    fig.update_yaxes(title_text="時間（h）", row=1, col=1)
    fig.update_yaxes(title_text="効率（%）", row=1, col=2)
    fig.update_yaxes(title_text="スコア", row=2, col=1)
    fig.update_yaxes(title_text="時間（分）", row=2, col=2)
    
    fig.update_layout(height=600, showlegend=False, title_text="睡眠指標のトレンド")
    
    return fig

# ヒートマップ（週ごとの睡眠パターン）
def create_sleep_heatmap(df):
    """週ごとの睡眠パターンをヒートマップで表示"""
    df_copy = df.copy()
    df_copy['weekday'] = pd.to_datetime(df_copy['date']).dt.day_name()
    df_copy['week'] = pd.to_datetime(df_copy['date']).dt.isocalendar().week
    
    # 曜日の順序を設定
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_copy['weekday'] = pd.Categorical(df_copy['weekday'], categories=weekday_order, ordered=True)
    
    # ピボットテーブル作成
    heatmap_data = df_copy.pivot_table(
        values='total_sleep_hours', 
        index='weekday', 
        columns='week', 
        aggfunc='mean'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=[f'Week {w}' for w in heatmap_data.columns],
        y=heatmap_data.index,
        colorscale='Blues',
        text=np.round(heatmap_data.values, 1),
        texttemplate="%{text}h",
        textfont={"size": 10},
        colorbar=dict(title="睡眠時間（h）")
    ))
    
    fig.update_layout(
        title="週ごとの睡眠パターン（曜日別）",
        xaxis_title="週",
        yaxis_title="曜日",
        height=400
    )
    
    return fig

# メイン関数
def main():
    st.title("😴 Fitbit 睡眠データダッシュボード")
    st.markdown("---")
    
    # サイドバー
    st.sidebar.title("設定")
    days_to_show = st.sidebar.slider("表示する日数", min_value=7, max_value=90, value=30)
    
    # データ生成
    df = generate_dummy_sleep_data(days_to_show)
    
    # 統計情報
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_sleep = df['total_sleep_hours'].mean()
        st.metric("平均睡眠時間", f"{avg_sleep:.1f}時間")
    
    with col2:
        avg_efficiency = df['sleep_efficiency'].mean()
        st.metric("平均睡眠効率", f"{avg_efficiency:.1f}%")
    
    with col3:
        avg_score = df['sleep_score'].mean()
        st.metric("平均睡眠スコア", f"{avg_score:.0f}点")
    
    with col4:
        avg_deep = df['deep_sleep_minutes'].mean()
        st.metric("平均深い睡眠", f"{avg_deep:.0f}分")
    
    st.markdown("---")
    
    # 睡眠パターンのタイムライン
    st.plotly_chart(create_sleep_timeline(df), use_container_width=True)
    
    # 2列レイアウト
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_sleep_stages_pie(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_sleep_heatmap(df), use_container_width=True)
    
    # トレンドチャート
    st.plotly_chart(create_sleep_trends(df), use_container_width=True)
    
    # データテーブル
    with st.expander("詳細データを表示"):
        st.dataframe(df.sort_values('date', ascending=False))

if __name__ == "__main__":
    main()