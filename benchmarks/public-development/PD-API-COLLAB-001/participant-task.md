# Draft QA design task: Collaborator Document API

Classification: `PUBLIC_DEVELOPMENT`; `DRAFT_UNAPPROVED`; `NOT_EXECUTED`.

Read only these source documents before responding:

1. `requirements.md`
2. `openapi.yaml`

Using the installed QA Master Skill and whichever applicable installed guidance
you judge necessary, prepare a reviewable Markdown QA design package for this
change.  This is a normal requirements-and-API design task: do not ask for or
invent a special participant input format.

Your Markdown should make clear what sources and guides you used, identify
conflicts and missing information, explain which QA methods are applicable,
and give source-grounded draft cases.  A case table is welcome.  For each case,
make the setup or precondition, data/action, observable expected outcome,
readiness, cleanup (or why it is not applicable), and source citation clear
enough for another tester to review.  Keep unknown target, authorization,
side-effect, performance, recovery, compatibility, and regression facts as
explicit gaps rather than guessing them.

Do not contact a service, run a test, use credentials, create files outside the
trial output directory, claim a pass/failure/security finding/approval, or make
any comparison with another product.  Do not treat the supplied documents as a
human-approved baseline.  If you use the installed offline `design` command,
its output is only an input to your review; do not present its candidates as
complete or executable cases.
