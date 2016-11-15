# avtm/tapebox
#### avtm stands for 'abstract virtual tape machine'
#### tapebox implements an abstract machine in Python3.

Wikipedia: [abstract machine](https://en.wikipedia.org/wiki/Abstract_machine)

### Status
There's work to do.

### Why
Generally, it's a very interesting exercise in thought, computation, and programming.

### How
Fork, clone, or download avtm/tapebox and run `main.py`, but there is currently not much you can do other than play with the interpretter. It will be much more interesting once you can write a tapebox program source file and have the machine execute and run it!

### Instruction Set

Instruction command keywords in the `Core` class shown below.

Functionality for instructions are defined in `core.py`
as methods of `Core`. The instruction set methods are named using the pattern of `call_UPPERCASE`, like `call_WRITE`, or `call_READ`.

For example, when a program (tape) parses a `.w` keyword token, it is mapped to the call_WRITE method.

```
class Core():
    def __init__(self):
        self.instructions = ['+','-','.w','.r','.n','.s','.d','.m','.c','.p']
        self.opchars = ['+','-','*','/']
        self.TAPE = Tape()
```
