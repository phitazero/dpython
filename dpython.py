import subprocess
import re
import sys

PYTHON_EXECUTABLE = "python"

# added to json import so no collisions occur
prefix = "_ϕナ"

PRELUDE = f"import json as {prefix}json"

PRINT_TEMPLATE = f"{{0}}print({prefix}json.dumps({{1}}, indent=4));print(\"\\n\")"
DUMP_TEMPLATE = f"{{0}}{prefix}json.dump({{1}}, open(\"{{2}}.json\", \"w\"), indent=4)"

try: codeLines = open(sys.argv[1], "r").readlines()
except FileNotFoundError:
	print(f"Can't find {sys.argv[1]}")
	sys.exit()
except IndexError:
	print("File not specified")
	sys.exit()

# getting just the line content, \n's will be brought back later in the code
codeLines = [line.rstrip("\n") for line in codeLines]

def repl(m):
	if m.group(3) == "":
		return PRINT_TEMPLATE.format(*m.groups())
	else:
		return DUMP_TEMPLATE.format(*m.groups())

reParts = ("^(\\s*)" "#", "([^#]*?)", "=>", "([A-Za-z0-9_]*)", "$")
r = re.compile("\\s*".join(reParts))

formattedCodeLines = [r.sub(repl, line) for line in codeLines]
formattedCodeLines = [PRELUDE] + formattedCodeLines

code = "\n".join(formattedCodeLines)

proc = subprocess.run(
	[PYTHON_EXECUTABLE, "-"] + sys.argv[2:],
	input = code.encode(),
	stdout = sys.stdout,
	stderr = sys.stderr
	)

sys.exit(proc.returncode)