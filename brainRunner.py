CHARACTERS = ["+", "-", "<", ">", "[", "]", ".", ",", "*"]
DISPLAY = False


def display(memory, command=""):
    if DISPLAY:
        for val in memory.tape:
            print("|", val, "|", end="")
        print()
        print("     " * memory.pointer + "  ^")
        print("     " * memory.pointer + "  |")
        print("     " * memory.pointer + "  " + command)
        print()
        input()


class Memory:
    def __init__(self, tape=[0], pointer=0):
        self.tape = tape
        self.pointer = pointer
        self.input_buffer = []


class Compiler:
    def __init__(self, code, memory=Memory()):
        self.memory = memory
        self.code = code

    def run(self):
        while len(self.code) > 0:
            command = self.code[0]
            display(self.memory, command)
            self.code = self.code[1:]
            if command == CHARACTERS[0]:
                self.plus()
            elif command == CHARACTERS[1]:
                self.minus()
            elif command == CHARACTERS[2]:
                self.left()
            elif command == CHARACTERS[3]:
                self.right()
            elif command == CHARACTERS[4]:
                self.open()
            elif command == CHARACTERS[5]:
                self.close()
            elif command == CHARACTERS[6]:
                self.write()
            elif command == CHARACTERS[7]:
                self.read()
            elif command == CHARACTERS[8]:
                global DISPLAY
                DISPLAY = not DISPLAY
            else:
                raise NotImplementedError(command)
        return self.memory.tape, self.memory.pointer

    def plus(self):
        self.memory.tape[self.memory.pointer] += 1

    def minus(self):
        self.memory.tape[self.memory.pointer] -= 1

    def left(self):
        if self.memory.pointer >= 0:
            self.memory.pointer -= 1
        else:
            raise IndexError("pointer can not go below 0")

    def right(self):
        if self.memory.pointer + 1 == len(self.memory.tape):
            self.memory.tape.append(0)
        self.memory.pointer += 1

    def open(self):
        depth = 0
        for i in range(len(self.code)):
            char = self.code[i]
            if char == CHARACTERS[4]:
                depth += 1
            elif char == CHARACTERS[5]:
                depth -= 1
                if depth == -1:
                    while self.memory.tape[self.memory.pointer] is not 0:
                        nested_code = Compiler(self.code[:i], self.memory)
                        nested_code.run()
                    self.code = self.code[i:]
                    break
        else:
            raise RuntimeError(CHARACTERS[5] + " not found for " + CHARACTERS[4])

    def close(self):
        return
        # raise RuntimeError(CHARACTERS[4] + " not found for " + CHARACTERS[5])

    def write(self):
        val = self.memory.tape[self.memory.pointer]
        if val == 10:
            print()
        else:
            print(chr(val), end="")

    def read(self):
        if len(self.memory.input_buffer) == 0:
            self.memory.input_buffer = [ord(character) for character in input()]
            self.memory.input_buffer.append(10)
        num = self.memory.input_buffer[0]
        self.memory.input_buffer = self.memory.input_buffer[1:]
        self.memory.tape[self.memory.pointer] = num


if __name__ == "__main__":
    with open('brainF.txt', 'r') as file:
        raw = file.read()

    pure_code = ''.join([i for i in raw if i in CHARACTERS])

    print(pure_code)

    compiler = Compiler(pure_code)
    print(compiler.run())
