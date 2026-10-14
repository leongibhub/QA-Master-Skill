import unittest
from qa_master.review_packet import create_review_packet, build_requirement_drafts

def candidate(line=1,risks=None):
    return {'source':{'path':'app.py','line':line,'symbol':'f','ref':'sha123'},
            'observed':'function found','risk_hints':risks or []}
def codes(packet):return [x['code'] for x in packet['findings']]

class ReviewPacketTests(unittest.TestCase):
    def test_empty(self):self.assertEqual(create_review_packet({'candidates':[]})['statistics']['observations'],0)
    def test_invalid(self):
        with self.assertRaises(ValueError):create_review_packet({})
    def test_source(self):self.assertEqual(create_review_packet({'candidates':[candidate()]})['observations'][0]['source']['path'],'app.py')
    def test_pending(self):self.assertEqual(create_review_packet({'candidates':[candidate()]})['approval'],'PENDING_HUMAN')
    def test_no_oracle(self):self.assertFalse(create_review_packet({'candidates':[candidate()]})['observations'][0]['testable_oracle'])
    def test_branches(self):self.assertIn('BRANCH_BOUNDARIES',codes(create_review_packet({'candidates':[candidate(risks=['BRANCHES'])]})))
    def test_exceptions(self):self.assertIn('ERROR_CONTRACT',codes(create_review_packet({'candidates':[candidate(risks=['EXCEPTIONS'])]})))
    def test_duplicate(self):self.assertIn('DUPLICATE_OBSERVATION',codes(create_review_packet({'candidates':[candidate(),candidate()]})))
    def test_missing_source(self):self.assertIn('MISSING_SOURCE',codes(create_review_packet({'candidates':[{'source':{}}]})))
    def test_gap(self):self.assertIn('INSPECTION_GAP',codes(create_review_packet({'candidates':[],'gaps':[{'kind':'UNSUPPORTED'}]})))
    def test_undecided(self):
        p=create_review_packet({'candidates':[candidate()]});self.assertEqual(len(build_requirement_drafts(p,{})['unresolved']),1)
    def test_accepted_still_draft(self):
        p=create_review_packet({'candidates':[candidate()]});k=p['observations'][0]['id']
        result=build_requirement_drafts(p,{k:{'decision':'accept','requirement':'Login','acceptance':'Session created'}})
        self.assertEqual(len(result['requirements']),1);self.assertFalse(result['baseline_approved'])
    def test_missing_acceptance(self):
        p=create_review_packet({'candidates':[candidate()]});k=p['observations'][0]['id']
        self.assertEqual(len(build_requirement_drafts(p,{k:{'decision':'accept','requirement':'Login'}})['unresolved']),1)
    def test_rejection(self):
        p=create_review_packet({'candidates':[candidate()]});k=p['observations'][0]['id']
        self.assertEqual(build_requirement_drafts(p,{k:{'decision':'reject'}})['rejected'],[k])
    def test_wrong_packet(self):
        with self.assertRaises(ValueError):build_requirement_drafts({}, {})
