$ErrorActionPreference = 'Continue'
Set-Location 'D:\QA-Master-Compare'
& 'C:\Program Files\Python\python.exe' -W error::ResourceWarning -m unittest discover -s tests -p test_case_conformance_independent.py -v 1> 'docs\verification\evidence\cr033\task-135-e9e141f\scoped-stdout.txt' 2> 'docs\verification\evidence\cr033\task-135-e9e141f\scoped-stderr.txt'
$LASTEXITCODE | Set-Content -Encoding ascii 'docs\verification\evidence\cr033\task-135-e9e141f\scoped-exit.txt'
exit $LASTEXITCODE
