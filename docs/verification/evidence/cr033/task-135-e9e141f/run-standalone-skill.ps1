$ErrorActionPreference = 'Stop'
$repo = 'D:\QA-Master-Compare'
$evidence = Join-Path $repo 'docs\verification\evidence\cr033\task-135-e9e141f'
$scratch = Join-Path $env:TEMP 'ccsa-e9e141f-r1'
$log = Join-Path $evidence 'standalone-skill.log'
New-Item -ItemType Directory -Force -Path $scratch | Out-Null
$archive = Join-Path $scratch 'src.zip'
$source = Join-Path $scratch 'src'
$wheelDir = Join-Path $scratch 'wheel'
$venv = Join-Path $scratch 'venv'
$consumer = Join-Path $scratch 'consumer'
$skill = Join-Path $scratch 'skill'
New-Item -ItemType Directory -Force -Path $wheelDir,$consumer | Out-Null
Set-Location $repo
& git archive --format=zip --output $archive HEAD *>> $log
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Expand-Archive -LiteralPath $archive -DestinationPath $source -Force
& 'C:\Program Files\Python\python.exe' -m pip wheel $source --no-deps --no-build-isolation -w $wheelDir *>> $log
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& 'C:\Program Files\Python\python.exe' -m venv $venv *>> $log
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$python = Join-Path $venv 'Scripts\python.exe'
$wheel = Get-ChildItem $wheelDir -Filter '*.whl' | Select-Object -First 1
if ($null -eq $wheel) { throw 'WHEEL_NOT_CREATED' }
& $python -m pip install --no-index --no-deps $wheel.FullName *>> $log
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Copy-Item (Join-Path $source 'examples\design-methods.json') (Join-Path $consumer 'bundle.json')
Copy-Item (Join-Path $source 'qa_master\skills\codex\examples\method-cases.json') (Join-Path $consumer 'cases.json')
& $python -I -m qa_master install-codex --target $skill *>> $log
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Set-Location $consumer
& $python -I (Join-Path $skill 'scripts\qa.py') audit-method-cases --input bundle.json --cases cases.json --output skill-audit.md --format markdown *>> $log
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if (-not (Test-Path 'skill-audit.md')) { throw 'SKILL_OUTPUT_MISSING' }
$output = Get-Content -Raw 'skill-audit.md'
if ($output -notmatch 'DRAFT_UNAPPROVED' -or $output -notmatch 'NOT_EXECUTED') { throw 'SKILL_OUTPUT_STATUS_MISSING' }
Get-Item 'skill-audit.md' | Format-List Name,Length | Out-File -Append -Encoding utf8 $log
exit 0
