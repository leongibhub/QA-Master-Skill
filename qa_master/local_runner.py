"""Local, scoped, bounded test execution with evidence; no shell or remote host."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import subprocess,os,time,json,hashlib,uuid
@dataclass(frozen=True)
class RunPermit:
    project:str
    command:tuple[str,...]
    workdir:str
    approver:str
    artifact_version:str
    def verify(self,project,command,workdir,artifact_version):
        if not all((self.project,self.command,self.workdir,self.approver,self.artifact_version)):raise PermissionError('Missing approval')
        if (self.project,self.command,self.workdir,self.artifact_version)!=(project,tuple(command),workdir,artifact_version):raise PermissionError('Execution scope mismatch')
ALLOWED={'pytest','python','python3'}
def run_local(project,argv,workdir,artifact_version,permit,output_dir,timeout=60):
    if not isinstance(argv,(list,tuple)) or not argv or any(not isinstance(a,str) or '\x00' in a for a in argv):raise ValueError('Invalid argv')
    if argv[0] not in ALLOWED:raise PermissionError('Unsupported executable')
    if argv[0] in ('python','python3') and (len(argv)<3 or argv[1]!='-m' or argv[2] not in ('pytest','unittest')):raise PermissionError('Only test modules allowed')
    if not 1<=timeout<=3600:raise ValueError('Invalid timeout')
    base=Path(workdir).resolve(strict=True)
    if not base.is_dir():raise ValueError('Working directory missing')
    permit.verify(project,argv,str(base),artifact_version)
    output=Path(output_dir).resolve();output.mkdir(parents=True,exist_ok=True)
    if output==base or base in output.parents:raise ValueError('Evidence directory must be separate')
    event=str(uuid.uuid4());started=time.time()
    try:
        proc=subprocess.run(argv,cwd=base,capture_output=True,text=True,timeout=timeout,shell=False,
          env={k:v for k,v in os.environ.items() if k not in ('PYTHONSTARTUP','PYTHONPATH')})
        status='PROCESS_SUCCEEDED' if proc.returncode==0 else 'PROCESS_FAILED'
        code=proc.returncode;stdout=proc.stdout;stderr=proc.stderr
    except subprocess.TimeoutExpired as e:
        status='TIMEOUT';code=None;stdout=e.stdout or b'';stderr=e.stderr or b''
        if isinstance(stdout,bytes):stdout=stdout.decode(errors='replace')
        if isinstance(stderr,bytes):stderr=stderr.decode(errors='replace')
    except OSError as e:
        status='ENVIRONMENT_ERROR';code=None;stdout='';stderr=type(e).__name__
    stdout=stdout[:200_000];stderr=stderr[:200_000]
    out=output/(event+'.stdout.txt');err=output/(event+'.stderr.txt');meta=output/(event+'.json')
    out.write_text(stdout,encoding='utf-8');err.write_text(stderr,encoding='utf-8')
    record={'run_id':event,'project':project,'argv':list(argv),'workdir':str(base),'artifact_version':artifact_version,
      'approver':permit.approver,'process_status':status,'business_result':'NOT_ASSESSED','returncode':code,
      'duration_sec':round(time.time()-started,4),'stdout_sha256':hashlib.sha256(stdout.encode()).hexdigest(),
      'stderr_sha256':hashlib.sha256(stderr.encode()).hexdigest(),'stdout_path':str(out),'stderr_path':str(err)}
    meta.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    return record
