from dataclasses import dataclass

from src.warikan_models.identity import Identity

@dataclass
class User():
    """ユーザー情報"""
    name: str
    identity: Identity

    def __hash__(self) -> int:
        return hash(self.identity)