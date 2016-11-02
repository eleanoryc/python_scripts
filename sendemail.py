import subprocess

def sendmail(filename):

    print filename

    email_msg = 'testemail: ' + filename + ' is the report'
    email_sub = "The report for "
    email_sub = """ " """ + email_sub + """  " """
    email_cmd = "cat " + filename + " | mailx -s %s %s <<<'%s' " % (email_sub, 'echeung@salesforce.com', email_msg)

    try:
        subprocess.check_call(email_cmd,shell=True)
        EMAIL_ERROR_MESSAGES = ""
        EMAIL_SUMMARY_MESSAGES = ""
    except subprocess.CalledProcessError as e:
        print("Exception Cmd : "  + str(e.cmd))
        print("Cmd Return Code : " +  str(e.returncode))



def main(argv=None):
    filename = 'newfile'
    sendmail(filename)
    exit(0)

if __name__ == '__main__':
    main()

