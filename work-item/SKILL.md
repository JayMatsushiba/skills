---
name: work-item
description: Take one GitHub issue through to a merged PR, as the single agent responsible for it. Creates a branch in its own worktree when work starts, commits the work, opens a PR that closes the issue when the work is nearly done, then, after /pr-review, works through the review comments, asks the developer to review and incorporates their feedback, rebases onto main if main has moved, and squash-merges once the developer approves. Use when asked to "work on #N", "pick up issue N", "address the review on PR N", or to finish and merge a work item. Never switches to another issue or PR.
argument-hint: "<issue number> | --feedback <PR number> | --merge <PR number>"
---

# Work item

A work item is one issue, one branch and one PR. It is the unit of
delegation between agents: each agent owns exactly one, from the first commit
to the merge.

## The one rule

**Work only on your own item.** Don't check out, edit, commit to, push to,
review or merge another item's branch or PR, even to fix something small. If
you find a problem that belongs to another item, or new work outside your
issue, comment on the relevant issue (or open a new issue) and carry on with
your own. Switching causes conflicts between agents.

If the work turns out not to fit the issue (much bigger, blocked, or no longer
needed), stop and tell the developer instead of widening the scope.

## Stage 1: Start (`/work-item <issue>`)

1. **Read the item.** `gh issue view <N> --comments`, the SPEC section it
   links, and `README.md`. If the issue is blocked (see its "Blocked by"),
   say so and stop.
2. **Check it isn't taken.** If a branch or open PR for the issue already
   exists, don't start a second one. Pick up that branch only if the
   developer says its earlier agent is finished with it.
3. **Claim it.** Comment on the issue that work has started and on which
   branch.
4. **Make a worktree and branch** from the latest `main`, so parallel agents
   don't share a working directory. Use `EnterWorktree` when available
   (or the Agent tool's `isolation: "worktree"`), otherwise:

   ```bash
   git fetch origin
   git worktree add ../<repo>-<branch> -b <branch> origin/main
   ```

   Name the branch after the workstream and the work, for example
   `ws3-patterns` or `ws1-geotiff-inputs`. For a fix, describe the fix:
   `fix-july-survey-date`.
5. **Push the branch early** (`git push -u origin <branch>`) so others can see
   the work has started.

## Stage 2: Do the work

- Work through the issue's task list in order. Tick tasks off in the issue
  body as they're done (`gh issue edit`), so progress shows in GitHub.
- **Keep commits neatly organised.** Each commit is one complete, logical
  step that someone can read on its own: one change, its tests, and the docs
  it affects. Don't mix unrelated changes in a commit, and don't leave
  "wip", "fix typo" or "address comments" commits. If the history is messy
  before opening the PR, tidy it: fold small fixes into the commit they fix
  with `git commit --fixup <sha>` and
  `GIT_SEQUENCE_EDITOR=: git rebase --autosquash origin/main`. The
  squash-merge lists these commit messages in the final commit on `main`, so
  they need to read well.
- **Write commit messages for a human reader.** The summary line is a brief,
  plain-language description of the work done, in the imperative, under
  about 70 characters: "Add WS3 fetch of ~100 m ocean-colour maps", not
  "update ws3_fetch.py". The body, if needed, says in a few short lines why
  the change was made and what changed in the results. No jargon a reader of
  the project wouldn't know. End with the attribution line the session gives
  you.
- Run the tests and, for notebooks or reports, render them before each push.
- **Keep README and SPEC true.** If the work changes a fact (a date, a
  confirmed answer, a result), update `README.md` or `SPEC.md` in the same
  branch.
- Record decisions and answers from people in the issue as comments, with
  who and when.

## Stage 3: Open the PR

Open the PR when the work is nearly done: all tasks attempted, tests passing,
and what's left is review. Don't open it before the acceptance criteria can
be checked.

```bash
gh pr create --title "<WS: what this does>" --body-file /tmp/pr.md
```

Body:

```markdown
Closes #<N>. One sentence on what this does.

## Result
Main findings or behaviour, in a few bullets. Say if the result is negative.

## Changes
Files and modules changed, grouped, one line each.

## Testing
What was run and its outcome.

## Open questions
For the developer or reviewers. Leave out if none.
```

Then stop and report the PR number and link. The next step, `/pr-review
<PR>`, starts the reviewers. Don't review your own PR.

## Stage 4: Address review feedback (`--feedback <PR>`)

The reviewers post comments on the PR. The work returns to you: either the
same agent is resumed, or a new agent is started on the same PR with this
skill. Either way, the work stays on this one item.

1. **Read every comment:**

   ```bash
   gh pr view <PR> --json reviews,comments
   gh api repos/{owner}/{repo}/pulls/<PR>/comments --paginate
   ```

2. **Decide on each one:** fix it, or don't and say why. Fix anything that's
   a correctness bug. For prose suggestions, apply them unless they change a
   number, a unit or the meaning of a finding. When a comment needs a fact or
   decision only the developer has, ask instead of guessing.
3. **Commit the fixes** in commits named for what they fix (for example
   "Apply content review: rock conclusion in key findings"). Push.
4. **Reply to each comment** with what was done and the commit, or why
   nothing was changed:

   ```bash
   gh api repos/{owner}/{repo}/pulls/<PR>/comments/<comment_id>/replies -f body="Fixed in <sha>: …"
   ```

5. Post a short summary comment on the PR: what was fixed, what was left and
   why, and questions for the developer.

Then stop and tell the developer the PR is ready for their review (Stage 5).

## Stage 5: Developer review

Every PR gets a human review before it's merged. The agent reviews catch
bugs and wording; the developer checks that the work does what the project
needs. Don't skip this stage, even when the agent reviews found nothing.

1. **Bring the branch up to date first,** so the developer reviews what will
   be merged. If `main` has moved on, rebase as in Stage 6, step 1.
2. **Ask for the review.** Post a PR comment, and tell the developer in the
   session, with:
   - the PR link and, for reports or notebooks, how to see the rendered
     output
   - a few lines on what the PR does and its main results
   - what changed after the agent reviews, and what was left and why
   - open questions that need the developer's decision
3. **Wait for the developer's feedback.** It can come as PR review
   comments, PR comments, or messages in the session. If the agent stopped
   while waiting, `/work-item --feedback <PR>` picks the work up again. Treat it like the agent reviews
   (Stage 4): fix or explain each point, commit with readable messages, push,
   and reply on the PR. Record feedback given in the session as a PR comment
   too, so GitHub holds the full record.
4. **Repeat** steps 2 and 3 until the developer approves. Approval must be
   explicit: "merge it", "approved", or an approving PR review. Fixing the
   last comment isn't approval.

If the developer's feedback changes the scope of the issue, stop and ask
whether to widen this PR or open a new issue, rather than doing both here.

## Stage 6: Rebase and merge (`--merge <PR>`)

Only after the developer has approved in Stage 5.

1. **Rebase if `main` has moved on:**

   ```bash
   git fetch origin
   git merge-base --is-ancestor origin/main HEAD || git rebase origin/main
   ```

   Resolve conflicts by keeping both sides' intent. If a conflict touches
   another item's work in a way you can't resolve without changing its
   meaning, stop and ask. After rebasing, rerun tests and renders, then
   `git push --force-with-lease`. If resolving conflicts changed anything the
   developer approved, show them the change and get approval again.
2. **Check the PR is ready:** CI passes (`gh pr checks <PR>`), every agent
   and developer comment has a reply, and no question is waiting on the
   developer.
3. **Squash-merge:**

   ```bash
   gh pr merge <PR> --squash --delete-branch
   ```

   The `Closes #N` line closes the issue. If the branch is checked out in a
   worktree, leave the worktree first and remove it afterwards
   (`git worktree remove <path>`).
4. Report the merge commit, the closed issue, and any follow-up issues
   opened along the way.
