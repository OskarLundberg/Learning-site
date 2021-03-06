from django.shortcuts import get_object_or_404, render

from .models import Course, Step


def course_list(request):
    courses = Course.objects.all()
    email = "questions@learningsite.com"
    return render(request, "courses/course_list.html", {"courses": courses, "email": email})


def course_detail(request, pk):
    # course = Course.objects.get(pk=pk)
    course = get_object_or_404(Course, pk=pk)
    step_count =  len(course.step_set.all())
    return render(request, "courses/course_detail.html", {"course": course, "step_count": step_count})


def step_detail(request, course_pk, step_pk):
    step = get_object_or_404(Step, course_id=course_pk, pk=step_pk)
    return render(request, "courses/step_detail.html", {"step": step})
