from fastapi import HTTPException, status


class LikeAlreadyGivenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already liked this post.",
        )
