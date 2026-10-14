"""Artifact-bound approvals for QA workflows (no identity-provider claim)."""
from __future__ import annotations
import hashlib,json,re
from dataclasses import dataclass,asdict

SHA256=re.compile(r'^[0-9a-f]{64}$')

def artifact_digest(document):
    """Stable digest of an exact JSON-serializable artifact."""
    raw=json.dumps(document,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

@dataclass(frozen=True)
class ArtifactApproval:
    kind:str
    project:str
    scope:str
    artifact_sha256:str
    reviewer:str
    decision:str='APPROVED'
    def __post_init__(self):
        if not all(isinstance(v,str) and v.strip() for v in
                   (self.kind,self.project,self.scope,self.reviewer)):
            raise ValueError('Missing approval attributes')
        if not SHA256.fullmatch(self.artifact_sha256):
            raise ValueError('Expected exact SHA-256 artifact identifier')
        if self.decision!='APPROVED':raise ValueError('Approval must be affirmative')
    def authorize(self,*,kind,project,scope,artifact):
        if (kind,project,scope)!=(self.kind,self.project,self.scope):
            raise PermissionError('Approval scope mismatch')
        if artifact_digest(artifact)!=self.artifact_sha256:
            raise PermissionError('Artifact was modified after approval')
        return True

def approve_artifact(*,kind,project,scope,artifact,reviewer):
    """Build a record from an explicit human decision, NOT authenticate a reviewer."""
    return ArtifactApproval(kind,project,scope,artifact_digest(artifact),reviewer)

def check_approval(record,*,kind,project,scope,artifact):
    if not isinstance(record,dict):return False
    try:
        approval=ArtifactApproval(**record)
        return approval.authorize(kind=kind,project=project,scope=scope,artifact=artifact)
    except (TypeError,ValueError,PermissionError):return False

def approval_record(approval):
    return asdict(approval)
