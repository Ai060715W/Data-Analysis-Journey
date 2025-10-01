import numpy as np
import pandas as pd
from scipy import stats
import json

def load_data(file_path):
    """加载处理后的数据"""
    return pd.read_csv(file_path)

def calculate_click_rates(df):
    """计算各组的点击率"""
    results = df.groupby('group')['clicked'].agg([
        ('count', 'count'),
        ('clicks', 'sum'),
        ('ctr', 'mean')
    ]).round(4)
    
    return results

def chi_square_test(df):
    """执行卡方检验"""
    # 创建列联表
    contingency_table = pd.crosstab(df['group'], df['clicked'])
    
    # 执行卡方检验
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    return {
        'chi2_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': dof,
        'expected_frequencies': expected.tolist()
    }

def calculate_confidence_interval(clicks_a, total_a, clicks_b, total_b, alpha=0.05):
    """计算两组比例差的置信区间"""
    p_a = clicks_a / total_a
    p_b = clicks_b / total_b
    
    # 计算比例差
    diff = p_b - p_a
    
    # 计算标准误
    se = np.sqrt(p_a * (1 - p_a) / total_a + p_b * (1 - p_b) / total_b)
    
    # 计算Z分数
    z_score = stats.norm.ppf(1 - alpha/2)
    
    # 计算置信区间
    margin_of_error = z_score * se
    ci_lower = diff - margin_of_error
    ci_upper = diff + margin_of_error
    
    return {
        'difference': diff,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'margin_of_error': margin_of_error,
        'relative_improvement': (p_b - p_a) / p_a
    }

def manual_power_analysis(control_ctr, treatment_ctr, sample_size, alpha=0.05, n_simulations=10000):
    """
    手动实现统计功效分析通过模拟
    
    参数:
    control_ctr: 控制组真实点击率
    treatment_ctr: 实验组真实点击率  
    sample_size: 每组样本量
    alpha: 显著性水平
    n_simulations: 模拟次数
    """
    significant_results = 0
    
    for _ in range(n_simulations):
        # 模拟控制组数据
        control_clicks = np.random.binomial(sample_size, control_ctr)
        
        # 模拟实验组数据
        treatment_clicks = np.random.binomial(sample_size, treatment_ctr)
        
        # 创建列联表
        control_no_clicks = sample_size - control_clicks
        treatment_no_clicks = sample_size - treatment_clicks
        
        contingency_table = np.array([
            [control_clicks, control_no_clicks],
            [treatment_clicks, treatment_no_clicks]
        ])
        
        # 执行卡方检验
        _, p_value, _, _ = stats.chi2_contingency(contingency_table)
        
        # 检查是否显著
        if p_value < alpha:
            significant_results += 1
    
    # 计算统计功效
    power = significant_results / n_simulations
    
    return {
        'power': power,
        'n_simulations': n_simulations,
        'significant_detections': significant_results
    }

def calculate_effect_size(control_ctr, treatment_ctr):
    """计算效应量 (Cohen's h)"""
    # 对比例数据使用反正弦变换
    h = 2 * (np.arcsin(np.sqrt(treatment_ctr)) - np.arcsin(np.sqrt(control_ctr)))
    return abs(h)

def comprehensive_analysis(df):
    """执行全面的统计分析"""
    # 基础点击率计算
    click_rates = calculate_click_rates(df)
    
    # 提取数据用于后续计算
    control_data = df[df['group'] == 'control']['clicked']
    treatment_data = df[df['group'] == 'treatment']['clicked']
    
    control_clicks = control_data.sum()
    control_total = len(control_data)
    treatment_clicks = treatment_data.sum()
    treatment_total = len(treatment_data)
    
    # 假设检验
    chi2_results = chi_square_test(df)
    
    # 置信区间
    ci_results = calculate_confidence_interval(
        control_clicks, control_total, 
        treatment_clicks, treatment_total
    )
    
    # 统计功效分析
    power_results = manual_power_analysis(
        control_ctr=click_rates.loc['control', 'ctr'],
        treatment_ctr=click_rates.loc['treatment', 'ctr'],
        sample_size=min(control_total, treatment_total),
        n_simulations=5000  # 减少模拟次数以提高速度
    )
    
    # 效应量计算
    effect_size = calculate_effect_size(
        click_rates.loc['control', 'ctr'],
        click_rates.loc['treatment', 'ctr']
    )
    
    # 汇总结果
    comprehensive_results = {
        'click_rates': click_rates.to_dict(),
        'chi_square_test': chi2_results,
        'confidence_intervals': ci_results,
        'power_analysis': power_results,
        'effect_size': effect_size,
        'sample_sizes': {
            'control': control_total,
            'treatment': treatment_total
        }
    }
    
    return comprehensive_results

def save_statistical_results(results, output_path):
    """保存统计结果到JSON文件"""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    # 加载数据
    df = load_data('../data/processed/ab_test_clean_data.csv')
    
    # 执行分析
    results = comprehensive_analysis(df)
    
    # 保存结果
    save_statistical_results(results, '../results/statistical_results.json')
    
    print("统计分析完成!")
    print(f"控制组CTR: {results['click_rates']['ctr']['control']:.3f}")
    print(f"实验组CTR: {results['click_rates']['ctr']['treatment']:.3f}")
    print(f"P值: {results['chi_square_test']['p_value']:.6f}")
    print(f"统计功效: {results['power_analysis']['power']:.3f}")
