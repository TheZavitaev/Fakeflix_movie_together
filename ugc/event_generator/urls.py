from enum import Enum


class DataType(Enum):
    VIEW = "views"
    REVIEW = "reviews"
    FILM_LIKE = "film_likes"
    REVIEW_LIKE = "review_likes"
    BOOKMARK = "bookmarks"


urlpatterns = {
    DataType.VIEW.value: "/api/v1/movie-progress/",
    DataType.REVIEW.value: "/api/v1/users/{user_id}/reviews/",
    DataType.FILM_LIKE.value: "/api/v1/users/{user_id}/ratings/",
    DataType.REVIEW_LIKE.value: "/api/v1/users/{user_id}/reviews/{review_id}/ratings/",
    DataType.BOOKMARK.value: "/api/v1/users/{user_id}/bookmarks/",
}
