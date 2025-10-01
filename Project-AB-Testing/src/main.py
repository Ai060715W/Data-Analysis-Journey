import os
import sys
from data_generator import generate_ab_test_data, save_data
from statistical_analysis import comprehensive_analysis, save_statistical_results, load_data
from visualization import (plot_click_rates_comparison, plot_confidence_intervals, 
                         plot_power_analysis, create_sample_power_curve)
from experiment_design import design_experiment

def ensure_directories():
    """确保所有需要的目录都存在"""
    directories = [
        '../data/raw',
        '../data/processed', 
        '../results/figures'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def generate_report(statistical_results):
    """生成详细的A/B测试报告"""
    
    report = f"""
# A/B测试分析报告

## 实验概述
**假设**: 修改小说详情页的"开始阅读"按钮颜色从蓝色改为红色可以提升点击率

## 关键结果

### 点击率表现
- **控制组(蓝色按钮) CTR**: {statistical_results['click_rates']['ctr']['control']:.3%}
- **实验组(红色按钮) CTR**: {statistical_results['click_rates']['ctr']['treatment']:.3%}
- **绝对提升**: {statistical_results['confidence_intervals']['difference']:.3%}
- **相对提升**: {statistical_results['confidence_intervals']['relative_improvement']:.1%}

### 统计显著性
- **P值**: {statistical_results['chi_square_test']['p_value']:.6f}
- **统计显著性**: {'是' if statistical_results['chi_square_test']['p_value'] < 0.05 else '否'}

### 效果估计
- **效应量 (Cohen\'s h)**: {statistical_results['effect_size']:.3f}
- **95% 置信区间**: [{statistical_results['confidence_intervals']['ci_lower']:.4f}, {statistical_results['confidence_intervals']['ci_upper']:.4f}]

### 统计功效
- **当前功效**: {statistical_results['power_analysis']['power']:.3f}
- **模拟次数**: {statistical_results['power_analysis']['n_simulations']}

## 业务建议

{'✅ **推荐实施**: 实验结果显示统计显著的提升，建议全面推广红色按钮。' 
 if statistical_results['chi_square_test']['p_value'] < 0.05 and statistical_results['confidence_intervals']['difference'] > 0 
 else '❌ **不推荐实施**: 实验结果不显著或为负向，建议保持原方案或重新设计实验。'}

## 后续步骤
1. 监控长期效果，确保提升的持续性
2. 考虑在不同用户细分中分析效果差异
3. 设计后续实验进一步优化用户体验
"""

    return report

def main():
    """主函数"""
    print("🚀 开始A/B测试分析流程...")
    
    # 确保目录存在
    ensure_directories()
    
    # 步骤1: 实验设计
    print("\n📋 步骤1: 实验设计")
    design = design_experiment()
    print("实验设计完成")
    
    # 步骤2: 生成数据
    print("\n📊 步骤2: 生成模拟数据")
    df_raw = generate_ab_test_data()
    df_processed = save_data(
        df_raw,
        '../data/raw/ab_test_raw_data.csv',
        '../data/processed/ab_test_clean_data.csv'
    )
    print(f"数据生成完成，共{len(df_raw)}条记录")
    
    # 步骤3: 统计分析
    print("\n📈 步骤3: 统计分析")
    df = load_data('../data/processed/ab_test_clean_data.csv')
    statistical_results = comprehensive_analysis(df)
    save_statistical_results(statistical_results, '../results/statistical_results.json')
    print("统计分析完成")
    
    # 步骤4: 可视化
    print("\n🎨 步骤4: 生成可视化图表")
    plot_click_rates_comparison(df, '../results/figures/click_rates_comparison.png')
    plot_confidence_intervals(df, '../results/figures/confidence_intervals.png')
    
    sample_sizes, power_levels = create_sample_power_curve()
    plot_power_analysis(sample_sizes, power_levels, '../results/figures/power_analysis.png')
    print("可视化完成")
    
    # 步骤5: 生成报告
    print("\n📝 步骤5: 生成分析报告")
    report = generate_report(statistical_results)
    
    with open('../results/ab_test_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("分析报告已保存至: ../results/ab_test_report.md")
    
    # 输出关键结果
    print("\n" + "="*50)
    print("🎯 A/B测试关键结果摘要")
    print("="*50)
    print(f"控制组CTR: {statistical_results['click_rates']['ctr']['control']:.3%}")
    print(f"实验组CTR: {statistical_results['click_rates']['ctr']['treatment']:.3%}")
    print(f"提升幅度: {statistical_results['confidence_intervals']['difference']:.3%}")
    print(f"P值: {statistical_results['chi_square_test']['p_value']:.6f}")
    print(f"统计显著性: {'是' if statistical_results['chi_square_test']['p_value'] < 0.05 else '否'}")
    print(f"统计功效: {statistical_results['power_analysis']['power']:.3f}")
    
    # 给出决策建议
    if statistical_results['chi_square_test']['p_value'] < 0.05 and statistical_results['confidence_intervals']['difference'] > 0:
        print("\n✅ 建议: 实验结果统计显著且正向，推荐实施新方案")
    else:
        print("\n❌ 建议: 实验结果不显著或负向，建议保持原方案")

if __name__ == "__main__":
    main()
