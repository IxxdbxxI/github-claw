#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import sys
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo


@dataclass
class FeedSource:
    name: str
    url: str


SOURCES = [
    FeedSource(name="The Verge · AI", url="https://www.theverge.com/rss/ai/index.xml"),
    FeedSource(
        name="MIT Technology Review · AI",
        url="https://www.technologyreview.com/topic/artificial-intelligence/feed",
    ),
    FeedSource(name="OpenAI Blog", url="https://openai.com/blog/rss"),
]


def fetch_xml(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "github-actions-openclaw-digest"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def parse_datetime(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except (TypeError, ValueError):
        pass
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except ValueError:
        return None


def iter_items(root: ET.Element) -> list[dict]:
    items: list[dict] = []
    if root.tag.endswith("feed"):
        for entry in root.findall(".//{*}entry"):
            link_element = entry.find("{*}link[@rel='alternate']") or entry.find("{*}link")
            link_value = ""
            if link_element is not None:
                link_value = (link_element.get("href") or link_element.text or "").strip()
            items.append(
                {
                    "title": (entry.findtext("{*}title") or "").strip(),
                    "link": link_value,
                    "published": entry.findtext("{*}published")
                    or entry.findtext("{*}updated"),
                }
            )
    else:
        for item in root.findall(".//item"):
            items.append(
                {
                    "title": (item.findtext("title") or "").strip(),
                    "link": (item.findtext("link") or "").strip(),
                    "published": item.findtext("pubDate")
                    or item.findtext("{http://purl.org/dc/elements/1.1/}date")
                    or item.findtext("{http://www.w3.org/2005/Atom}updated"),
                }
            )
    return items


def safe_link(entry: dict) -> str:
    if entry.get("link"):
        return entry["link"]
    return ""


def build_digest(output_path: str, title_path: str) -> None:
    now_utc = dt.datetime.now(dt.timezone.utc)
    week_start = now_utc - dt.timedelta(days=7)
    now_bjt = now_utc.astimezone(ZoneInfo("Asia/Shanghai"))
    items: list[dict] = []
    errors: list[str] = []

    for source in SOURCES:
        try:
            payload = fetch_xml(source.url)
            root = ET.fromstring(payload)
            for entry in iter_items(root):
                title = entry.get("title") or ""
                link = safe_link(entry)
                published = parse_datetime(entry.get("published"))
                if not title or not link:
                    continue
                if published and published < week_start:
                    continue
                items.append(
                    {
                        "title": title,
                        "link": link,
                        "published": published,
                        "source": source.name,
                    }
                )
        except Exception as exc:
            errors.append(f"{source.name}: {exc}")

    seen_links: set[str] = set()
    unique_items: list[dict] = []
    for item in sorted(
        items,
        key=lambda i: i["published"] or now_utc,
        reverse=True,
    ):
        if item["link"] in seen_links:
            continue
        seen_links.add(item["link"])
        unique_items.append(item)

    title = f"推送日报 | AI 科技热点周报 | {now_bjt:%Y-%m-%d}"
    lines = [
        "# 推送日报 | AI 科技热点周报",
        f"- 生成时间：{now_bjt:%Y-%m-%d %H:%M}（北京时间）",
        "- 覆盖范围：最近 7 天",
        "- 数据源：" + "、".join(source.name for source in SOURCES),
        "",
        "## 本周热点",
    ]

    if unique_items:
        for index, item in enumerate(unique_items[:12], start=1):
            published = (
                item["published"].astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")
                if item["published"]
                else "未知时间"
            )
            lines.append(
                f"{index}. [{item['title']}]({item['link']}) — {item['source']} — {published}"
            )
    else:
        lines.append("本周暂无抓取到的热点条目。")

    if errors:
        lines.extend(
            [
                "",
                "## 抓取异常",
                "以下数据源抓取失败（不影响其余内容生成）：",
            ]
        )
        lines.extend(f"- {error}" for error in errors)

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(lines).strip() + "\n")
    with open(title_path, "w", encoding="utf-8") as title_file:
        title_file.write(title)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate weekly AI digest.")
    parser.add_argument("--output", required=True, help="Path to digest markdown file.")
    parser.add_argument("--title-out", required=True, help="Path to title text file.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    build_digest(args.output, args.title_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
