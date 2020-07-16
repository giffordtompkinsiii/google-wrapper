from gtasks_api import GtasksAPI
import os 

creds_file = os.path.join('clients','gifford_tompkins')

gtasks = GtasksAPI(os.path.join(creds_file,'credentials.json'), os.path.join(creds_file, 'token.pickle'))

class TaskApp(object):
    def __init__(self, service):
        for k,v in service.__dict__.items():
            self.__setattr__(k,v)
        self.task_lists = []


app = TaskApp(gtasks.service)

class Task(object):
    def __init__(self, task_list, task):
        self.task_list = task_list
        for k,v in task.items():
            self.__setattr__(k, v)


    def set_parent(self, parent_id):
        app.tasks().move(tasklist=self.task_list.id,
                         task=self.id,
                         parent=parent_id
                        ).execute()

class TaskList(object):
    def __init__(self, ListObject):
        self.service = app
        for k, v in ListObject.items():
            self.__setattr__(k, v)
        
        self.tasks = []
        for t in app.tasks().list(tasklist=self.id, maxResults=100).execute()['items']:
            self.tasks.append(Task(self, t))

    def add_task(self, task_name=None, parent=None):
        body = {
            'title':input('New Task: ') if not task_name else task_name
        }
        parent_exist = input(f"Do you want to assign a parent task? (Y/n) \n> ").lower() == 'y'
        if parent_exist:
            first_level_tasks = self.print_tasks()
            parent = first_level_tasks[int(input("\n[Input interger selection]\n> "))].id
        return self.service.tasks().insert(tasklist=self.id, body=body, parent=parent).execute()


    def print_tasks(self):
        first_level_tasks = [t for t in self.tasks if not hasattr(t, 'parent')]
        for i, t in enumerate(first_level_tasks):
            print(f"[{i}] -- {t.title}")
        return first_level_tasks

    def organize_tasks(self, tasks=None):
        if not tasks:
            tasks = self.tasks
        first_level_tasks = self.print_tasks()
        for t in tasks:
            print(t.title)   
            if hasattr(t, 'parent'):
                question = f"Would you like to change the parent of this task from '{[s.title for s in self.tasks if s.id==t.parent][0]}'?"
            else:
                question = f"Would you like to assign the parent of this task?"
            answer = input(question + " 'n'/(select index of parent)\n>").lower() 
            if answer == 'n':
                continue
            elif answer.isnumeric():
                t.set_parent(first_level_tasks[int(answer)].id)

for list in app.tasklists().list().execute()['items']:
    app.task_lists.append(TaskList(list))


