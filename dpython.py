import subprocess
import re
import sys

PYTHON_EXECUTABLE = "python"

# added to json import so no collisions occur
prefix = "_ϕナ"

PRELUDE = f"import json as {prefix}json"

PRINT_TEMPLATE = f"print({prefix}json.dumps({{0}}, indent=4));print(\"\\n\")"
DUMP_TEMPLATE = f"{prefix}json.dump({{0}}, open(\"{{1}}.json\", \"w\"), indent=4)"

try: codeLines = open(sys.argv[1], "r").readlines()
except FileNotFoundError:
	print(f"Can't find {sys.argv[1]}")
	sys.exit()
except IndexError:
	print("File not specified")
	sys.exit()

def repl(m):
	var, dest = m.groups()

	if dest == "":
		return PRINT_TEMPLATE.format(var)
	else:
		return DUMP_TEMPLATE.format(var, dest)

reParts = ("^", "#", "([A-Za-z_][A-Za-z0-9_]*)", "=>", "([A-Za-z0-9_]*)", "$")
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