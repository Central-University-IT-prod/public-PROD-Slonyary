from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database.models.base import AlchemyBaseModel


class Image(AlchemyBaseModel):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    base64: Mapped[str] = mapped_column(String, nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="cascade"),
        nullable=False,
    )

    post = relationship("Post", back_populates="images", lazy="joined")
