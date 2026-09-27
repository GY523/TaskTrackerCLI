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
        update (t_id) (description) - update the description of a task\n
        delete (t_id) - delete task with given t_id\n
        mark-in-progress (t_id) - mark the specified task as in progress\n
        mark-done (t_id) - mark the task as done\n
        list [status] - list all (without parameter) or by status\n
            - status: todo/in-progress/done\n''')
    
def addTask(task_dict: dict, description: str):
    '''
    Add task with the description given. 
    structure of a task
    {t_id:
	    {description:"",
        status: '',
        createdAt: datetime,
        updatedAt: datetime}
    }
    '''
    id_list = list(map(int, task_dict.keys())) # [id1, id2]


    new_id = max(id_list, default=0) + 1
    # Define date time format
    fmt = '%Y-%m-%d %H:%M:%S'
    task_dict.update({new_id: {'desc': description,
                            'status': 'todo',
                            'createdAt': dt.datetime.now().strftime(fmt),
                            'updatedAt': dt.datetime.now().strftime(fmt) }})
    logging.info(f'New Task with id: {id} has been added to the data')
    
    return new_id

def updateTask(task_dict: dict, t_id: str , description: str):
    '''
    Update the description of the task with the given t_id.
    If the task with the given t_id does not exist, raise Exception to be handled outst_ide of function.
    '''
    if task_dict.get(t_id, 0):
        task_dict[t_id]['desc'] = description
        # Update the updatedAt field
        fmt = '%Y-%m-%d %H:%M:%S'
        task_dict[t_id]['updatedAt'] = dt.datetime.now().strftime(fmt)
        logging.info(f'Task with t_id: {t_id} has been updated with new description: {description}')
    else:
        raise Exception(f'Task with t_id: {t_id} is not found. Check again for the existing t_id')
    
    return None
    
def deleteTask(task_dict: dict, t_id: str):
    '''
    Delete the task with the given t_id.

    if the t_id doesn't exist, raise Exception to be handled outst_ide of function.
    '''
    if task_dict.get(t_id, 0):
        del task_dict[t_id]
        logging.info(f'Task with t_id: {t_id} has been deleted')
    else:
        raise Exception(f'Task with t_id: {t_id} is not found. Check again for the existing t_id')

    return None

def markTaskInProgress(task_dict: dict , t_id: str):
    '''
    Mark the task with the given t_id as in-progess
    
    If the task with the given t_id does not exist, print error message and return.
    
    Change the value of the 'status' of a task 
    '''
    if task_dict.get(t_id, 0):
        task_dict[t_id]['status'] = 'in-progress'
        # UPdate the updatedAt field
        fmt = '%Y-%m-%d %H:%M:%S'
        task_dict[t_id]['updatedAt'] = dt.datetime.now().strftime(fmt)
        logging.info(f'Task with t_id: {t_id} mark as in progress.')
    else:
        raise Exception(f'Task with t_id: {t_id} is not found. Check again for the existing t_id')

    return None

def markTaskDone(task_dict: dict , t_id: str):
    '''
    Mark the task with the given t_id as done
    
    If the task with given t_id does not exist, print message and return.

    Change the value of the'status of a task    
    '''
    if task_dict.get(t_id, 0):
        task_dict[t_id]['status'] = 'done'
        # Update the updatedAt field
        fmt = '%Y-%m-%d %H:%M:%S'
        task_dict[t_id]['updatedAt'] = dt.datetime.now().strftime(fmt)
        logging.info(f'Task with t_id: {t_id} mark as done.')
    else:
        raise Exception(f'Task with t_id: {t_id} is not found. Check again for the existing t_id')

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
        for t_id, properties in task_dict.items():
            print(f't_id: {t_id}')
            for k, v in properties.items():
                print(f'    {k}: {v}')
            print()
    else:
        print(f'Tasks {status}'.center(40, '*'))
        cnt = 0
        for t_id, properties in task_dict.items():
            if properties['status'] == status:
                print(f't_id: {t_id}')
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
if len(sys.argv) > 1:
    command = sys.argv[1].lower()
    task_dict = loadTask(task_dict, TASKFILE)
else:
    print_help()
    sys.exit(1)

# Define the function calls for each command user enter
match command:
    case "help":
        print_help()
    case 'add' if len(sys.argv) == 3:
        try:
            description = sys.argv[2]
            t_id = addTask(task_dict, description)
            print(f'Task added successfully (ID: {t_id})')
            writeTask(task_dict, TASKFILE)
            
        except Exception as err:
            err = f'Error adding task: {err}'
            logging.error(err)
            print(err)

    case 'update' if len(sys.argv) == 4: 
        try:
            t_id = sys.argv[2]
            description = sys.argv[3]
            updateTask(task_dict, t_id, description)
            writeTask(task_dict, TASKFILE)

        except Exception as err:
            err = f'Error updating task: {err}'
            logging.error(err)
            print(err)

    case 'delete' if len(sys.argv) == 3:
        try:
            t_id = sys.argv[2]
            deleteTask(task_dict, t_id)
            writeTask(task_dict, TASKFILE)

        except Exception as err:
            err = f'Error deleting task: {err}'
            logging.error(err)
            print(err)

    case 'mark-in-progress' if len(sys.argv) == 3:
        try:
            t_id = sys.argv[2]
            markTaskInProgress(task_dict, t_id)
            writeTask(task_dict, TASKFILE)
        
        except Exception as err:
            err = f'Error marking task as in progress: {err}'
            logging.error(err)
            print(err)

    case 'mark-done' if len(sys.argv) == 3:
        try:
            t_id = sys.argv[2]
            markTaskDone(task_dict, t_id)
            writeTask(task_dict, TASKFILE)

        except Exception as err:
            err = f'Error mark Done: {err}'
            logging.error(err)
            print(err)
    
    case 'list' if len(sys.argv) <= 3:
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
    case _:
        print_help()