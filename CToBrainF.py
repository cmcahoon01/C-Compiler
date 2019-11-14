STRING_LENGTH = 5


class Memory:
    output = ""
    used_memory = 0
    variables = []
    variable_locations = {}


class Head:
    pointer = 0

    def __init__(self, memory):
        self.memory = memory

    def point_at(self, location):
        if location < 0:
            raise IndexError(str(location) + " is out of bounds")
        if self.pointer > location:
            for _ in range(self.pointer - location):
                self.left()
        else:
            for _ in range(location - self.pointer):
                self.right()
        self.memory.pointer = location

    def follow_pointer(self):  # DISLOCATES POINTER
        self.memory.output += ">>>>>>[-<<<<+<<+>>>>>>]<<<<[->>>>+<<<<]<<"  # copy destination to cursor
        self.point_at(0)
        self.memory.output += "["  # until arrived
        self.right()
        self.memory.output += "-]"  # arrived

    def reset(self):
        self.memory.output += ">>>>[-<<+<<+>>>>]<<[->>+<<]<<"  # copy location to cursor
        self.memory.output += "["  # until arrived
        self.left()
        self.memory.output += "-]"  # arrived
        self.pointer = 0  # corrects pointer

    def left(self):
        self.memory.output += "<[->>+>+<<<]>>>[-<<<+>>>]<"  # copy left size to storage
        self.memory.output += "["  # until storage is empty
        self.memory.output += "<<[->>>+<<<]>[-<+>]>[-<+>]<"  # slide left 1
        self.memory.output += "-]<"
        self.pointer -= 1

    def right(self):
        self.memory.output += ">>>>>[-<<<+<+>>>>]<<<[->>>+<<<]<"  # copy right size to storage
        self.memory.output += "["  # until storage is empty
        self.memory.output += "[->+<]<[->+<]>>>[-<<<+>>>]<"  # slide right 1
        self.memory.output += "-]<"
        self.pointer += 1

    def set_storage(self, value):
        self.memory.output += ">"
        self.set_value(value)
        self.memory.output += "<"

    def erase_left(self):
        self.memory.output += "<[->>+<<]>>"  # move left size to storage
        self.memory.output += "["  # until storage is empty
        self.memory.output += "<<[-]>[-<+>]>[-<+>]<"  # push left 1
        self.memory.output += "-]<"
        self.pointer -= 1
        self.memory.used_memory -= 1

    def erase_right(self):
        self.memory.output += ">>>>>[-<<<<+>>>>]<<<<"  # move right size to storage
        self.memory.output += "["  # until storage is empty
        self.memory.output += ">>[-]<<[->+<]<[->+<]>>"  # push left 1
        self.memory.output += "-]<"
        self.memory.used_memory -= 1

    def input(self):
        self.memory.output += ">>>>>,"  # point at where string will start, overwriting size with the input
        self.memory.output += "----------[++++++++++>[->+<]>+<,----------]>"  # read until newline character(10)
        self.memory.output += "[->>+<<]>>[-<+<+<+>>>]<---"  # setup train to carry size to front
        self.memory.output += "[<<[->>>+<<<]>[-<+>]>[-<+>]<-]<"  # move size to front
        self.memory.output += "[->>+<<]<[->>+<<]<[->>+<<]"  # move blanks to front
        # slide head and blanks to end
        self.memory.output += ">>>>[-<<<<<+<+>>>>>>]<<<<<[->>>>>+<<<<<]<"  # copy right size to storage
        self.memory.output += "["  # until storage is empty
        self.memory.output += "[->+<]>>>>[-<<<<<+>>>>>]<<<"  # slide right 1
        self.memory.output += "-]<"
        self.pointer += 1

    def print(self):
        self.memory.output += ">>>[-<<+>>]>[-<<+>>]"  # create gap in obj
        self.memory.output += ">[-<+<+>>]<"  # copy size to train
        self.memory.output += "----[>>.<<[->+<]>>[-<<+>>]<-]>"  # move across string while printing
        self.memory.output += "++++++++++.----------"  # print a newline
        self.memory.output += ">[-<+<+>>]<[->+<]<-"  # prepare train to return
        self.memory.output += "[<[->>+<<]>[-<+>]<-]<"

    def set_value(self, value):  # must be pointed at where value will be set, with a blank to its right
        self.memory.output += "+" * (value % 10)  # Set storage to ones digit of value
        if value >= 10:
            self.memory.output += ">"
            self.memory.output += "+" * int(value / 10)  # Set blank to the rest of the number
            self.memory.output += "[-<++++++++++>]"  # Add 10 * blank to storage
            self.memory.output += "<"  # point at storage


class JavaToBrainFConverter:
    memory = Memory()
    head = Head(memory)

    def get_new_work_storage(self, obj_type=0):
        self.head.point_at(self.memory.used_memory)
        if 0 <= obj_type < 10:
            self.memory.output += ">>>" + "+" * obj_type + ">" + "+" * self.memory.used_memory + ">+++++>>+++++<<<<<<<"
        else:
            self.memory.output += ">>>" + "+" * obj_type + ">" + "+" * self.memory.used_memory + ">++++>++++<<<<<<"
        self.memory.used_memory += 1
        return self.memory.used_memory - 1

    def copy_to_new_work_storage(self, location):
        new_location = self.get_new_work_storage()
        self.copy(location, new_location)
        return new_location

    def set_to_new_work_storage(self, number):
        new_location = self.get_new_work_storage()
        self.set_int(new_location, number)
        return new_location

    def clean_last_items(self, size):
        self.head.point_at(self.memory.used_memory)
        for _ in range(size):
            self.head.erase_left()

    def evaluate_commands(self, commands, save_to):
        if len(commands) == 0:
            return
        elif len(commands) == 1:
            try:
                self.set_int(save_to, int(commands[0]))
                return
            except ValueError:
                if commands[0] in self.memory.variables:
                    self.copy(self.memory.variable_locations[commands[0]], save_to)
                    return
                elif len(commands[0]) > 3 and commands[0][:3] == "mem":
                    self.copy(int(commands[0][3:]), save_to)
                    return
                elif commands[0][0] == '"':
                    self.set_string(save_to, commands[0][1:-1])
                elif commands[0] == "scanf":
                    self.input(save_to)
                    return
        elif commands[0] == "int":
            self.make_int(commands[1])
            if len(commands) > 2 and commands[2] == "=":
                self.assign_variable(commands[1], commands[3:])
            return
        elif commands[1] == "=":
            self.assign_variable(commands[0], commands[2:])
            return
        elif commands[1] == "+":
            locations = [self.get_new_work_storage(), self.get_new_work_storage()]
            self.evaluate_commands([commands[0]], locations[0])
            self.evaluate_commands(commands[2:], locations[1])
            self.move_int(locations[0], save_to)
            self.move_int(locations[1], save_to, clear_old=False)
            self.clean_last_items(2)
            return
        elif commands[0] == "(":
            close = self.find_closing_parenthesis(commands)
            location = self.get_new_work_storage()
            self.evaluate_commands(commands[1:close], location)
            self.evaluate_commands(["mem" + str(location)] + commands[close + 1:], save_to)
            self.clean_last_items(1)
            return
        elif commands[0] == "printf":
            location = self.get_new_work_storage()
            self.evaluate_commands(commands[1:], location)
            self.out_print(location)
            self.clean_last_items(1)
        elif commands[0] == "to_string":
            self.evaluate_commands(commands[1:], save_to)

        else:
            raise RuntimeError("unknown command " + commands)

    def make_int(self, name):
        self.memory.variables.append(name)
        location = self.get_new_work_storage(obj_type=2)
        self.memory.variable_locations[name] = location

    def assign_variable(self, name, value_list):
        location = self.get_new_work_storage()
        self.evaluate_commands(value_list, location)
        self.move_int(location, self.memory.variable_locations[name])
        self.clean_last_items(1)

    def set_int(self, location, number):
        self.head.point_at(location)
        self.memory.output += ">>>[-]++>>>"  # Set type
        self.memory.output += "+" * (number % 10)  # Set storage to ones digit of value
        self.memory.output += "<<<<"  # use head's blank as a placeholder
        if number >= 10:
            self.memory.output += "+" * int(number / 10)  # Set blank to the rest of the number
            self.memory.output += "[->>>>++++++++++<<<<]"  # Add 10 * blank to storage
        self.memory.output += "<<"  # point at cursor

    def set_string(self, location, string):
        str_location = self.get_new_work_storage(10)
        self.head.point_at(location)
        self.memory.output += ">>>[-]+>>>[-]" + "+" * str_location + "<<<<<<"  # create pointer to new string
        self.head.point_at(str_location)
        self.memory.output += ">>>>>>[-]<"
        self.head.set_value(len(string))
        self.memory.output += ">"
        for character in string:
            self.head.set_value(ord(character))
            self.memory.output += ">"
        self.head.set_value(len(string))
        self.memory.output += "++++"
        self.memory.output += "<" * len(string) + "<<<<<<"

    def move_int(self, a, b, clear_old=True):
        if clear_old:
            self.head.point_at(b)
            self.memory.output += ">>>>[-]++>>[-]<<<<<<"
        self.head.point_at(a)
        self.memory.output += ">>>>>>[-<<<<<<"
        self.head.point_at(b)
        self.memory.output += ">>>>>>+<<<<<<"
        self.head.point_at(a)
        self.memory.output += ">>>>>>]<<<<<<"

    def copy(self, a, b, clear_old=True):
        if clear_old:
            self.head.point_at(b)
            self.memory.output += ">>>>[-]++>>[-]<<<<<<"
        copy_location = self.get_new_work_storage()
        self.move_int(a, copy_location)
        self.head.point_at(copy_location)
        self.memory.output += ">>>>>>[-<<<<<<"
        self.head.point_at(b)
        self.memory.output += ">>>>>>+<<<<<<"
        self.head.point_at(a)
        self.memory.output += ">>>>>>+<<<<<<"
        self.head.point_at(copy_location)
        self.memory.output += ">>>>>>]<<<<<<"
        self.clean_last_items(1)

    def input(self, location):
        str_location = self.get_new_work_storage(10)
        self.head.point_at(location)
        self.memory.output += ">>>[-]+>>>[-]" + "+" * str_location + "<<<<<<"
        self.head.point_at(str_location)
        self.head.input()

    def out_print(self, location):
        self.head.point_at(location)
        self.head.follow_pointer()
        self.head.print()
        self.head.reset()

    def run(self, code):
        location = self.get_new_work_storage()
        for line_number in range(len(code)):
            line = code[line_number]
            if len(line) == 0:
                continue
            if line[-1] == ";":
                line = line[:-1]
            parts = line.split(" ")
            self.evaluate_commands(parts, location)
            self.memory.output += "\n"
        self.head.point_at(0)

    @staticmethod
    def find_closing_parenthesis(commands, index=0):
        depth = 0
        for i in range(index + 1, len(commands)):
            char = commands[i]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == -1:
                    return i
        raise RuntimeError('")" not found')


if __name__ == "__main__":
    with open('C.txt', 'r') as file:
        raw = file.read().split("\n")

    converter = JavaToBrainFConverter()
    converter.run(raw)
    print(converter.memory.output)
