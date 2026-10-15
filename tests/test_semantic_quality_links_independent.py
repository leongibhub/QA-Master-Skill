"""TASK064 independent real link/reparse checks; no mocked filesystem links."""
import copy
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from qa_master import semantic_quality as sq
from test_semantic_quality_independent import fixture,canonical,sha


class SemanticLinkIndependent(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='sq-link-independent-')
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.inputs=self.root/'inputs';self.assets=self.inputs/'assets';self.assets.mkdir(parents=True)
        self.bundle,self.response=fixture();raw=canonical(self.response)
        (self.assets/'response.json').write_bytes(raw)
        (self.assets/'facts.txt').write_bytes(b'Published policies; evaluator-authored development facts.')
        self.bundle['sources'][0]['locator']='assets/facts.txt'
        self.bundle['response']=dict(state='PRESENT',source_path='assets/response.json',byte_count=len(raw),sha256=sha(raw),declared_projection_id=self.bundle['contract']['projection_id'])
        self.path=self.inputs/'bundle.json';self.path.write_bytes(canonical(self.bundle))
    def link(self,kind,path,target):
        self.assertTrue(path.absolute().is_relative_to(self.root.absolute()))
        self.assertTrue(target.absolute().is_relative_to(self.root.absolute()))
        if kind=='junction':
            if os.name!='nt':self.skipTest('NOT_APPLICABLE: junction is Windows-specific')
            result=subprocess.run(['cmd.exe','/c','mklink','/J',str(path),str(target)],capture_output=True)
            self.assertEqual(result.returncode,0,repr(result.stderr+result.stdout))
            self.assertTrue(os.lstat(path).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
        else:
            try:path.symlink_to(target,target_is_directory=True)
            except OSError as error:
                if os.name=='nt' and getattr(error,'winerror',None)==1314:self.skipTest('NOT_EXECUTED: Windows denied real symlink creation (1314)')
                raise
            self.assertTrue(path.is_symlink())
        # Remove only the verified in-fixture link itself; never traverse its target.
        self.addCleanup(lambda: os.rmdir(path) if kind=='junction' else path.unlink())
        return path
    def rejected(self,fn):
        with self.assertRaises(sq.SemanticQualityError) as error:fn()
        self.assertEqual(error.exception.code,'LINK_FORBIDDEN')
    def exercise(self,kind,operation):
        target=self.root/'output-real';target.mkdir();sentinel=target/'sentinel.txt';sentinel.write_bytes(b'KEEP')
        if operation=='bundle':
            alias=self.link(kind,self.root/'input-alias',self.inputs)
            self.rejected(lambda:sq.validate_bundle(alias/'bundle.json'))
            self.rejected(lambda:sq.evaluate_bundle(alias/'bundle.json',target/'rejected'))
        elif operation in ('source','response'):
            alias=self.link(kind,self.inputs/'alias',self.assets)
            if operation=='source':self.bundle['sources'][0]['locator']='alias/facts.txt'
            else:self.bundle['response']['source_path']='alias/response.json'
            self.path.write_bytes(canonical(self.bundle))
            self.rejected(lambda:sq.validate_bundle(self.path))
            self.rejected(lambda:sq.evaluate_bundle(self.path,target/'rejected'))
        elif operation=='output':
            alias=self.link(kind,self.root/'output-alias',target)
            self.rejected(lambda:sq.evaluate_bundle(self.path,alias/'rejected'))
        else:
            result=sq.evaluate_bundle(self.path,target/'published');actual=Path(result['profile_path']).parent
            before={str(p.relative_to(actual)):p.read_bytes() for p in actual.rglob('*') if p.is_file()}
            alias=self.link(kind,self.root/'inspect-alias',target)
            self.rejected(lambda:sq.inspect_result(alias/'published'/actual.name))
            self.assertEqual(before,{str(p.relative_to(actual)):p.read_bytes() for p in actual.rglob('*') if p.is_file()})
        self.assertEqual(sentinel.read_bytes(),b'KEEP');self.assertFalse((target/'rejected').exists())
        self.assertEqual((self.assets/'facts.txt').read_bytes(),b'Published policies; evaluator-authored development facts.')
        self.assertEqual((self.assets/'response.json').read_bytes(),canonical(self.response))


def _case(kind,operation):
    def test(self):self.exercise(kind,operation)
    return test
for _kind in ('junction','symlink'):
    for _operation in ('bundle','source','response','output','inspect'):
        setattr(SemanticLinkIndependent,'test_'+_kind+'_'+_operation,_case(_kind,_operation))
