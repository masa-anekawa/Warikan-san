from dataclasses import dataclass

@dataclass
class Identity():
    """ユーザーの認証情報"""
    email: str
    hashed_password: str

    def __hash__(self) -> int:
        return hash(self.email)