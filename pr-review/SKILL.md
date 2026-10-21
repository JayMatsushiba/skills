---
name: pr-review
description: Review an open work-item PR with two new agents, one running /content-review on the prose and one running /code-review at max effort, and post their findings on the PR as review comments. Then hand the PR back to the agent that wrote it to address the feedback. Use when a work-item PR has been opened, or when asked to "review PR N", "run the reviews", or "get agent reviews on this PR".
argument-hint: "<PR number>"
---

# PR review

Run this from the main session (the one that starts agents), not from the
agent that wrote the PR. The reviewers must be new agents, so they read the
PR without the author's context.

## 1. Check the PR

```bash
gh pr view <PR> --json number,title,headRefName,baseRefName,state,isDraft,body,url
gh pr diff <PR> --name-only
```

- Stop if the PR is closed or merged.
- Note the issue it closes (`Closes #N` in the body) and the author agent,
  if known.
- Sort the changed files into **prose** (`README.md`, `SPEC.md`, other
  `.md`, `.qmd`, and notebooks with text) and **code** (everything else).
  A `.qmd` file counts as both.

## 2. Start both reviewers at once

Start two agents in the same message so they run in parallel. Give each
`isolation: "worktree"` so neither touches the author's working directory.
Neither reviewer edits, commits or pushes: they only comment.

**Code reviewer:**

> Review PR #<PR> in <owner>/<repo>. Run `/code-review max <PR> --comment` so
> the findings are posted as inline comments on the PR. Don't apply fixes, and
> don't commit or push. When it's done, reply with the number of findings
> posted, grouped by severity, and a one-line summary of each.

**Content reviewer** (skip if no prose files changed, and say so in the
summary):

> Review the prose in PR #<PR> in <owner>/<repo> as a project manager would
> read it. Check out the PR head in your worktree
> (`gh pr checkout <PR> --detach`), then run `/content-review <prose files>`
> on these files: <list>. Don't use `--fix`, and don't commit or push.
>
> Post the findings as one PR review with event `COMMENT`. Each finding on a
> line the PR changed becomes an inline comment on that line, with the
> check, the current text and the suggested rewrite (use a ```suggestion
> block when the rewrite replaces whole lines). Put findings on unchanged
> lines, the word counts and the open questions in the review body:
>
> ```bash
> gh api repos/<owner>/<repo>/pulls/<PR>/reviews --input review.json
> ```
>
> where `review.json` has `commit_id` (the PR head SHA), `event: "COMMENT"`,
> `body`, and `comments: [{path, line, side: "RIGHT", body}]`. Reply with the
> number of comments posted and the open questions.

GitHub doesn't let you request changes on your own PR, so both reviews use
`COMMENT`.

## 3. Check the reviews landed

When both agents report back:

```bash
gh pr view <PR> --json reviews --jq '.reviews[] | {author: .author.login, state, submittedAt}'
gh api repos/<owner>/<repo>/pulls/<PR>/comments --paginate --jq 'length'
```

If a reviewer failed to post, post its findings yourself as a PR comment so
the feedback is in GitHub, not only in chat.

## 4. Hand back to the author

The feedback goes back to the agent that wrote the PR:

- **If the author agent is still running** (or can be resumed), send it a
  message with `SendMessage`: "Reviews are posted on PR #<PR>. Run
  `/work-item --feedback <PR>`."
- **Otherwise,** start one new agent on the same PR with
  `/work-item --feedback <PR>`. It picks up the author's branch and works
  only on that PR.

Don't fix the findings in this session, and don't give the same PR to two
agents.

## 5. Report

Reply with the PR link, the number of findings from each reviewer, the most
serious ones in a line each, the content reviewer's open questions, and which
agent the PR was handed to. After it addresses the reviews, that agent asks
the developer for the human review (`work-item` Stage 5) before any merge.
