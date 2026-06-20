import json
from datetime import datetime
from pathlib import Path

#Dir for query logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "rag_logs.jsonl"


def log_query(query, answer, sources):

    #Store one JSON object per query
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "answer": answer,
        "sources_used": [
            {
                "source_type": source.get("source_type", ""),
                "title": source.get("title", ""),
                "url": source.get("url", ""),
                "rerank_score": source.get("rerank_score", None),
            }
            for source in sources
        ],
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")