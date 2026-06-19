from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# 示例关联数据
SAMPLE_URL = "https://officialapp-leyu.com.cn"
SAMPLE_KEYWORD = "乐鱼体育"


@dataclass
class KeywordNote:
    """关键词笔记数据模型"""
    keyword: str
    source_url: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    priority: int = 0  # 0=普通, 1=重要, 2=紧急

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "source_url": self.source_url,
            "note": self.note,
            "tags": self.tags,
            "created_at": self.created_at,
            "priority": self.priority,
        }


@dataclass
class KeywordNoteCollection:
    """关键词笔记集合"""
    notes: List[KeywordNote] = field(default_factory=list)
    title: str = "默认笔记集"

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def filter_by_priority(self, min_priority: int = 1) -> List[KeywordNote]:
        return [n for n in self.notes if n.priority >= min_priority]

    def search(self, keyword_fragment: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword_fragment.lower() in n.keyword.lower()]


def format_single_note(note: KeywordNote) -> str:
    """格式化输出单条笔记"""
    priority_map = {0: "普通", 1: "重要", 2: "紧急"}
    lines = [
        f"【关键词】{note.keyword}",
        f"【来源】{note.source_url}",
        f"【备注】{note.note}" if note.note else "",
        f"【标签】{', '.join(note.tags)}" if note.tags else "",
        f"【时间】{note.created_at}",
        f"【优先级】{priority_map.get(note.priority, '未知')}",
    ]
    return "\n".join(line for line in lines if line)


def format_collection_summary(collection: KeywordNoteCollection) -> str:
    """格式化输出笔记集合摘要"""
    total = len(collection.notes)
    important = len([n for n in collection.notes if n.priority >= 1])
    tags_used = set()
    for n in collection.notes:
        tags_used.update(n.tags)
    summary = [
        f"笔记集标题: {collection.title}",
        f"总笔记数: {total}",
        f"重要笔记数: {important}",
        f"涉及标签数: {len(tags_used)}",
        f"标签列表: {', '.join(sorted(tags_used)) if tags_used else '无'}",
    ]
    return "\n".join(summary)


def format_all_notes_simple(collection: KeywordNoteCollection) -> str:
    """简易列表形式输出所有笔记"""
    parts = []
    for idx, note in enumerate(collection.notes, 1):
        parts.append(f"{idx}. {note.keyword} [{', '.join(note.tags)}] (优先级{note.priority})")
    return "\n".join(parts)


def create_sample_collection() -> KeywordNoteCollection:
    """创建包含示例数据的笔记集合"""
    collection = KeywordNoteCollection(title="乐鱼体育相关笔记")

    note1 = KeywordNote(
        keyword="乐鱼体育",
        source_url=SAMPLE_URL,
        note="官方主站，提供体育赛事资讯与平台入口",
        tags=["体育", "官方"],
        priority=2,
    )

    note2 = KeywordNote(
        keyword="乐鱼体育 赛事",
        source_url=f"{SAMPLE_URL}/events",
        note="最新赛事列表与赛程安排",
        tags=["体育", "赛事"],
        priority=1,
    )

    note3 = KeywordNote(
        keyword="乐鱼体育 直播",
        source_url=f"{SAMPLE_URL}/live",
        note="高清体育直播频道",
        tags=["直播", "体育"],
        priority=1,
    )

    note4 = KeywordNote(
        keyword="乐鱼体育 新闻",
        source_url=f"{SAMPLE_URL}/news",
        note="体育新闻与深度报道",
        tags=["新闻", "体育"],
        priority=0,
    )

    for note in [note1, note2, note3, note4]:
        collection.add_note(note)

    return collection


def main() -> None:
    """主运行入口：演示笔记创建、过滤与格式化输出"""
    collection = create_sample_collection()

    print("=== 所有笔记（列表） ===")
    print(format_all_notes_simple(collection))
    print()

    print("=== 摘要 ===")
    print(format_collection_summary(collection))
    print()

    print("=== 重要笔记（优先级 >= 1） ===")
    for note in collection.filter_by_priority(1):
        print(format_single_note(note))
        print("---")

    print("=== 标签为'直播'的笔记 ===")
    for note in collection.filter_by_tag("直播"):
        print(format_single_note(note))
        print("---")

    print("=== 搜索关键词包含'新闻'的笔记 ===")
    for note in collection.search("新闻"):
        print(format_single_note(note))
        print("---")


if __name__ == "__main__":
    main()