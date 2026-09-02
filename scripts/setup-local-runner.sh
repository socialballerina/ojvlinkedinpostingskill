#!/usr/bin/env bash
# Register this machine as the runner for the OJV LinkedIn workflow.
#
# After this, pressing the button on the Vercel page runs the job here instead of
# on GitHub's servers, using this machine's own Claude Code login. No API key and
# no CLAUDE_CODE_OAUTH_TOKEN secret needed.
#
# The runner polls GitHub outbound. It opens no inbound port and needs no tunnel.
# When this machine is asleep or the service is stopped, jobs queue on GitHub and
# run when it comes back. GitHub drops a job that has queued for 24 hours.
#
# Undo everything with:  scripts/setup-local-runner.sh remove

set -euo pipefail

REPO="${OJV_REPO:-socialballerina/ojvlinkedinpostingskill}"
DIR="${OJV_RUNNER_DIR:-$HOME/.ojv-actions-runner}"
LABELS="self-hosted,ojv"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing $1. Install it first."; exit 1; }; }

if [ "${1:-install}" = "remove" ]; then
  if [ -d "$DIR" ]; then
    cd "$DIR"
    ./svc.sh stop 2>/dev/null || true
    ./svc.sh uninstall 2>/dev/null || true
    TOKEN=$(gh api -X POST "/repos/$REPO/actions/runners/remove-token" --jq .token 2>/dev/null || true)
    [ -n "$TOKEN" ] && ./config.sh remove --token "$TOKEN" 2>/dev/null || true
    cd - >/dev/null
    rm -rf "$DIR"
    echo "Runner removed and $DIR deleted."
  else
    echo "Nothing installed at $DIR."
  fi
  gh variable delete OJV_RUNNER --repo "$REPO" 2>/dev/null && echo "OJV_RUNNER variable cleared, so runs go back to GitHub's runners." || true
  exit 0
fi

need gh
need curl
gh auth status >/dev/null 2>&1 || { echo "Run 'gh auth login' first."; exit 1; }

# Claude Code has to be able to authenticate as you, on this machine.
if ! command -v claude >/dev/null 2>&1; then
  echo "The claude CLI is not installed. Install it with:"
  echo "  npm install -g @anthropic-ai/claude-code"
  exit 1
fi
if ! claude auth status 2>/dev/null | grep -q '"loggedIn": *true'; then
  echo
  echo "The claude CLI on this machine is not logged in."
  echo "Run 'claude' once, complete the login, then run this script again."
  echo "The desktop app's login is separate, so the CLI needs its own."
  exit 1
fi
echo "Claude Code is installed and logged in."

case "$(uname -s)-$(uname -m)" in
  Darwin-arm64) PKG="osx-arm64" ;;
  Darwin-x86_64) PKG="osx-x64" ;;
  Linux-x86_64) PKG="linux-x64" ;;
  Linux-aarch64) PKG="linux-arm64" ;;
  *) echo "Unsupported platform $(uname -s)-$(uname -m)."; exit 1 ;;
esac

VERSION=$(curl -fsSL https://api.github.com/repos/actions/runner/releases/latest | python3 -c 'import json,sys;print(json.load(sys.stdin)["tag_name"].lstrip("v"))')
TARBALL="actions-runner-${PKG}-${VERSION}.tar.gz"
URL="https://github.com/actions/runner/releases/download/v${VERSION}/${TARBALL}"

mkdir -p "$DIR"
cd "$DIR"
if [ ! -f ./config.sh ]; then
  echo "Downloading runner ${VERSION} for ${PKG}."
  curl -fsSL -o "$TARBALL" "$URL"
  tar xzf "$TARBALL"
  rm -f "$TARBALL"
fi

if [ ! -f .runner ]; then
  echo "Registering with $REPO."
  TOKEN=$(gh api -X POST "/repos/$REPO/actions/runners/registration-token" --jq .token)
  ./config.sh --unattended --replace \
    --url "https://github.com/$REPO" \
    --token "$TOKEN" \
    --name "$(scutil --get ComputerName 2>/dev/null || hostname)-ojv" \
    --labels "$LABELS" \
    --work _work
else
  echo "Already registered."
fi

./svc.sh install >/dev/null
./svc.sh start
echo
gh variable set OJV_RUNNER --body self-hosted --repo "$REPO"
echo
echo "Done. Jobs now run on this machine."
echo "  status : cd $DIR && ./svc.sh status"
echo "  stop   : cd $DIR && ./svc.sh stop      (jobs queue until you start it again)"
echo "  remove : scripts/setup-local-runner.sh remove"
