# data_cleaner.py
import pandas as pd
import numpy as np
import os

def load_data(filepath):
    """加载数据"""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath, parse_dates=['timestamp'])
    print(f"Original shape: {df.shape}")
    return df

def clean_data(df):
    """数据清洗函数"""
    print("Cleaning data...")
    df_clean = df.copy()
    
    # 处理重复值
    initial_count = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    print(f"Removed {initial_count - len(df_clean)} duplicate rows.")
    
    # 处理异常值：阅读时长大于0
    df_clean = df_clean[df_clean['read_time'] > 0]
    print(f"Removed rows with non-positive read_time. Current shape: {df_clean.shape}")
    
    return df_clean

def add_features(df):
    """添加衍生特征"""
    print("Adding features...")
    df_enriched = df.copy()
    
    # 衍生新特征
    df_enriched['date'] = df_enriched['timestamp'].dt.date
    df_enriched['hour'] = df_enriched['timestamp'].dt.hour
    df_enriched['day_of_week'] = df_enriched['timestamp'].dt.dayofweek
    
    return df_enriched

def save_clean_data(df, filename):
    """保存清洗后的数据"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Cleaned data saved to: {filename}")

if __name__ == "__main__":
    # 加载原始数据
    input_path = '../data/user_behavior_data.csv'
    df_raw = load_data(input_path)
    
    # 数据清洗
    df_clean = clean_data(df_raw)
    
    # 添加特征
    df_enriched = add_features(df_clean)
    
    # 保存清洗后的数据
    output_path = '../data/user_behavior_data_clean.csv'
    save_clean_data(df_enriched, output_path)
    
    # 显示清洗后的数据信息
    print("\nCleaned Data Info:")
    print(df_enriched.info())
    print("\nCleaned Data Description:")
    print(df_enriched.describe())
    
    print("\nData cleaning completed successfully!")
