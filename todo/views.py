from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm

# Create your views here.
def todo_list(request):
    todos = Todo.objects.filter(complete=False)
    return render(request, 'todo/todo_list.html', {'todos':todos})
    #'todo':todos 라고 했다가 오류났음. 연결해준 todo_list.html에는 변수가 todos이기 때문.

def todo_detail(request, pk):
    todo = Todo.objects.get(id=pk)
    return render(request, 'todo/todo_detail.html', {'todo':todo})

def todo_post(request): #todo생성
    if request.method == "POST": #POST 요청이면
        form = TodoForm(request.POST)
        if form.is_valid(): #폼을 검증하고,
            todo = form.save(commit=False)
            todo.save() #데이터를 저장할 수 있도록 해줌
            return redirect('todo_list')
    else:
        form = TodoForm()
    #POST요청 중 폼의 값이 유효하지 않거나, POST 요청이 아니라면, 폼을 포함한 템플릿을 보여줌.
    return render(request, 'todo/todo_post.html', {'form':form})

def todo_edit(request, pk): #todo수정
    todo = Todo.objects.get(id=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_post.html', {'form':form})

def done_list(request): #완료된 Todo를 보여줌
    dones = Todo.objects.filter(complete=True) #Todo 객체중 complete가 True인 객체들을 가져옴.
    return render(request, 'todo/todo_done.html', {'dones':dones}) #해당 객체들을 done_list.html에 보냄

def todo_done(request, pk):#Todo를 완료상태로 변환.
    todo = Todo.objects.get(id=pk)
    todo.complete = True #Todo 객체의 complete를 True로 변경 
    todo.save() #DB에 저장
    return redirect('todo_list')

