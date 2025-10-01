import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from statistical_analysis import load_data, calculate_click_rates, calculate_confidence_interval

def setup_plot_style():
    """设置绘图样式"""
    plt.style.use('default')
    sns.set_palette("husl")
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False

def plot_click_rates_comparison(df, save_path=None):
    """绘制点击率对比图"""
    setup_plot_style()
    
    click_rates = calculate_click_rates(df)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 柱状图
    groups = ['控制组(蓝色)', '实验组(红色)']
    ctr_values = [click_rates.loc['control', 'ctr'], click_rates.loc['treatment', 'ctr']]
    
    bars = ax1.bar(groups, ctr_values, color=['#1f77b4', '#d62728'], alpha=0.7)
    ax1.set_ylabel('点击率 (CTR)')
    ax1.set_title('A/B测试点击率对比')
    ax1.grid(True, alpha=0.3)
    
    # 在柱子上添加数值标签
    for bar, value in zip(bars, ctr_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                f'{value:.3f}', ha='center', va='bottom')
    
    # 饼图显示点击分布
    total_clicks = click_rates['clicks'].sum()
    total_impressions = click_rates['count'].sum()
    no_clicks = total_impressions - total_clicks
    
    labels = ['点击', '未点击']
    sizes = [total_clicks, no_clicks]
    colors = ['#ff9999', '#66b3ff']
    
    ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('总体点击分布')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"点击率对比图已保存至: {save_path}")
    
    plt.show()

def plot_confidence_intervals(df, save_path=None):
    """绘制置信区间图"""
    setup_plot_style()
    
    # 计算置信区间
    control_data = df[df['group'] == 'control']['clicked']
    treatment_data = df[df['group'] == 'treatment']['clicked']
    
    control_clicks = control_data.sum()
    control_total = len(control_data)
    treatment_clicks = treatment_data.sum()
    treatment_total = len(treatment_data)
    
    ci_results = calculate_confidence_interval(
        control_clicks, control_total, 
        treatment_clicks, treatment_total
    )
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制点估计和置信区间
    point = ci_results['difference']
    lower = ci_results['ci_lower']
    upper = ci_results['ci_upper']
    
    ax.errorbar(x=point, y=0, xerr=[[point - lower], [upper - point]], 
                fmt='o', color='black', capsize=5, capthick=2, markersize=8)
    
    # 添加参考线
    ax.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='无效果线')
    ax.axvline(x=point, color='blue', linestyle='-', alpha=0.5, label=f'估计效果: {point:.4f}')
    
    # 填充置信区间
    ax.axvspan(lower, upper, alpha=0.2, color='gray', label='95% 置信区间')
    
    ax.set_yticks([])
    ax.set_xlabel('点击率差异 (实验组 - 控制组)')
    ax.set_title('A/B测试效果估计与置信区间')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 添加统计显著性标注
    if lower > 0:
        significance = "统计显著"
        color = "green"
    else:
        significance = "不显著" 
        color = "red"
    
    ax.text(0.5, 0.9, f'效果: {significance}', transform=ax.transAxes, 
            color=color, fontsize=12, ha='center', weight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"置信区间图已保存至: {save_path}")
    
    plt.show()

def plot_power_analysis(sample_sizes, power_levels, save_path=None):
    """绘制统计功效分析图"""
    setup_plot_style()
    
    plt.figure(figsize=(10, 6))
    plt.plot(sample_sizes, power_levels, 'bo-', linewidth=2, markersize=6)
    plt.axhline(y=0.8, color='red', linestyle='--', alpha=0.7, label='目标功效 (0.8)')
    plt.axhline(y=0.9, color='orange', linestyle='--', alpha=0.7, label='高功效 (0.9)')
    
    plt.xlabel('每组样本量')
    plt.ylabel('统计功效')
    plt.title('样本量与统计功效关系')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # 标注常见样本量对应的功效
    for i, (size, power) in enumerate(zip(sample_sizes, power_levels)):
        if size in [1000, 5000, 10000]:
            plt.annotate(f'{power:.2f}', (size, power), 
                        textcoords="offset points", xytext=(0,10), ha='center')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"功效分析图已保存至: {save_path}")
    
    plt.show()

def create_sample_power_curve():
    """创建样本功效曲线示例数据"""
    # 这里使用简化版的功效计算
    sample_sizes = [500, 1000, 2000, 5000, 8000, 10000, 15000, 20000]
    power_levels = [0.25, 0.45, 0.68, 0.89, 0.95, 0.97, 0.99, 0.995]
    
    return sample_sizes, power_levels

if __name__ == "__main__":
    # 加载数据
    df = load_data('../data/processed/ab_test_clean_data.csv')
    
    # 生成所有图表
    plot_click_rates_comparison(df, '../results/figures/click_rates_comparison.png')
    plot_confidence_intervals(df, '../results/figures/confidence_intervals.png')
    
    # 生成功效分析图
    sample_sizes, power_levels = create_sample_power_curve()
    plot_power_analysis(sample_sizes, power_levels, '../results/figures/power_analysis.png')
