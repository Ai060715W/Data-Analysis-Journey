import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_ab_test_data(control_ctr=0.08, treatment_ctr=0.105, n_users=10000):
    """
    生成A/B测试模拟数据
    
    参数:
    control_ctr: 控制组点击率 (8%)
    treatment_ctr: 实验组点击率 (10.5%)
    n_users: 总用户数
    """
    np.random.seed(42)  # 确保结果可重现
    
    # 生成用户ID
    user_ids = [f"user_{i:06d}" for i in range(n_users)]
    
    # 随机分配到控制组和实验组
    groups = np.random.choice(['control', 'treatment'], size=n_users, p=[0.5, 0.5])
    
    # 根据分组生成点击数据
    clicks = []
    for group in groups:
        if group == 'control':
            click = np.random.binomial(1, control_ctr)
        else:
            click = np.random.binomial(1, treatment_ctr)
        clicks.append(click)
    
    # 生成时间戳（模拟7天数据）
    start_date = datetime(2024, 1, 1)
    timestamps = []
    for i in range(n_users):
        random_days = np.random.randint(0, 7)
        random_hours = np.random.randint(0, 24)
        timestamp = start_date + timedelta(days=random_days, hours=random_hours)
        timestamps.append(timestamp)
    
    # 创建DataFrame
    df = pd.DataFrame({
        'user_id': user_ids,
        'timestamp': timestamps,
        'group': groups,
        'clicked': clicks
    })
    
    return df

def save_data(df, raw_path, processed_path):
    """保存原始和处理后的数据"""
    # 保存原始数据
    df.to_csv(raw_path, index=False)
    
    # 数据清洗和处理
    df_clean = df.copy()
    df_clean['date'] = pd.to_datetime(df_clean['timestamp']).dt.date
    df_clean['hour'] = pd.to_datetime(df_clean['timestamp']).dt.hour
    
    # 保存处理后的数据
    df_clean.to_csv(processed_path, index=False)
    
    return df_clean

if __name__ == "__main__":
    # 生成数据
    df_raw = generate_ab_test_data()
    df_processed = save_data(
        df_raw, 
        '../data/raw/ab_test_raw_data.csv',
        '../data/processed/ab_test_clean_data.csv'
    )
    
    print(f"生成数据完成，共{len(df_raw)}条记录")
    print("数据概览:")
    print(df_processed.groupby('group')['clicked'].agg(['count', 'mean']))
