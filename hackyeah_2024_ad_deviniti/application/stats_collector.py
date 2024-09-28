import datetime
from typing import Any, Dict

from pydantic import BaseModel


class LLMCallTokens(BaseModel):
    call_name: str
    llm_model_name: str
    prompt_tokens: int
    completion_tokens: int


class StatsCollector:
    _start_time: datetime.datetime
    stats: Dict[str, Any]
    _counter = 1

    def __init__(self) -> None:
        self._start_time = datetime.datetime.now()
        self.stats = dict()
        self.stats["tokens"] = []

    def duration(self) -> float:
        return (datetime.datetime.now() - self._start_time).total_seconds()

    def add_time_measure(self, name: str) -> None:
        self.stats[name] = self.duration()
        self.stats[f"{str(self._counter).rjust(2, '0')}_{name}"] = self.duration()
        self._counter += 1

    def add_property(self, name: str, value: Any) -> None:
        self.stats[name] = value

    def add_llm_tokens(self, tokens: LLMCallTokens) -> None:
        self.stats["tokens"].append(tokens.dict())
