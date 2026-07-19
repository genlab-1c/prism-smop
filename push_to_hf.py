#!/usr/bin/env python3
"""Публикация датасета на HuggingFace: data/*.jsonl + карточка README.

HF-frontmatter (configs raw/sft, лицензия, размер) держим ОТДЕЛЬНО в `.hf_header.md`,
а НЕ в самом README.md — иначе YAML-блок «утекал» бы в GitHub и мусорил в карточке репо.
Здесь header приклеивается к README только на заливке в HF; git-README остаётся чистым.

Токен HF берётся из окружения (`HF_TOKEN`) или `~/.cache/huggingface/token`.

    python push_to_hf.py
"""

from pathlib import Path

from huggingface_hub import HfApi

REPO = "genlab-1c/prism-smop"
HERE = Path(__file__).resolve().parent


def main() -> None:
    header = HERE.joinpath(".hf_header.md").read_text(encoding="utf-8").rstrip() + "\n"
    body = HERE.joinpath("README.md").read_text(encoding="utf-8")
    if body.lstrip().startswith("---"):
        raise SystemExit("в git-README не должно быть frontmatter — он живёт в .hf_header.md")

    api = HfApi()
    # 1) файлы данных — как есть (служебные .hf_header.md / push_to_hf.py на HF не едут)
    api.upload_folder(
        folder_path=str(HERE),
        repo_id=REPO,
        repo_type="dataset",
        allow_patterns=["data/*.jsonl"],
        commit_message="Refresh dataset files",
    )
    # 2) README = frontmatter + тело (карточка HF с конфигами)
    api.upload_file(
        path_or_fileobj=(header + "\n" + body).encode("utf-8"),
        path_in_repo="README.md",
        repo_id=REPO,
        repo_type="dataset",
        commit_message="Refresh dataset card",
    )
    print(f"OK → https://huggingface.co/datasets/{REPO}")


if __name__ == "__main__":
    main()
