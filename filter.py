import operator
import ast

original_message = None

commands = [
    "hello", "help", "time", "date", "calc",
    "search", "translate", "define", "weather", "news",
    "joke", "quote", "flip", "roll", "password",
    "note", "note list", "note delete", "todo add", "todo list",
    "todo done", "remind", "timer", "stopwatch", "open",
    "clear", "history", "settings", "ask", "summarize",
    "explain", "rewrite", "correct", "brainstorm", "plan",
    "screenshot", "system-info", "battery", "volume", "mute", 
    "exit"
]

def calculate():
    ops = {
        ast.Add         : operator.add,
        ast.Sub         : operator.sub,
        ast.Mult        : operator.mul,
        ast.Div         : operator.truediv,
        ast.FloorDiv    : operator.floordiv,
        ast.mod         : operator.mod,
        ast.Pow         : operator.pow,
        ast.USub        : operator.neg,
        ast.UAdd        : operator.pos
    }

    def solve(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float) :
            


def process_message(msg):
    original_message = msg
    print(original_message)

    

    return msg 
