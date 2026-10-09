#!/usr/bin/env python3
"""
Comprehensive test suite for CODESTREAM-lite CLI & MCP Server (bin/codestream).
Tests Lane P1 (Status & State), Lane P2 (Check Runner), Lane P3 (Linters), and Lane P4 (MCP).
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestCodestreamCLI(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="codestream_test_")
        self.root = Path(self.test_dir)
        self.rules_path = self.root / "RULES.md"
        self.rules_path.write_text("# RULES\n\nSeven rules.\n", encoding="utf-8")

        self.codestream_dir = self.root / ".codestream"
        self.codestream_dir.mkdir(parents=True)
        self.active_dir = self.codestream_dir / "active"
        self.active_dir.mkdir(parents=True)
        self.archive_dir = self.codestream_dir / "archive"
        self.archive_dir.mkdir(parents=True)

        self.state_file = self.codestream_dir / "STATE.json"
        self.initial_state = {
            "framework": "CODESTREAM-lite",
            "version": "0.1.0",
            "current_state": 1,
            "active_milestone": "Milestone 1",
            "active_phase": "P1",
            "state_history": [
                {
                    "state": 1,
                    "agent": "github-copilot",
                    "step": "plan",
                    "summary": "Initial draft of spec",
                    "status": "awaiting SPEC_APPROVED",
                }
            ],
            "artifacts": {
                "roadmap": ".codestream/ROADMAP.md",
                "discovery": ".codestream/DISCOVERY.md",
                "active_spec": ".codestream/active/M01-P01-spec.md",
                "project": ".codestream/PROJECT.md",
                "bugs": ".codestream/BUGS.md",
                "features": ".codestream/FEATURES.md",
                "active_wave": None,
            },
        }
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.initial_state, f, indent=2)

        (self.active_dir / "M01-P01-spec.md").write_text("# Spec\n", encoding="utf-8")

        # Set up a sample PROJECT.md for check tests
        self.project_file = self.codestream_dir / "PROJECT.md"
        self.project_file.write_text(
            "# PROJECT\n\n"
            "## The checks (rule 4)\n\n"
            "| Check | Command |\n"
            "|---|---|\n"
            "| fast_echo | echo 'hello test' |\n"
            "| failing_check | sh -c 'echo \"Fatal error line 42\" >&2; exit 1' |\n"
            "| build | N/A (no build step) |\n"
            "| unconfigured | <command> |\n",
            encoding="utf-8",
        )

        repo_root = Path(__file__).resolve().parent.parent
        self.cli_bin = repo_root / "bin" / "codestream"

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def run_cli(self, args, expect_exit=0):
        cmd = [str(self.cli_bin), "--root", str(self.root)] + args
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(
            proc.returncode,
            expect_exit,
            f"Expected {expect_exit}, got {proc.returncode}.\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}",
        )
        return proc

    # ------------------------------------------------------------------
    # Lane P1: Status & State Tests
    # ------------------------------------------------------------------
    def test_status_human_and_json(self):
        res = self.run_cli(["status"])
        self.assertIn("CODESTREAM-lite", res.stdout)
        self.assertIn("Milestone 1", res.stdout)
        self.assertIn("P1", res.stdout)

        res_json = self.run_cli(["status", "--json"])
        data = json.loads(res_json.stdout)
        self.assertTrue(data["valid"])
        self.assertEqual(data["current_state"], 1)
        self.assertEqual(data["active_artifact"], ".codestream/active/M01-P01-spec.md")

    def test_status_error_handling(self):
        self.state_file.write_text("not json", encoding="utf-8")
        res = self.run_cli(["status"], expect_exit=1)
        self.assertIn("Corrupted .codestream/STATE.json", res.stderr)

    def test_state_append_and_archiving(self):
        for i in range(2, 9):
            self.run_cli(
                [
                    "state",
                    "append",
                    "--step",
                    f"step_{i}",
                    "--summary",
                    f"Work for step {i}",
                    "--status",
                    "in_progress",
                    "--archive-threshold",
                    "4",
                ]
            )

        with open(self.state_file, "r", encoding="utf-8") as f:
            state = json.load(f)

        self.assertEqual(state["current_state"], 8)
        self.assertEqual(len(state["state_history"]), 4)

        archive_file = self.archive_dir / "STATE_HISTORY.md"
        self.assertTrue(archive_file.is_file())
        text = archive_file.read_text(encoding="utf-8")
        self.assertIn("State 1 — plan", text)
        self.assertIn("State 2 — step_2", text)

    # ------------------------------------------------------------------
    # Lane P2: Project Check Runner Tests
    # ------------------------------------------------------------------
    def test_check_execution_and_filtering(self):
        # Run only fast_echo
        res = self.run_cli(["check", "--filter", "fast_echo"])
        self.assertIn("PASSED", res.stdout)
        self.assertIn("fast_echo", res.stdout)

        # Run JSON output
        res_json = self.run_cli(["check", "--filter", "fast_echo", "--json"])
        data = json.loads(res_json.stdout)
        self.assertTrue(data["overall_passed"])
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["exit_code"], 0)

        # Run failing check
        res_fail = self.run_cli(["check", "--filter", "failing_check"], expect_exit=1)
        self.assertIn("FAILED", res_fail.stdout)
        self.assertIn("Fatal error line 42", res_fail.stdout)

        # Run all (includes N/A skip and failure)
        res_all_json = self.run_cli(["check", "--json"], expect_exit=1)
        data_all = json.loads(res_all_json.stdout)
        self.assertFalse(data_all["overall_passed"])
        statuses = {r["name"]: r["status"] for r in data_all["results"]}
        self.assertEqual(statuses["fast_echo"], "passed")
        self.assertEqual(statuses["failing_check"], "failed")
        self.assertEqual(statuses["build"], "skipped")
        self.assertEqual(statuses["unconfigured"], "skipped")

    # ------------------------------------------------------------------
    # Lane P3: Spec & Wave Linting Tests
    # ------------------------------------------------------------------
    def test_lint_spec_valid_and_invalid(self):
        valid_spec = self.root / "valid_spec.md"
        valid_spec.write_text(
            "# M1 / Phase 1 — Feature\n\n"
            "## Problem\nProblem statement.\n\n"
            "## Proposed approach\nApproach statement.\n\n"
            "## What you can do after this phase\nUser can do X.\n\n"
            "## What we are not building\n- None\n\n"
            "## Rules and patterns that apply\n- Pattern\n\n"
            "## How we will know it works\n- [ ] It works\n",
            encoding="utf-8",
        )
        res = self.run_cli(["lint", "spec", str(valid_spec)])
        self.assertIn("PASS", res.stdout)

        # Bad spec with missing sections and forbidden AC ID
        bad_spec = self.root / "bad_spec.md"
        bad_spec.write_text(
            "# M1 / Phase 1 — Feature\n\n"
            "## Problem\nProblem statement.\n\n"
            "Verifies AC-101 and Mapped to AC.\n",
            encoding="utf-8",
        )
        res_bad = self.run_cli(["lint", "spec", str(bad_spec)], expect_exit=1)
        self.assertIn("FAIL", res_bad.stdout)
        self.assertIn("AC-101", res_bad.stdout)
        self.assertIn("Missing required section", res_bad.stdout)

    def test_lint_wave_collision(self):
        collision_wave = self.root / "wave_conflict.md"
        collision_wave.write_text(
            "# M1 / Wave W1\n\n"
            "## Lanes\n\n"
            "| Stage | Phase | Spec | Approval | Status |\n"
            "|---|---|---|---|---|\n"
            "| 1 | P1 | .codestream/active/M01-P01-spec.md | approved | building |\n"
            "| 1 | P2 | .codestream/active/M01-P01-spec.md | approved | building |\n\n"
            "## Ownership\n\n"
            "| Phase | Owns (rewrites) | May only add to (shared) |\n"
            "|---|---|---|\n"
            "| P1 | src/shared.py | |\n"
            "| P2 | src/shared.py | |\n",
            encoding="utf-8",
        )
        res = self.run_cli(["lint", "wave", str(collision_wave)], expect_exit=1)
        self.assertIn("FAIL", res.stdout)
        self.assertIn("Ownership collision in Stage 1", res.stdout)

    # ------------------------------------------------------------------
    # Lane P4: MCP Server Stdio Protocol Tests
    # ------------------------------------------------------------------
    def test_mcp_protocol_handshake_and_tools(self):
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "codestream_status", "arguments": {}},
            },
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "codestream_run_checks",
                    "arguments": {"filter": "fast_echo"},
                },
            },
        ]

        input_str = "\n".join(json.dumps(r) for r in requests) + "\n"
        proc = subprocess.run(
            [str(self.cli_bin), "--root", str(self.root), "mcp"],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(proc.returncode, 0)
        lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
        self.assertEqual(len(lines), 4)

        resp1 = json.loads(lines[0])
        self.assertEqual(resp1["id"], 1)
        self.assertEqual(resp1["result"]["serverInfo"]["name"], "codestream-mcp")

        resp2 = json.loads(lines[1])
        self.assertEqual(resp2["id"], 2)
        tool_names = [t["name"] for t in resp2["result"]["tools"]]
        self.assertIn("codestream_status", tool_names)
        self.assertIn("codestream_state_append", tool_names)
        self.assertIn("codestream_run_checks", tool_names)
        self.assertIn("codestream_lint_spec", tool_names)

        resp3 = json.loads(lines[2])
        self.assertEqual(resp3["id"], 3)
        status_content = json.loads(resp3["result"]["content"][0]["text"])
        self.assertTrue(status_content["valid"])
        self.assertEqual(status_content["milestone"], "Milestone 1")

        resp4 = json.loads(lines[3])
        self.assertEqual(resp4["id"], 4)
        check_content = json.loads(resp4["result"]["content"][0]["text"])
        self.assertTrue(check_content["overall_passed"])


if __name__ == "__main__":
    unittest.main()
