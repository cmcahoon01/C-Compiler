import brainRunner
import CToBrainF

with open('C.txt', 'r') as file:
    raw = file.read().split("\n")

converter = CToBrainF.JavaToBrainFConverter()
converter.run(raw)
print(converter.memory.output)

pure_code = ''.join([i for i in converter.memory.output if i in brainRunner.CHARACTERS])

compiler = brainRunner.Compiler(pure_code)
print(compiler.run())
