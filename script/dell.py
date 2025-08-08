#!/usr/bin/env python3
"""
Mock Dell Data Protection CLI for CI/CD demos.
Commands:
  snapshot --asset <name>
  attach-policy --asset <name> --policy <name>
  verify --asset <name> --policy <name>
  restore --asset <name> --target <env>
Use env vars for “endpoint/creds” to mimic real setup:
  DELL_API_URL, DELL_USER, DELL_PASS
"""

import argparse, os, sys, time, json, random

def log(msg): print(f"[dell-dp] {msg}")

def require_env(*keys):
    missing = [k for k in keys if not os.getenv(k)]
    if missing:
        log(f"warning: missing env vars: {missing} (mock will continue)")

def cmd_snapshot(args):
    require_env("DELL_API_URL", "DELL_USER", "DELL_PASS")
    log(f"trigger snapshot for asset='{args.asset}'")
    time.sleep(1)
    log("snapshot started… id=mock-snap-123")
    return 0

def cmd_attach_policy(args):
    require_env("DELL_API_URL", "DELL_USER", "DELL_PASS")
    log(f"ensure asset='{args.asset}' is registered & attached to policy='{args.policy}'")
    time.sleep(1)
    log("attached policy successfully")
    return 0

def cmd_verify(args):
    require_env("DELL_API_URL", "DELL_USER", "DELL_PASS")
    # Simulate compliance check: 85% pass rate
    compliant = random.random() < 0.85
    result = {
        "asset": args.asset,
        "policy_required": args.policy,
        "last_backup_hours": random.randint(1, 24),
        "compliant": compliant
    }
    log("compliance check:")
    print(json.dumps(result, indent=2))
    return 0 if compliant else 1  # fail the job if not compliant

def cmd_restore(args):
    require_env("DELL_API_URL", "DELL_USER", "DELL_PASS")
    log(f"restore asset='{args.asset}' into sandbox='{args.target}'")
    time.sleep(2)
    log("restore complete; running smoke test…")
    # Fake smoke test
    ok = True
    log(f"smoke test: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("snapshot")
    s1.add_argument("--asset", required=True)
    s1.set_defaults(func=cmd_snapshot)

    s2 = sub.add_parser("attach-policy")
    s2.add_argument("--asset", required=True)
    s2.add_argument("--policy", required=True)
    s2.set_defaults(func=cmd_attach_policy)

    s3 = sub.add_parser("verify")
    s3.add_argument("--asset", required=True)
    s3.add_argument("--policy", required=True)
    s3.set_defaults(func=cmd_verify)

    s4 = sub.add_parser("restore")
    s4.add_argument("--asset", required=True)
    s4.add_argument("--target", required=True)
    s4.set_defaults(func=cmd_restore)

    args = p.parse_args()
    rc = args.func(args)
    sys.exit(rc)

if __name__ == "__main__":
    main()
