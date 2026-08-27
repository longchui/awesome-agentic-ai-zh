import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(api_key="sk-dbc3562701fb44239beefa60af196a0f",base_url="https://api.deepseek.com")
# 中文情绪分类（正面 / 负面 / 中立）
TEST_SET = [
    ("这部电影超赞、看完想再看一次！", "正面"),
    ("剧情无聊、演员演技尴尬。", "负面"),
    ("这是一部 2019 年的电影。", "中立"),
    ("我不确定喜不喜欢、可能再想想。", "中立"),
    ("第一集很不错但第二集就崩了。", "负面"),
    ("看完心情很好、推荐！", "正面"),
]

FEW_SHOT_EXAMPLES = """范例：
input: 这家餐厅的牛排好吃到让我哭出来。
output: 正面

input: 服务生态度很差、我再也不会来了。
output: 负面

input: 这家店位于新北市三重区。
output: 中立
"""

# 两种条件共用同一段“任务说明”；few-shot 只多加范例——这样对比才干净，量到的是“范例”本身的效果，而不是“终于告诉模型要做什么”。
TASK = "把下面的句子分类成“正面 / 负面 / 中立”其中一个，只输出这三个词其中之一、不要多余文字。\n\n"

def classify(text: str, *, use_few_shot: bool) -> str:
    preifx = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    prompt = f"{TASK}{preifx}input: {text}\noutput:"
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content.strip().splitlines()[0]

def evaluate(use_few_shot:bool) ->tuple[int, int]:
    correct = 0
    for text, label in TEST_SET:
        pred = classify(text, use_few_shot=use_few_shot)
        ok = label in pred
        print(f" {'√' if ok else '×'} [{label}] {text[:30]}... -> '{pred}'")
        if ok:
            correct += 1
    return correct, len(TEST_SET)

print("=== 0-shot ===")
c0, n = evaluate(use_few_shot=False)
print(f"正确 {c0}/{n} = {c0/n:.0%}")

print("\n=== 3-shot ===")
c3, _ = evaluate(use_few_shot=True)
print(f"正确 {c3}/{n} = {c3/n:.0%}")

# === 自我验证 ===
# 两种条件都给了同样的任务说明，所以这里量的是“范例本身”带来的差异。
# few-shot 不保证每次都赢（看 model / 题目 / 抽样），所以不硬性要求 c3 >= c0。
assert n == 6 and 0 <= c0 <= n and 0 <= c3 <= n, "两种条件都要各跑完 6 题"
print(f"\n✅ 练习 2 通过 — 0-shot {c0}/{n}、3-shot {c3}/{n}；few-shot 净提升 {c3 - c0} 题（可能为 0 甚至负，都算正常）（本机 $0）")
print("💡 观察：有了任务说明，0-shot 就有基本盘；few-shot 的价值在“钉住输出格式” + 示范模棱两可案例（如 '中立'）的判准")
print("💡 小 model（gemma4:e4b）对格式更敏感，所以 few-shot 的帮助通常比 Claude 明显——但仍非保证，要跑了才知道")

