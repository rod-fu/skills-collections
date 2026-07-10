#!/usr/bin/env python3
import argparse
import datetime as dt
import json

PPT_STYLES = {
    "bold": [
        "新瑞士大字报 Neo-Swiss Billboard",
        "黑底数字剧场 Black Big-Number Stage",
        "高饱和单色撞色海报 Mono-Brand Type-as-Hero",
        "全幅渐变宣言 Full-Bleed Gradient Manifesto",
        "CS50 单概念糖果舞台 Candy-Color Lecture Stage",
        "玩味手绘极简 Playful Maximalist Editorial",
        "不羁玩梗流行版 Irreverent Pop",
        "Y2K 膨胀大字 Maximalist 3D-Type",
    ],
    "neutral": [
        "Bento 便当格模块网格 Bento Grid",
        "Neo-Swiss 暗色终端 Dark Hairline Terminal",
        "双字体咨询版 Two-Font Consulting",
        "图谱箭头企业版 Diagram-Driven Isotype",
        "单图母图概念图解 Diagrammatic Minimalism",
        "Sparkline 叙事波形 Narrative Sparkline",
    ],
    "quiet": [
        "断言-证据 Assertion-Evidence",
        "瑞士机构极简 Institutional Swiss Minimal",
        "杂志编辑长文流 Editorial Longform",
        "人文圆角卡片 Humanist Rounded Cards",
        "研报密集图表 Dense Research Report",
        "纯文字宣言备忘录 All-Text Manifesto",
    ],
}


def normalize_temperature(value):
    mapping = {
        "大胆": "bold",
        "bold": "bold",
        "中性": "neutral",
        "neutral": "neutral",
        "安静": "quiet",
        "quiet": "quiet",
    }
    return mapping.get((value or "").strip().lower(), "neutral")


def main():
    parser = argparse.ArgumentParser(description="Pick a Huashu Design PPT style.")
    parser.add_argument("--temperature", default="neutral", help="大胆/bold, 中性/neutral, 安静/quiet")
    parser.add_argument("--second", type=int, help="Override clock second for deterministic tests.")
    args = parser.parse_args()

    temp = normalize_temperature(args.temperature)
    styles = PPT_STYLES[temp]
    second = args.second if args.second is not None else dt.datetime.now().second
    selected = styles[second % len(styles)]
    print(json.dumps({
        "视觉温度": {"bold": "大胆", "neutral": "中性", "quiet": "安静"}[temp],
        "方案A_秒数轮盘": selected,
        "方案B_现实参照": "对标 McKinsey/Sequoia 的高密度结构页，强调证据链和清晰判断句。",
        "方案C_最佳设计师": "假设预算无上限，迁移 Pentagram/原研哉式的母题提炼与克制留白。",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
