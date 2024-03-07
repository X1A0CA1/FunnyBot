from pyrogram.types.user_and_chats.user import User, Link

from utils import contains_only_special_whitespace


def full_name(self) -> str:
    if self.last_name:
        fullname = f"{self.first_name} {self.last_name}"
    else:
        fullname = self.first_name
    if contains_only_special_whitespace(fullname):
        fullname = "潇洒的互联网高隐私行者"
    return fullname


def mention(self) -> Link:
    return Link(
        f"tg://user?id={self.id}",
        self.full_name or "Deleted Account",
        self._client.parse_mode
    )


# noinspection DuplicatedCode
def __eq__(self, other) -> bool:
    if isinstance(other, User):
        return self.id == other.id
    else:
        return False


setattr(User, "full_name", property(full_name))
setattr(User, "mention", property(mention))
setattr(User, "__eq__", __eq__)
