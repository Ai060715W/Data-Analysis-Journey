# analyzer.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

def load_clean_data(filepath):
    """加载清洗后的数据"""
    print(f"Loading cleaned data from {filepath}...")
    df = pd.read_csv(filepath, parse_dates=['timestamp'])
    return df

def ensure_figures_dir():
    """确保figures目录存在"""
    figures_dir = '../data/figures/'
    os.makedirs(figures_dir, exist_ok=True)
    return figures_dir

def analyze_user_activity(df, figures_dir):
    """分析用户活跃度"""
    print("Analyzing user activity...")
    
    # 每日活跃用户数 (DAU)
    dau = df.groupby('date')['user_id'].nunique()
    plt.figure(figsize=(12, 6))
    dau.plot(kind='line', title='Daily Active Users (DAU) Trend', color='orange', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Number of Active Users')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{figures_dir}dau_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 用户每日阅读时段分布
    hourly_activity = df.groupby('hour').size()
    plt.figure(figsize=(10, 6))
    hourly_activity.plot(kind='bar', color='skyblue', title='User Activity by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Events')
    plt.tight_layout()
    plt.savefig(f'{figures_dir}hourly_activity.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'avg_dau': dau.mean(),
        'peak_hour': hourly_activity.idxmax()
    }

def analyze_content_preference(df, figures_dir):
    """分析内容偏好"""
    print("Analyzing content preference...")
    
    # 最受欢迎的书籍类别
    category_popularity = df['category'].value_counts()
    plt.figure(figsize=(10, 6))
    category_popularity.plot(kind='bar', color='lightgreen', title='Popularity of Book Categories')
    plt.xlabel('Book Category')
    plt.ylabel('Number of Events')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{figures_dir}category_popularity.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 不同类别的平均阅读时长
    category_read_time = df.groupby('category')['read_time'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    category_read_time.plot(kind='bar', color='salmon', title='Average Reading Time by Category (minutes)')
    plt.xlabel('Book Category')
    plt.ylabel('Average Reading Time (minutes)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{figures_dir}category_read_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'most_popular_category': category_popularity.index[0],
        'category_longest_read': category_read_time.index[0]
    }

def analyze_user_value(df, figures_dir):
    """分析用户价值"""
    print("Analyzing user value...")
    
    # 用户阅读总时长分布
    user_total_read_time = df.groupby('user_id')['read_time'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    user_total_read_time.hist(bins=50, color='purple', alpha=0.7)
    plt.title('Distribution of Total Reading Time per User')
    plt.xlabel('Total Reading Time (minutes)')
    plt.ylabel('Number of Users')
    plt.tight_layout()
    plt.savefig(f'{figures_dir}user_read_time_dist.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 用户分层 (基于阅读行为)
    user_activity = df.groupby('user_id').agg(
        total_events=('user_id', 'count'),
        total_read_time=('read_time', 'sum'),
        unique_books=('book_id', 'nunique')
    ).sort_values('total_read_time', ascending=False)
    
    # 定义用户分层
    user_activity['user_tier'] = pd.qcut(user_activity['total_read_time'], q=3, labels=['Low', 'Medium', 'High'])
    tier_distribution = user_activity['user_tier'].value_counts()
    
    # 高价值用户行为分析
    high_value_users = user_activity[user_activity['user_tier'] == 'High']
    
    return {
        'num_high_value_users': len(high_value_users),
        'tier_distribution': tier_distribution.to_dict()
    }

def analyze_action_types(df, figures_dir):
    """分析行为类型"""
    print("Analyzing action types...")
    
    action_counts = df['action_type'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(action_counts, labels=action_counts.index, autopct='%1.1f%%', startangle=90, 
            colors=['gold', 'lightcoral', 'lightskyblue'])
    plt.title('Distribution of Action Types')
    plt.savefig(f'{figures_dir}action_type_pie.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'action_distribution': action_counts.to_dict()
    }

def generate_report(insights):
    """生成分析报告"""
    print("\n" + "="*50)
    print("数据分析报告")
    print("="*50)
    
    for section, data in insights.items():
        print(f"\n{section.upper()}:")
        for k, v in data.items():
            print(f"  {k}: {v}")
    
    # 将报告保存到文件
    report_path = '../data/analysis_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("数据分析报告\n")
        f.write("="*50 + "\n")
        
        for section, data in insights.items():
            f.write(f"\n{section.upper()}:\n")
            for k, v in data.items():
                f.write(f"  {k}: {v}\n")
    
    print(f"\n完整报告已保存至: {report_path}")

if __name__ == "__main__":
    # 加载清洗后的数据
    input_path = '../data/user_behavior_data_clean.csv'
    df = load_clean_data(input_path)
    
    # 确保图表目录存在
    figures_dir = ensure_figures_dir()
    
    # 执行各项分析
    insights = {}
    
    insights['user_activity'] = analyze_user_activity(df, figures_dir)
    insights['content_preference'] = analyze_content_preference(df, figures_dir)
    insights['user_value'] = analyze_user_value(df, figures_dir)
    insights['action_types'] = analyze_action_types(df, figures_dir)
    
    # 生成并显示报告
    generate_report(insights)
    
    print("\nAnalysis completed successfully!")
