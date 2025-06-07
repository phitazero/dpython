import subprocess
import re
import sys
import ast
import json

PYTHON_EXECUTABLE = "python"

# added to json import so no collisions occur
prefix = "_ϕナ"

PRELUDE = f"import json as {prefix}json"

PRINT_TEMPLATE = f"{{0}}print({prefix}json.dumps({{1}}, indent=4));print(\"\\n\")"
WRITE_TEMPLATE = f"{{0}}{prefix}json.dump({{1}}, open(\"{{3}}.json\", \"w\"), indent=4)"
APPEND_TEMPLATE = f"{{0}}open(\"{{3}}.json\", \"a\").write({prefix}json.dumps({{1}}, indent=4) + \"\\n\\n\")"
CLEAR_TEMPLATE = f"{{0}}open(\"{{3}}.json\", \"w\")"

try: codeLines = open(sys.argv[1], "r").readlines()
except FileNotFoundError:
	print(f"Can't find {sys.argv[1]}")
	sys.exit()
except IndexError:
	print("File not specified")
	sys.exit()

# getting just the line content, \n's will be brought back later in the code
codeLines = [line.rstrip("\n") for line in codeLines]

stdoutFormatTo = None
stdoutFormatOp = None

def parseStdoutDirectives(codeLines):
	def repl(m):
		global stdoutFormatTo
		global stdoutFormatOp

		if not stdoutFormatOp is None:
			print("\"Note: only one directive capturing stdout can be used at a time\"")
			print("                                                 - the README on github")
			exit(1)

		stdoutFormatOp, stdoutFormatTo = m.groups()

	reParts = ("^" "#", "\\$", "(=>|=>>)", "([A-Za-z0-9_]*)", "$")
	r = re.compile("\\s*".join(reParts))

	return [r.sub(repl, line) for line in codeLines]

def replaceDirectives(codeLines):
	def repl(m):
		var = m.group(2)
		op = m.group(3)
		dest = m.group(4)
		if var == "":
			return CLEAR_TEMPLATE.format(*m.groups())
		elif op == "=>" and dest != "":
			return WRITE_TEMPLATE.format(*m.groups())
		elif op == "=>>" and dest != "":
			return APPEND_TEMPLATE.format(*m.groups())
		elif stdoutFormatTo is None:
			return PRINT_TEMPLATE.format(*m.groups())

	reParts = ("^(\\s*)" "#", "([^#]*?)", "(=>|=>>)", "([A-Za-z0-9_]*)", "$")
	r = re.compile("\\s*".join(reParts))

	return [r.sub(repl, line) for line in codeLines]

codeLines = parseStdoutDirectives(codeLines)
formattedCodeLines = [PRELUDE] + replaceDirectives(codeLines)

code = "\n".join(formattedCodeLines)

def reformatJSON(text):
	try:
		obj = ast.literal_eval(text)
	except: return

	if type(obj) != dict and type(obj) != list: return

	try:
		jsonStr = json.dumps(obj, indent=4)
	except: return

	return jsonStr

if stdoutFormatOp is None:
	proc = subprocess.run(
		[PYTHON_EXECUTABLE, "-"] + sys.argv[2:],
		input = code.encode(),
		stdout = sys.stdout,
		stderr = sys.stderr
	)
	returncode = proc.returncode

else:
	proc = subprocess.Popen(
		[PYTHON_EXECUTABLE, "-u", "-"] + sys.argv[2:],
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE,
		stderr = sys.stderr,
		text = True
	)

	proc.stdin.write(code)
	proc.stdin.close()

	for line in proc.stdout:
		jsonStr = reformatJSON(line)
		if jsonStr is None: print(line, end="")
		else:
			if stdoutFormatTo == "":
				print(jsonStr, end="")
			elif stdoutFormatOp == "=>":
				open(f"{stdoutFormatTo}.json", "w").write(jsonStr)
			else:
				open(f"{stdoutFormatTo}.json", "a").write(jsonStr + "\n\n")

	proc.wait()
	returncode = proc.returncode

sys.exit(returncode)