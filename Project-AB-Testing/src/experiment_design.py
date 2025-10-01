def design_experiment():
    """
    设计A/B测试实验方案
    """
    experiment_design = {
        "hypothesis": "修改小说详情页的'开始阅读'按钮颜色从蓝色改为红色可以提升点击率",
        "metric": "点击率(CTR)",
        "groups": {
            "control": "蓝色按钮(原版)",
            "treatment": "红色按钮(新版)"
        },
        "success_metric": "点击率提升至少2%且统计显著(p < 0.05)",
        "sample_size_per_group": 5000,  # 每组样本量
        "significance_level": 0.05,
        "test_duration": "7天"
    }
    return experiment_design

if __name__ == "__main__":
    design = design_experiment()
    print("实验设计:")
    for key, value in design.items():
        print(f"{key}: {value}")
