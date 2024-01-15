#Import required packages
import tkinter as tk
from tkinter import ttk
from datetime import datetime

#Class which holds all app related features
class Task_App():
    #Initializes all widgets and frames
    def __init__(self):
        #Backbone for all of the widgets and app
        self.root = tk.Tk()
        self.root.geometry('400x400')
        self.root.title("Task Catalogue")
        self.mainframe = tk.Frame(self.root, background='black')
        self.mainframe.pack(fill='both', expand=True)
        self.task_file_path = 'task_file.txt'

        try:
            with open(self.task_file_path, 'r') as task_file:
                start_lines = []
                for i in range(3):
                    start_lines.append(task_file.readline().rstrip("\n"))
            print(start_lines)
            if start_lines != ["Select", "", "Task"]:
                with open(self.task_file_path, 'w') as file:
                    file.write("Select\n\nTask\n")
                    print("File did not have correct Header: New File created")
        except FileNotFoundError:
            with open(self.task_file_path, 'w'):
                file.write("Select\n\nTask\n")
                print("Had to make a new file")

        #This frame holds the title
        self.titleframe = ttk.Frame(self.mainframe)
        self.titleframe.pack(side="top", pady=10)

        #Title
        self.title = ttk.Label(self.titleframe, text="Task Catalogue", foreground="white", background="black", font=("Times New Roman", 24))
        self.title.pack()

        #Frame holding text entries related to adding a new task
        self.add_task_frame = ttk.Frame(self.mainframe)
        self.add_task_frame.pack(side="top", after=self.titleframe, pady=10)

        #This logic is for the field where the name of the task is entered
        self.add_task_name_field = ttk.Entry(self.add_task_frame)
        self.add_task_name_field.insert(0, "[Enter Task Name]")
        #This logic serves to have a placeholder text function
        taskNameFieldList = [self.add_task_name_field, "[Enter Task Name]"]
        self.add_task_name_field.bind("<FocusIn>", lambda event: self.clear_field(*taskNameFieldList))
        self.add_task_name_field.bind("<FocusOut>", lambda event: self.add_placeholder(*taskNameFieldList))
        self.add_task_name_field.pack(side="bottom")

        #Task Description
        self.add_task_description = tk.Text(self.add_task_frame, width=30, height=3)
        self.add_task_description.insert("1.0", "[Enter Task Description]")
        #Text widget requires different parameters for placeholder functionality
        taskDescriptionFieldList = [self.add_task_description, "[Enter Task Description]", ["1.0", "end-1c"]]
        self.add_task_description.bind("<FocusIn>", lambda event: self.clear_field(*taskDescriptionFieldList))
        self.add_task_description.bind("<FocusOut>", lambda event: self.add_placeholder(*taskDescriptionFieldList))
        self.add_task_description.pack(side="bottom", before=self.add_task_name_field)

        #Task Due Date Frame
        self.due_date_frame = ttk.Frame(self.add_task_frame)
        self.due_date_frame.pack(side='bottom', before=self.add_task_description, pady=5)

        #Task Due Date Entries
        self.due_date_title = ttk.Label(self.due_date_frame, text="Due Date", font=("Times New Roman", 12))
        self.due_date_title.pack(side='top')
        self.due_date_month = ttk.Entry(self.due_date_frame, width=3)
        self.due_date_month.pack(side='left')
        self.divider1 = ttk.Label(self.due_date_frame, text="/", font=("Times New Roman", 12))
        self.divider1.pack(side='left')
        self.due_date_day = ttk.Entry(self.due_date_frame, width=2)
        self.due_date_day.pack(side='left')
        self.divider2 = ttk.Label(self.due_date_frame, text="/", font=("Times New Roman", 12))
        self.divider2.pack(side='left')
        self.due_date_year = ttk.Entry(self.due_date_frame, width=4)
        self.due_date_year.pack(side='left')

        #PlaceHolders
        self.placeholders = [taskNameFieldList[1], taskDescriptionFieldList[1]]
        #Add Task Button
        self.add_task_button = ttk.Button(self.add_task_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side='bottom', before=self.due_date_frame)

        #Organize Tasks Frame
        self.organize_task_frame = ttk.Frame(self.mainframe)
        self.organize_task_frame.pack(side="top", after=self.add_task_frame, pady=10)

        #Select Task Dropdown
        lines = self.access_clean_lines()
        tasks = [lines[i:i+3:2] for i in range(0, len(lines), 3)]
        #tasks = [lines[i:i+3] for i in range(0, len(lines), 3)]
        #descriptions = [tasks[x].pop(1) for x in range(0, len(lines), 3)]
        self.Desplaceholder = tk.StringVar(self.organize_task_frame)
        self.Desplaceholder.set(tasks[0])
        self.task_dropdown_menu = ttk.OptionMenu(self.organize_task_frame, self.Desplaceholder, *tasks, command=lambda value: self.change_description(value, self.access_clean_lines()))
        self.task_dropdown_menu.pack(side='top', pady=10)

        self.selected_task_description = ttk.Label(self.organize_task_frame, text=f"", foreground="black", background="white", font=("Times New Roman", 12))
        self.selected_task_description.pack(side='bottom')

        self.selected_task_index = 0
        self.mark_complete_button = ttk.Button(self.organize_task_frame, text="Mark Task Complete", command=self.mark_task_complete)
        self.mark_complete_button.pack(side='bottom', before=self.selected_task_description)

        self.root.mainloop()
        return

    #Accesses the text file in readmode and collects the file as a list of lines
    def access_clean_lines(self):
        try:
            with open(self.task_file_path, 'r') as task_file:
                task_lines = task_file.readlines()
                cleaned_lines = []
                for line in task_lines:
                    cleaned_lines.append(line.rstrip("\n"))
            return cleaned_lines
        except FileNotFoundError:
            print(f"The file '{self.task_file_path}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}\nCould not properly access file lines")

    #Accesses the text file which holds the task data and adds an additional task
    def add_task(self):
        newTaskName = self.add_task_name_field.get()

        if newTaskName in self.access_clean_lines():
             print("Error found: Already a task with the same name present")
             return

        newTaskDescription = self.add_task_description.get('1.0', 'end-1c')
        newTaskDueDate = self.due_date_month.get() + "/" + self.due_date_day.get() + "/" + self.due_date_year.get()
        newTaskEntry = newTaskName+"\n"+newTaskDescription+'\n'+newTaskDueDate+"\n"

        #This logic ensures that the information is present and accurate before it adds the task to the list
        for item in [newTaskName, newTaskDescription]:
            if item in self.placeholders:
                print("Failed to add entry!\nPlease fill out the following:" + item)
                return
        if self.check_if_invalid_date(*newTaskDueDate.split("/")):
            print("Failed to add entry!\nInvalid or Past Date\nPlease Enter an Appropriate Date")
            return


        try:
            with open(self.task_file_path, 'a') as task_file:
                task_file.write(newTaskEntry)
            self.sort_tasks()
            print("Added Task: \n" + newTaskEntry)
            #Add the task to the dropdown
            lines = self.access_clean_lines()
            self.update_dropdown([lines[i:i+3:2] for i in range(0, len(lines), 3)])
        except FileNotFoundError:
            print(f"The file '{self.task_file_path}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}\nCould not properly add task")

        

    #Clears a text field of placeholder text when it is clicked on
    def clear_field(self, entry, placeholder, index=[]):
        if entry.get(*index) == placeholder:
            try:
                entry.delete(0, 'end')
            except:
                entry.delete("1.0", 'end')

    #ReEnters placeholder text when the field is clicked off of
    def add_placeholder(self, entry, placeholder, index=[]):
        if entry.get(*index) == '':
            try:
                entry.insert(0, placeholder)
            except:
                entry.insert("1.0", placeholder)

    #Self explanatory
    def check_if_invalid_date(self, month=0, day=0, year=0):
        try:
            date_data = list(map(int, [year, month, day]))
            due_date = datetime(*date_data)
            if due_date.date() < datetime.now().date():
                return True
            return False
        except ValueError:
            return True

    #This function takes in all of the information in the file and sorts according to the date
    def sort_tasks(self):
        try:
            #Opens the file and reads it into a list of each line and removes newline character at the end of each line
            lines = self.access_clean_lines()
            #Seperates the list into a list of sublist grouped in threes
            separated_tasks = [lines[i:i+3] for i in range(0, len(lines), 3)]
            #Sorts the list by the 3rd element using datetime format
            separated_tasks = separated_tasks[1:len(separated_tasks)+1]
            sorted_date_tasks = sorted(separated_tasks, key=lambda x: datetime.strptime(x[2], '%m/%d/%Y'))
            #Rejoins the sublists of lines and then rejoins the list into one composite string
            sorted_tasks = "\n".join(["\n".join(x) for x in sorted_date_tasks]) +"\n"
            with open (self.task_file_path, 'r') as task_file:
                lines = task_file.readlines()
                lastline = lines.pop()
                if "\n" not in lastline:                         #This needs to be fixed
                    with open(self.task_file_path, 'a') as task_file:
                        task_file.write("\n")
                        print("added")
            with open(self.task_file_path, 'w') as task_file:
                task_file.write(f"Select\n\nTask\n{sorted_tasks}")
        except FileNotFoundError:
            print(f"The file '{self.task_file_path}' does not exist.\nCould not reach file")
        except Exception as e:
            print(f"An error occurred: {e}\nCould not properly sort tasks")

    def change_description(self, current_value, tasklines):
        self.selected_task_index = tasklines.index(current_value[0])
        description_index = self.selected_task_index + 1
        self.selected_task_description.config(text=f"{tasklines[description_index]}")

    def mark_task_complete(self):
         try:
            lines = self.access_clean_lines()
            del lines[self.selected_task_index:self.selected_task_index+3]
            altered_tasks = "\n".join(lines[3:])
            with open(self.task_file_path, 'w') as task_file:
                task_file.write(f"Select\n\nTask\n{altered_tasks}")
            menu = self.task_dropdown_menu['menu']
            task_menu_index= int(self.selected_task_index/3)
            #menu.entryconfig(task_menu_index-1, label="Completed Task")
            menu.delete(task_menu_index-1)
            print("Task has been successfully marked completed and removed")
         except FileNotFoundError:
            print(f"The file '{self.task_file_path}' does not exist.\nCould not reach file")
         except Exception as e:
            print(f"An error occurred: {e}\nCould not properly mark task complete")

    def update_dropdown(self, new_options):
         self.Desplaceholder.set(new_options[0])
         menu = self.task_dropdown_menu['menu']
         self.task_dropdown_menu['menu'].delete(0,'end')
         for option in new_options:
            menu.add_command(label=option, command=lambda v=option: self.change_description(v, self.access_clean_lines()))
#Starts App
if __name__ == '__main__':
    Task_App()
    #Create the file with the select task lines