from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment
from .forms import CourseForm, LessonForm

# --------------------------
# Courses
# --------------------------

@login_required(login_url='/users/login/')
def course_list(request):
    if not request.user.is_staff:
        return redirect('users:login')
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrolled = False
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'courses/course_detail.html', {'course': course, 'enrolled': enrolled})


@login_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_create.html', {'form': form})

@login_required
def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Seul l'instructeur peut modifier le cours
    if course.instructor != request.user:
        return redirect('course_detail', course_id=course.id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/course_update.html', {'form': form, 'course': course})


@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Seul l'instructeur peut supprimer
    if course.instructor != request.user:
        return redirect('course_detail', course_id=course.id)

    if request.method == "POST":
        course.delete()
        return redirect('course_list')

    return render(request, 'courses/course_delete.html', {'course': course})


# --------------------------
# Lessons
# --------------------------

@login_required
def lesson_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', course.id)
    else:
        form = LessonForm()

    return render(request, 'courses/lesson_form.html', {
        'form': form,
        'course': course,
        'title': "Ajouter une leçon"
    })
@login_required
def lesson_update(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)

    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('course_detail', lesson.course.id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'courses/lesson_form.html', {
        'form': form,
        'course': lesson.course,
        'title': "Modifier la leçon"
    })

@login_required
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    course_id = lesson.course.id
    lesson.delete()
    return redirect('course_detail', course_id)

@login_required
def lesson_detail(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})


# --------------------------
# Enrollment
# --------------------------

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('course_detail', course_id=course.id)
