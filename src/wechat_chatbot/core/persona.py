from pathlib import Path


def load_persona(directory: Path) -> str:
    """合并为一条 system 消息；修改模板后重启即可生效。"""
    names = ("IDENTITY.md", "SOUL.md", "USER.md", "MEMORY.md")
    sections = [f"## {name}\n{(directory / name).read_text(encoding='utf-8')}" for name in names]
    return "\n\n".join(sections)
