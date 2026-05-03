'''
Task CLI - A simple Task Management Tool
'''
import sys, json, datetime as dt, logging

# Define functions
# User functions
def print_help():
    print(''' Task CLI - A simple Task Management Tool\n  
    usage: task-cli [command] [parameters]\n
    commands:\n
        help - show this help message\n
        add (description) - add task with the description\n
        update (id) (description) - update the description of a task\n
        delete (id) - delete task with given id\n
        mark-in-progress (id) - mark the specified task as in progress\n
        mark-done (id) - mark the task as done\n
        list [status] - list all (without parameter) or by status\n
            - status: todo/in-progress/done\n''')
    
def addTask(task_dict: dict, description: str):
    '''
    Add task with the description given. 
    structure of a task
    {id:
	    {description:"",
        status: '',
        createdAt: datetime,
        updatedAt: datetime}
    }
    '''
    id = str(len(task_dict.keys()) + 1)
    # Define date time format
    fmt = '%Y-%m-%d %H:%M:%S'
    task_dict.update({id: {'desc': description,
                            'status': 'todo',
                            'createdAt': dt.datetime.now().strftime(fmt),
                            'updatedAt': dt.datetime.now().strftime(fmt) }})
    logging.info(f'New Task with id: {id} has been added to the data')

    return id

def updateTask(task_dict: dict, id: str , description: str):
    '''
    Update the description of the task with the given id.
    If the task with the given id does not exist, raise Exception to be handled outside of function.
    '''
    if task_dict.get(id, 0):
        task_dict[id]['desc'] = description
        # Update the updatedAt field
        fmt = '%Y-%m-%d %H:%M:%S'
        task_dict[id]['updatedAt'] = dt.datetime.now().strftime(fmt)
        logging.info(f'Task with ID: {id} has been updated with new description: {description}')
    else:
        raise Exception(f'Task with ID: {id} is not found. Check again for the existing id')
    
    return None
    
def deleteTask(task_dict: dict, id: str):
    '''
    Delete the task with the given id.

    if the id doesn't exist, raise Exception to be handled outside of function.
    '''
    if task_dict.get(id, 0):
        del task_dict[id]
        logging.info(f'Task with ID: {id} has been deleted')
    else:
        raise Exception(f'Task with ID: {id} is not found. Check again for the existing id')

    return None

def markTaskInProgress(task_dict: dict , id: str):
    '''
    Mark the task with the given id as in-progess
    
    If the task with the given id does not exist, print error message and return.
    
    Change the value of the 'status' of a task 
    '''
    if task_dict.get(id, 0):
        task_dict[id]['status'] = 'in-progress'
        # UPdate the updatedAt field
        fmt = '%Y-%m-%d %H:%M:%S'
        task_dict[id]['updatedAt'] = dt.datetime.now().strftime(fmt)
        logging.info(f'Task with ID: {id} mark as in progress.')
    else:
        raise Exception(f'Task with ID: {id} is not found. Check again for the existing id')

    return None

def markTaskDone(task_dict: dict , id: str):
    '''
    Mark the task with the given id as done
    
    If the task with given id does not exist, print message and return.

    Change the value of the'status of a task    
    '''
    if task_dict.get(id, 0):
        task_dict[id]['status'] = 'done'
        # Update the updatedAt field
        fmt = '%Y-%m-%d %H:%M:%S'
        task_dict[id]['updatedAt'] = dt.datetime.now().strftime(fmt)
        logging.info(f'Task with ID: {id} mark as done.')
    else:
        raise Exception(f'Task with ID: {id} is not found. Check again for the existing id')

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
def loadTask(task_dict: dict, task_file: str):
    '''
    Load the task data from the file and assign to the task dictionary.
    '''
    # Open the file
    try:
        with open(task_file, 'r', encoding = 'utf-8') as f:
            # the reassignment here causes the references to change, therefore necessary to return dictionary
            task_dict = json.load(f)        
            logging.debug(f'loadTask(): task data {task_dict}')

            return task_dict
        
    # if file not found, create a new one
    except FileNotFoundError:
        logging.warning(f'{task_file} not found. Creating new file.')
        with open(task_file, 'w', encoding = 'utf-8') as f:
            f.write('{}')
    # if content is not in json format
    except json.JSONDecodeError as err:
        err = f'JSON decode error: {err}'
        logging.error(err)
        print(err)

def writeTask(task_dict: dict, task_file: str):
    '''
    Write the tasks from dictionary to the task file
    '''
    # Open the file to write
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task_dict, f, indent=4)
        logging.debug(f'Task data updated to "{task_file}.')

    return None

# Define constants and global variable
TASKFILE='task.json'
LOGFILE='log.txt'
task_dict = {}

# set up logging 
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

# Define the CLI structure
# get the argument of from command line and check for the length
if len(sys.argv) >= 2  and sys.argv[1].lower() in ['help', 'add','update','delete','mark-in-progress','mark-done','list']:
    # Command given are valid
    command = sys.argv[1].lower()
    task_dict = loadTask(task_dict, TASKFILE)
else:
    command = 'help'

# Define the function calls for each command user enter
if command == 'help':
    print_help()
elif command == 'add' and len(sys.argv) == 3:
    try:
        description = sys.argv[2]
        id = addTask(task_dict, description)
        print(f'Task added successfully (ID: {id})')
        writeTask(task_dict, TASKFILE)
        
    except Exception as err:
        err = f'Error adding task: {err}'
        logging.error(err)
        print('err')

elif command == 'update' and len(sys.argv) == 4: 
    try:
        id = sys.argv[2]
        description = sys.argv[3]
        updateTask(task_dict, id, description)
        writeTask(task_dict, TASKFILE)

    except Exception as err:
        err = f'Error updating task: {err}'
        logging.error(err)
        print(err)

elif command == 'delete' and len(sys.argv) == 3:
    try:
        id = sys.argv[2]
        deleteTask(task_dict, id)
        writeTask(task_dict, TASKFILE)

    except Exception as err:
        err = f'Error deleting task: {err}'
        logging.error(err)
        print(err)

elif command == 'mark-in-progress' and len(sys.argv) == 3:
    try:
        id = sys.argv[2]
        markTaskInProgress(task_dict, id)
        writeTask(task_dict, TASKFILE)
    
    except Exception as err:
        err = f'Error marking task as in progress: {err}'
        logging.error(err)
        print(err)

elif command == 'mark-done' and len(sys.argv) == 3:
    try:
        id = sys.argv[2]
        markTaskDone(task_dict, id)
        writeTask(task_dict, TASKFILE)

    except Exception as err:
        err = f'Error mark Done: {err}'
        logging.error(err)
        print(err)
    
elif command == 'list' and len(sys.argv) <= 3:
    try:
        if len(sys.argv) == 2:
            listTask(task_dict, '')
        else:
            if sys.argv[2] not in ['todo', 'in-progress', 'done']:
                raise Exception('Status should be one of "todo", "in-progress", and "done".')
            else:
                listTask(task_dict, sys.argv[2])
    except Exception as err:
        err = f'Error Listing task: {err}'
        logging.error(err)
        print(err)
else:
    print(f'Command "{command}" parameter incorrect')
    print_help()