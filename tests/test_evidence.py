import tempfile
import unittest
from pathlib import Path

from core.evidence import (
    VerificationStatus,
    VerificationItem,
    VerificationReport,
    EvidenceCollector,
    DeviceVerificationDetails,
)

class TestEvidenceSystem(unittest.TestCase):
    def test_not_run_cannot_claim_pass(self):
        report = VerificationReport(
            feature_name="user-auth",
            specification_status=VerificationStatus.PASS,
            tests_item=VerificationItem(name="Unit Tests", status=VerificationStatus.NOT_RUN),
            analysis_item=VerificationItem(name="Analysis", status=VerificationStatus.PASS),
        )
        self.assertFalse(report.is_fully_passing)

    def test_fully_passing_when_all_pass(self):
        report = VerificationReport(
            feature_name="user-auth",
            specification_status=VerificationStatus.PASS,
            tests_item=VerificationItem(name="Unit Tests", status=VerificationStatus.PASS),
            analysis_item=VerificationItem(name="Analysis", status=VerificationStatus.PASS),
            build_item=VerificationItem(name="Build", status=VerificationStatus.NA),
            integration_item=VerificationItem(name="Integration", status=VerificationStatus.NA),
        )
        self.assertTrue(report.is_fully_passing)


    def test_evidence_collector_writes_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            feat_dir = Path(tmpdir)
            collector = EvidenceCollector(feat_dir)
            
            log_path = collector.record_log("tests.txt", "2 tests passed in 0.5s")
            self.assertTrue(log_path.exists())
            self.assertEqual(log_path.read_text(encoding="utf-8"), "2 tests passed in 0.5s")

            report = VerificationReport(
                feature_name="sample-feat",
                specification_status=VerificationStatus.PASS,
                tests_item=VerificationItem(
                    name="Tests",
                    status=VerificationStatus.PASS,
                    command="npm test",
                    output_summary="2 passed",
                    evidence_file="tests.txt",
                ),
            )
            verif_file = collector.write_verification_report(report)
            self.assertTrue(verif_file.exists())
            content = verif_file.read_text(encoding="utf-8")
            self.assertIn("Verification Report: sample-feat", content)
            self.assertIn("`PASS`", content)
            self.assertIn("`tests.txt`", content)

if __name__ == "__main__":
    unittest.main()
