class User:
    def __init__(self, user_id: int, name: str, username: str) -> None:
        self.user_id = user_id
        self.name = name
        self.language = "ENG"

    def __str__(self) -> str:
        return (f"{self.user_id}  "
                f"{self.name}  "
                f"{self.language}  ")
