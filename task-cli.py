#
import sys, json, datetime, logging

# Define constants and global variable
TASKFILE='task.json'
LOGFILE='log.txt'

# set up logging 
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# Define functions
# User functions
def print_help():
    print(''' Task CLI - A simple Task Management Tool\n  
          \tusage: task-cli [command] [parameters]\n
          \tcommands:\n
            \t\thelp - show this help message\n
            \t\tadd (description) - add task with the description\n
            \t\tupdate (id) (description - update the description of a task\n
            \t\tdelete (id) - delete task with given id\n
            \t\tmark-in-progress (id) - mark the specified task as in progress\n
            \t\tmark-done (id) - mark the task as done\n
            \t\tlist [status] - list all (without parameter) or by status\n
              \t\t\t- status: todo/in-progress/done\n''')
    
def addTask(description):
    return id
def updateTask(id, description):
    return None
    
def deleteTask(id):
    return None

def markTaskInProgress(id):
    return None
def markTaskDone(id):
    return None
def listTask(status):
    return None

# Internal functions
def loadTask(task_file, task_dict):
    return None
def writeTask(task_file, task_dict):
    return None

# Define the CLI structure
# get the argument of from command line, if does not match all words, 

if len(sys.argv) > 1 and sys.argv[0].lower() in ['help', 'add','update','delete','mark-in-progress','mark-done','list']:
    command = sys.argv[0].lower()
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

