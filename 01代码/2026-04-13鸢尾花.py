# ===== 鸢尾花分类 ·  (已修复) =====
from sklearn.datasets import load_iris
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
# 修复报错：需要导入 classification_report
from sklearn.metrics import classification_report

# 1. 加载数据
# 修复报错：这里必须加括号 () 调用函数，并赋值给变量 iris
iris = load_iris()
X, y = iris.data, iris.target

# 2. 划分数据：80%训练，20%测试 (random_state=42保证结果可复现)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 参数实验区 ---
# 你可以切换下面三组参数来观察效果：

# 实验1：小脑子+短训练 (欠拟合风险)
# model = MLPClassifier(hidden_layer_sizes=(3,), max_iter=100, random_state=42)

# 实验2：标准配置 (推荐)
# model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000, random_state=42)

# 实验3：大脑子+长训练 (过拟合风险)
model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=5000, random_state=42)

# 3. 训练模型 (fit是监督学习核心接口)
model.fit(X_train, y_train)

# 4. 评估准确率 (score返回测试集准确率)
accuracy = model.score(X_test, y_test)
print(f"✅ 模型准确率: {accuracy:.2%}")

# 5. 输出详细报告 
# 第一步：必须先让模型去“猜”结果，存入 y_pred
y_pred = model.predict(X_test)

# 第二步：打印报告
# 注意：target_names 必须从 iris 实例中获取 (iris.target_names)，不能用 load_iris.target_names
print("\n📊 详细分类报告:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))
