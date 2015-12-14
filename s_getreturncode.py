from subprocess import CalledProcessError, check_output

try:
    output = check_output(["ls", "non existent"])
    returncode = 0
    #return True
except CalledProcessError as e:
    output = e.output
    returncode = e.returncode
    #return False

print(returncode)
