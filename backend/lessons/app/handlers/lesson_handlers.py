from typing import Any

from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.app.utils.pagination import paginate
from lessons.app.http.requests.lesson_requests import (
    LessonFilterRequest,
    LessonCreateRequest,
)
from lessons.app.http.resources.lesson_resources import LessonResource
from lessons.app.repositories.lesson_repository import LessonRepository
from lessons.app.services.lesson_service import LessonCreator


class LessonsFilterHandler(GenericAPIView):
    serializer_class = LessonFilterRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data, partial=True)
        data.is_valid(raise_exception=True)

        lessons = LessonRepository().filter(data=data.validated_data)

        return Response(
            paginate(data=lessons, request=self.request, resource=LessonResource)
        )


@permission_classes([IsAuthenticated])  # TODO Add IsTeacher permission
class LessonCreateHandler(GenericAPIView):
    serializer_class = LessonCreateRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        lesson = LessonCreator(
            data=data.validated_data, user=self.request.user
        ).create()

        return Response({"data": LessonResource(lesson).data})
