#
import sys, json, datetime as dt, logging

# Define constants and global variable
TASKFILE='task.json'
LOGFILE='log.txt'

# set up logging 
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# Define functions
# User functions
def print_help():
    print(''' Task CLI - A simple Task Management Tool\n  
    usage: task-cli [command] [parameters]\n
    commands:\n
        help - show this help message\n
        add (description) - add task with the description\n
        update (id) (description - update the description of a task\n
        delete (id) - delete task with given id\n
        mark-in-progress (id) - mark the specified task as in progress\n
        mark-done (id) - mark the task as done\n
        list [status] - list all (without parameter) or by status\n
            - status: todo/in-progress/done\n''')
    
# Add task with description given into task dictionary and write into file.
def addTask(task_dict, description):
    id = len(task_dict.keys()) + 1
    # Define date time format
    fmt = '%Y-%m-%d %H:%M:%S'
    task_dict.update({id: {'desc': description,
                            'status': 'todo',
                            'createdAt': dt.datetime.now().strftime(fmt),
                            'updatedAt': dt.datetime.now().strftime(fmt) }})
    logging.debug(f'New Task with id: {id} has been added to the data')
    return id
def updateTask(id, description):
    return None
    
def deleteTask(id):
    return None

def markTaskInProgress(id):
    return None
def markTaskDone(id):
    return None

def listTask(task_dict: dict , status: str):
    '''
    List all the tasks store in dictionary if status is empty.
    If status is given, list the tasks with the specified status only.
    '''
    # status is empty
    if not status:
        print('All Tasks'.center(40, '*'))

        # Iterate through all the tasks and properties and print out
        for id, properties in task_dict.items():
            print(f'ID: {id}')
            for k, v in properties.items():
                print(f'    {k}: {v}')
            print()
    else:
        print(f'Tasks {status}'.center(40, '*'))
        cnt = 0
        for id, properties in task_dict.items():
            if properties['status'] == status:
                print(f'ID: {id}')
                for k, v in properties.items(): 
                    print(f'    {k}: {v}')
                print()
                cnt += 1
                
        if cnt == 0:
            print(f'No task with status: {status} found.')

    return None

# Internal functions

# Read the all tasks from file and assign to a dictionary
def loadTask(task_file):
    # Open the file
    try:
        with open(task_file, 'r', encoding = 'utf-8') as f:
            task_dict = json.load(f)
            logging.debug(f'loadTask(): task data {task_dict}')

            return task_dict
        
    # if file not found, create a new one
    except FileNotFoundError:
        logging.warning(f'{task_file} not found. Creating new file.')
        with open(task_file, 'w', encoding = 'utf-8') as f:
            f.write('{}')
    except json.JSONDecodeError as err:
        logging.error(f'JSON decode error: {err}')
        print('Error parsing task data, check log for details')

# Write the tasks from dictionary to the file
def writeTask(task_file, task_dict):
    # Open the file to write
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task_dict, f, indent=4)
        logging.debug(f'Task data updated to "{task_file}.')

    return None

# Define the CLI structure
# get the argument of from command line, if does not match all words, 
task_dict = {}

if len(sys.argv) > 1 and sys.argv[0].lower() in ['help', 'add','update','delete','mark-in-progress','mark-done','list']:
    # Command given are valid
    # Read the file
    command = sys.argv[0].lower()
    task_dict = loadTask(TASKFILE)
else:
    command = 'help'

# Define the functions for each command
if command == 'help':
    print_help()
elif command == 'add':
    try:
        description = sys.argv[1]
        id = addTask(description)
        print(f'Task added successfully (ID: {id})')
    except Exception as err:
        logging.error(f'Error adding task: {err}')
        print('Failed to add task. Please check log for details.')

elif command == 'update':
    try:
        id = int(sys.argv[1])
        description = sys.argv[2]
        updateTask(id, description)

    except Exception as err:
        logging.error(f'Error updating task: {err}')
        print('Failed to update task. Please check log for details')

elif command == 'delete':
    try:
        id = int(sys.argv[1])
        deleteTask(id)

    except Exception as err:
        logging.error(f'Error updating task: {err}')
        print('Failed to delete task. Please check log for details')

elif command == 'mark-in-progress':
    try:
        id = int(sys.argv[1])
        markTaskInProgress(id)
    
    except Exception as err:
        logging.error(f'Error marking task as in progress: {err}')
        print('Failed to change status of task. Please check log for details')
elif command == 'mark-done':
    try:
        id = int(sys.argv[1])
        markTaskDone(id)

    except Exception as err:
        logging.error(f'Error mark Done: {err}')
        print(f'Failed to change status of task, Please check log for details')
    
elif command == 'list':
    try:
        if len(sys.argv) ==1:
            listTask('')
        else:
            listTask(sys.argv[1])
    except Exception as err:
        logging.error(f'Error Listing task: {err}')
        print('Something wrong. Check log for details')
else:
    logging.error(f'user input logic error')

