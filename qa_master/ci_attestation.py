"""Verify GitLab CI metadata; NOT proof of artifact authenticity."""
from __future__ import annotations
from dataclasses import dataclass
import re

_SHA=re.compile(r'^[0-9a-f]{40}$')
class AttestationError(ValueError):pass
@dataclass(frozen=True)
class ExpectedRun:
    project_id:int
    job_id:int
    pipeline_id:int
    commit_sha:str
    ref:str
    environment:str
    def validate(self):
        if any(type(x) is not int or x<1 for x in (self.project_id,self.job_id,self.pipeline_id)):
            raise AttestationError('Invalid IDs')
        if not isinstance(self.commit_sha,str) or not _SHA.fullmatch(self.commit_sha):
            raise AttestationError('Full 40-character commit SHA required')
        if not isinstance(self.ref,str) or not self.ref.strip() or not isinstance(self.environment,str) or not self.environment.strip():
            raise AttestationError('Ref and environment required')

def assess_ci_job(reader,expected:ExpectedRun,*,protected_ref_required=True):
    expected.validate()
    project=reader.project(expected.project_id)
    if type(project.get('id')) is not int or project['id']!=expected.project_id:
        raise AttestationError('Project mismatch')
    job=reader.job(expected.project_id,expected.job_id)
    pipeline=reader.pipeline(expected.project_id,expected.pipeline_id)
    reasons=[]
    if job.get('id')!=expected.job_id:reasons.append('JOB_ID_MISMATCH')
    if job.get('status')!='success':reasons.append('JOB_NOT_SUCCESS')
    if (job.get('pipeline') or {}).get('id')!=expected.pipeline_id:reasons.append('JOB_PIPELINE_MISMATCH')
    if (job.get('commit') or {}).get('id')!=expected.commit_sha:reasons.append('JOB_COMMIT_MISMATCH')
    if pipeline.get('id')!=expected.pipeline_id:reasons.append('PIPELINE_ID_MISMATCH')
    if pipeline.get('sha')!=expected.commit_sha:reasons.append('PIPELINE_COMMIT_MISMATCH')
    if pipeline.get('ref')!=expected.ref:reasons.append('PIPELINE_REF_MISMATCH')
    if pipeline.get('status')!='success':reasons.append('PIPELINE_NOT_SUCCESS')
    if protected_ref_required and pipeline.get('ref_protected') is not True:reasons.append('PROTECTED_REF_NOT_CONFIRMED')
    if (job.get('environment') or {}).get('name')!=expected.environment:reasons.append('ENVIRONMENT_MISMATCH')
    return {'metadata_matches':not reasons,'reasons':reasons,'project_id':expected.project_id,
            'job_id':expected.job_id,'pipeline_id':expected.pipeline_id,
            'commit_sha':expected.commit_sha,'artifact_authenticated':False,
            'provenance':'CI_METADATA_CHECKED' if not reasons else 'CI_METADATA_REJECTED',
            'next_step':'Retrieve artifact from authenticated job, hash it, enforce provenance policy'}
