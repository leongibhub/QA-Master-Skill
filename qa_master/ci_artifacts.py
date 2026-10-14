"""Download JUnit from a verified GitLab CI job archive, without blindly trusting evidence."""
from __future__ import annotations
import hashlib,io,tempfile,zipfile
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request,urlopen
from .ci_attestation import assess_ci_job
from .junit_ingest import ingest_junit
from .evidence_binding import RunManifest,bind_junit
class ArtifactError(ValueError):pass
def fetch_job_junit(reader,expected,case_map,*,junit_entry,max_zip_bytes=10_000_000,max_xml_bytes=5_000_000,artifact_transport=None):
    report=assess_ci_job(reader,expected)
    if not report['metadata_matches']:raise ArtifactError('CI metadata mismatch: '+','.join(report['reasons']))
    if not isinstance(junit_entry,str) or not junit_entry or junit_entry.startswith('/') or '\\' in junit_entry or '..' in junit_entry.split('/'):raise ArtifactError('Unsafe entry path')
    url=reader.origin+'/api/v4/projects/'+quote(str(expected.project_id),safe='')+'/jobs/'+str(expected.job_id)+'/artifacts'
    headers={'Accept':'application/zip'}
    if reader.token:headers['PRIVATE-TOKEN']=reader.token
    def download(url,headers,limit):
        with urlopen(Request(url,headers=headers,method='GET'),timeout=20) as response:
            blob=response.read(limit+1)
            if len(blob)>limit:raise ArtifactError('ZIP too large')
            return blob
    data=(artifact_transport or download)(url,headers,max_zip_bytes)
    if not isinstance(data,bytes) or len(data)>max_zip_bytes:raise ArtifactError('Invalid/oversized ZIP')
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            infos=archive.infolist()
            if len(infos)>500:raise ArtifactError('Too many ZIP members')
            matches=[i for i in infos if i.filename==junit_entry and not i.is_dir()]
            if len(matches)!=1:raise ArtifactError('JUnit entry missing or duplicate')
            if matches[0].file_size>max_xml_bytes:raise ArtifactError('JUnit XML too large')
            with archive.open(matches[0]) as stream:
                xml=stream.read(max_xml_bytes+1)
                if len(xml)>max_xml_bytes:raise ArtifactError('JUnit XML exceeds limit')
    except (zipfile.BadZipFile,RuntimeError) as exc:raise ArtifactError('Invalid artifact ZIP') from exc
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'junit.xml';path.write_bytes(xml)
        parsed=ingest_junit(path,case_map,max_bytes=max_xml_bytes)
        manifest=RunManifest(str(expected.project_id),expected.commit_sha,expected.environment,
                            str(expected.job_id),hashlib.sha256(xml).hexdigest(),tuple(r['case_id'] for r in parsed['runs']))
        bound=bind_junit(parsed,manifest,str(path))
    bound.update({'job_metadata_checked':True,'artifact_downloaded_from_job_api':True,
                  'archive_sha256':hashlib.sha256(data).hexdigest(),'source_authenticated':False,
                  'provenance':'CI_ARTIFACT_FETCHED_NOT_ATTESTED'})
    return bound
