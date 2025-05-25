import click # type: ignore
import storage
from datetime import datetime

@click.group()
def manager():
    pass


@click.command()
@click.option('--id', '-i', help='ID of the task', type=int, default=None)
@click.option('--sort', '-s', help='Sort tasks by due date', type=bool, default=False)
def view(id, sort):
    if id is not None:
        click.secho(f"\n> Task #{id}", fg='cyan', bold=True, underline=True)
        
        tasks = storage.load_tasks()
        
        task_id_str = str(id)
        
        if task_id_str not in tasks['tasks']:
            click.echo()
            click.secho(f" Task #{id} not found", fg='red', bold=True)
            click.secho(f" Use 'view' without --id to see all tasks", fg='bright_black')
            click.echo()
            return
        
        task_data = tasks['tasks'][task_id_str]
        click.echo()
        
        click.secho("┌─────────────────────────────────────────────────┐", fg='blue')
        
        if task_data['completed']:
            status_line = f" #{id:<3} COMPLETED"
            task_color = 'bright_black'
            border_color = 'green'
        else:
            status_line = f" #{id:<3} IN PROGRESS"
            task_color = 'white'
            border_color = 'yellow'
        
        click.secho(status_line.ljust(49) , fg=border_color, bold=True)
        
        task_line = f" Name: {task_data['task']}"
        click.secho(task_line.ljust(49) , fg=task_color, bold=True)
        
        if task_data['description']:
            desc_line = f" Description: {task_data['description']}"
            click.secho(desc_line.ljust(49) , fg='bright_black')
        
        due_date_line = f" Due Date: {task_data['due_date']}"
        click.secho(due_date_line.ljust(49), fg='bright_blue')
        
        days_left = storage.calculate_days_left(task_data['due_date'])
        if days_left < 0:
            days_remaining_line = f" Days Remaining: {abs(days_left)} days overdue"
            days_color = 'red'
        elif days_left == 0:
            days_remaining_line = f" Days Remaining: Due today!"
            days_color = 'yellow'
        else:
            days_remaining_line = f" Days Remaining: {days_left} days"
            days_color = 'green'

        if task_data['completed']:
            days_remaining_line = f" wohoo you've completed this task!"
            days_color = 'bright_black'
        
        click.secho(days_remaining_line.ljust(49), fg=days_color, bold=True)
        
        click.secho("└─────────────────────────────────────────────────┘", fg='blue')
        click.echo()
       
    else:
        click.secho("\n > Your Tasks", fg='cyan', bold=True)
        
        tasks = storage.load_tasks()
        
        if not tasks['tasks']:
            click.echo("\n Empty task list")
            click.secho("  + Add your first task with: ", fg='bright_black', nl=False)
            click.secho("add <task_name>", fg='green', bold=True)
            click.echo()
            return
        
        click.echo()

        if sort:
            tasks['tasks'] = dict(sorted(tasks['tasks'].items(), key=lambda x: x[1]['days_left'] and x[1]['completed']))
    
        for i, (task_id, task_data) in enumerate(tasks['tasks'].items(), 1):
            click.secho("┌─────────────────────────────────────────────────┐", fg='blue')
            
            if task_data['completed']:
                status_line = f" #{task_id:<3} COMPLETED"
                task_color = 'bright_black'
                border_color = 'green'
            else:
                status_line = f" #{task_id:<3} IN PROGRESS"
                task_color = 'white'
                border_color = 'yellow'
            
            click.secho(status_line.ljust(49) , fg=border_color, bold=True)
            
            task_line = f" Name: {task_data['task']}"
            click.secho(task_line.ljust(49) , fg=task_color, bold=True)
            
            if task_data['description']:
                desc_line = f" Description: {task_data['description']}"
                click.secho(desc_line.ljust(49) , fg='bright_black')
            
            due_date_line = f" Due Date: {task_data['due_date']}"
            click.secho(due_date_line.ljust(49), fg='bright_blue')
            
            days_left = storage.calculate_days_left(task_data['due_date'])
            if days_left < 0:
                days_remaining_line = f" Days Remaining: {abs(days_left)} days overdue"
                days_color = 'red'
            elif days_left == 0:
                days_remaining_line = f" Days Remaining: Due today!"
                days_color = 'yellow'
            else:
                days_remaining_line = f" Days Remaining: {days_left} days"
                days_color = 'green'
            
            if task_data['completed']:
                days_remaining_line = f" wohoo you've completed this task!"
                days_color = 'bright_black'
            
            click.secho(days_remaining_line.ljust(49), fg=days_color, bold=True)
            
            click.secho("└─────────────────────────────────────────────────┘", fg='blue')
            
            if i < len(tasks['tasks']):
                click.echo()

@click.command()
@click.argument('task')
@click.option('--description', '-d', help='Description of the task', default='')
@click.option('--due-date', '-due', help='Due date of the task, format: DD-MM-YYYY', default=f"{datetime.now().strftime('%d-%m-%Y')}")

def add(task, description, due_date):
    storage.add_task(task, description, due_date)
    click.echo(f"Task {task} added successfully")


@click.command()
@click.option('--id', '-i', help='ID of the task', type=int, default=None)
def complete(id):
    storage.complete_task(id)
    click.echo(f"Task {id} completed successfully")


@click.command()
@click.option('--id', '-i', help='ID of the task', type=int, default=None)
def delete(id):
    storage.delete_task(id)
    click.echo(f"Task {id} deleted successfully")

manager.add_command(view)
manager.add_command(add)
manager.add_command(complete)
manager.add_command(delete)

