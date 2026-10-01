"""Offline tests. No network, no keys needed. Run: python3 ops/tests/test_ops.py"""
import json, os, sys, tempfile, unittest, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ops.lib import llm, state
from ops.router import route as R
import ops.run as run


class Sandbox(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        state.STATE = t / "state"; state.QUEUE = t / "queue"
        for s in state.STAGES: (state.QUEUE / s).mkdir(parents=True)
    def tearDown(self): self.tmp.cleanup()


class TestRouting(Sandbox):
    def test_rules(self):
        self.assertEqual(R.route("make the hero copy shorter, too wordy")["route"], "copy_trim")
        self.assertEqual(R.route("fix the json-ld schema and sitemap")["route"], "seo_work")
        self.assertEqual(R.route("is chatgpt citing us? check visibility")["route"], "citation_probe")
        self.assertEqual(R.route("find backlink prospects")["skill"], "backlink-prospecting")
    def test_ambiguous_goes_to_review(self):
        self.assertEqual(R.route("hello there")["route"], "review")


class TestDecisions(Sandbox):
    Q = {"k": {"type": "choice", "instructions": "x", "criteria": {"a": "A", "b": "B"}},
         "n": {"type": "noul", "instructions": "y"}}
    def test_dry_run_is_honest(self):
        d = llm.decide({"m": "t"}, self.Q)
        self.assertTrue(d["simulated"]); self.assertEqual(d["decisions"]["k"]["status"], "needs_review")
        self.assertIsNone(d["answers"]["k"]["probabilities"])
    def test_confidence_gate(self):
        hi = {"k": {"probabilities": {"a": 0.93, "b": 0.07}}, "n": {"noul": 0.96}}
        lo = {"k": {"probabilities": {"a": 0.52, "b": 0.48}}, "n": {"noul": 0.55}}
        self.assertEqual(llm.interpret(self.Q, hi)["k"]["status"], "selected")
        self.assertEqual(llm.interpret(self.Q, lo)["k"]["status"], "needs_review")
        self.assertEqual(llm.interpret(self.Q, lo)["n"]["status"], "needs_review")
    def test_validation(self):
        with self.assertRaises(llm.LLMError): llm.decide({}, {"k": {"type": "choice", "instructions": "x", "criteria": {"a": "A"}}})
    def test_other_label_never_auto_selected(self):
        q = {"k": {"type": "choice", "instructions": "x", "criteria": {"a": "A", "other": "O"}}}
        self.assertEqual(llm.interpret(q, {"k": {"probabilities": {"other": 0.99, "a": 0.01}}})["k"]["status"], "needs_review")
    def test_scrub_removes_key_values(self):
        old = os.environ.get("GEMINI_API_KEY")
        fake = "fake-" + "x" * 12          # built at runtime; never a literal in the repo
        os.environ["GEMINI_API_KEY"] = fake
        try:
            self.assertNotIn(fake, llm._scrub("boom " + fake + " boom"))
        finally:
            if old is None: os.environ.pop("GEMINI_API_KEY", None)
            else: os.environ["GEMINI_API_KEY"] = old


class TestState(Sandbox):
    def test_enqueue_is_idempotent(self):
        a, new1 = state.enqueue({"x": 1}); b, new2 = state.enqueue({"x": 1})
        self.assertEqual(a, b); self.assertTrue(new1); self.assertFalse(new2)
    def test_claim_finish_recover(self):
        jid, _ = state.enqueue({"x": 2})
        cid, job = state.claim(); self.assertEqual(cid, jid)
        self.assertEqual(state.recover(), 1)               # interrupted -> back to inbox
        state.claim(); state.finish(jid, "done", {"ok": True})
        self.assertEqual(state.listing()["done"], [jid])
        self.assertFalse(state.enqueue({"x": 2})[1])       # done jobs never re-queue
    def test_budget_counts(self):
        state.budget_spend(2, 0.01); self.assertEqual(state.budget_read()["calls"], 2)


class TestRunner(Sandbox):
    def test_gate_blocks_approval_actions(self):
        self.assertFalse(run.gate("send_outreach")["allowed"]); self.assertTrue(run.gate("note")["allowed"])
    def test_shell_allowlist(self):
        self.assertFalse(run.run_shell(["rm", "-rf", "/"])["ok"])
    def test_lead_triage_dry_run_never_auto_routes(self):
        res = run.run_workflow("lead-triage", False, "Hi, need a launch video next week")
        self.assertEqual(res["ctx"]["route"]["destination"], "review")
    def test_scam_text_dry_run_still_review(self):
        res = run.run_workflow("lead-triage", False, "Connect your wallet to claim airdrop")
        self.assertEqual(res["ctx"]["route"]["destination"], "review")
    def test_page_audit_runs(self):
        res = run.run_workflow("page-audit")
        self.assertTrue(res["ctx"]["audit"]["ok"], res["ctx"]["audit"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
