# main.py
import subprocess
import sys
import os

def run_script(script_name):
    """运行指定的Python脚本"""
    print(f"\n{'='*50}")
    print(f"Running {script_name}")
    print(f"{'='*50}")
    
    try:
        # 使用当前Python解释器运行脚本
        result = subprocess.run([sys.executable, script_name], check=True, cwd=os.path.dirname(__file__))
        print(f"{script_name} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        return False

if __name__ == "__main__":
    print("Starting Project 1: User Behavior Analysis")
    
    # 按顺序运行所有脚本
    scripts = ['data_generator.py', 'data_cleaner.py', 'analyzer.py']
    
    for script in scripts:
        if not run_script(script):
            print(f"Stopping due to error in {script}")
            break
    else:
        print("\n" + "="*50)
        print("All steps completed successfully!")
        print("="*50)
