# Development Board: Gridline

## Project routing

- Project ID: football-game
- Target repository: Sgilmore186/gridline
- Target branch: main
- Push policy: verified direct pushes to main, explicitly authorized 2026-11-24 in Gridline AGENTS.md. No force pushes; private build only for private publication.
- Project rules: https://github.com/Sgilmore186/gridline/blob/main/AGENTS.md
- Dream Board: https://github.com/Sgilmore186/gridline/blob/main/docs/DREAM_BOARD.md
- Enrollment approval/source: Seph requested Gridline integration following shared workflow setup, 2026-11-26.
- Activation: pending

## Cutover safety

This board is prepared, not yet the active queue. The legacy [board snapshot](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md) records a Codex claim over B-018 / 4.3–4.7 from 2026-11-26 (claim commit b92883f, rollback 888bfcf). Its release is not confirmed. The existing agent may finish its assigned work under the old rules. Do not start a competing run or clear the claim based on time alone.

After both integration PRs are merged: fetch the latest Gridline main and PM main, confirm the legacy agent has stopped/released its claim, reconcile its commits, test results, publication and new board entries, and verify Gridline's AGENTS.md points here. Perform a read-only routing pass (active primary, correct repo, skills accessible, valid dependencies, no competing claim). Then change Activation to active and record the handoff in this board, using a normal non-force push under the reviewed enrollment. Only the cutover coordinator may activate after those checks; if uncertain, leave pending. Do not run both queues. For pending activation, the nightly trigger may perform read-only checks and report what is missing but must not modify game code.

## Run claim

- Owner: none (legacy claim unresolved; see cutover)
- Run ID: none
- Claimed/renewed UTC: none
- Starting target commit: none

## Priority repairs

No new repair authorized by this migration. Agents can add reproducible, scoped bugs and necessary quality fixes under the shared execution skill. Known baseline debt: some go-ball and long-gain targets remain outside desired ranges (legacy 3.9); measure before changing and address in Phase 4 validation where applicable.

## Ordered phases

### Historical phases 1–3 and shipped backlog

Existing implementation and history remain at the [legacy board snapshot](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md) and [upgrade plan](https://github.com/Sgilmore186/gridline/blob/main/docs/upgrade-plan.md). Do not rebuild completed passing, predictive engine, intelligent coaching, menus, roster tools, clutch or momentum. Phase 3A signed off; Phase 3B and several recent features remain unplaytested. Their evidence/history is preserved in Gridline reports; verify regressions in B-018/4.7. Design-only B-013 and B-014 are not shipped features.

### B-018 - Phase 4: Ratings and competitive balance

- Objective: independent attributes, realistic local matchups, IQ/AWR, team competitiveness and validated full-game balance.
- Approval: 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- Dependencies: existing phases 1–3 and attribute foundation.
- Phase gate: full acceptance matrix, private publication verified and physical phone/user signoff before the next core phase as specified in Phase 4. Explicit authorization allows 4.3–4.7 implementation before 4.2 publication; do not treat publication or phone verification as already done. Unattended work may continue within this phase where independent, but do not silently waive the final explicit signoff.

#### B-018/4.1 - Audit and baseline

- **Objective:** Preserve reproducible rating baseline.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** none
- **Status:** done
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Verify existing audit/report and baseline provenance; avoid repeating completed work.
- **Toolbox:** Gridline `skills/gridline-validation/SKILL.md`, `node tests/check_scripts.mjs`, `node --test tests/player_attributes.test.mjs`; relevant seeded tools in the Phase 4 spec.
- **Acceptance criteria:** Audit, baseline and specification recorded; no production change required.
- **Evidence:** e2da625 and docs/reports/2026-11-26-phase4-audit.md; historical report says complete.
- **Handoff:** Use as baseline, not a new implementation.

#### B-018/4.2 - Attribute foundation

- **Objective:** Stable player identities, independent attributes and archetypes.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.1
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Inspect existing implementation and attribute tests; preserve canonical attrs, provenance, legacy saves, authored OVR, player IDs and card fields. Do not activate gameplay formulas here.
- **Toolbox:** Gridline `skills/gridline-validation/SKILL.md`, `node tests/check_scripts.mjs`, `node --test tests/player_attributes.test.mjs`; relevant seeded tools in the Phase 4 spec.
- **Acceptance criteria:** Existing attribute fixtures, paired source/dist checks and compatibility evidence; private release/physical verification remain recorded separately.
- **Evidence:** 671cbd1; legacy report says tests pass and paired 80-play regression, but private publication failed and phone review open.
- **Handoff:** No rewrite. Use 4.7 delivery for current tested build; preserve original 4.2 handoff. 4.3 implementation explicitly authorized.

#### B-018/4.3a - Local pass protection

- **Objective:** Individual OL/DL protection.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.2 implementation validated
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Replace global OL averages in protection with assigned pass blockers vs local rushers, strength, agility, acceleration and legal help. Instrument pocket time, pressure, blocks and sacks.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Seeded isolated OL/DL tests show monotonic talent effect and nonzero upsets; no duplicated help or OVR multiplier.
- **Evidence:** Local protection skills replace whole-OL OVR; 3 seeds x100k cells, nonzero upsets,160 held-QB reps median3.20s. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.3b - Local run blocking

- **Objective:** Individual run block and shedding.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3a
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Use local run-block technique, strength, leverage, scheme and assigned/spare blockers against shedding; log wins, sheds and contact location.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Isolated OL/DL tests and mirrored runs show better blocking improves lanes; preserve run-type tactical counters.
- **Evidence:** 14400 live runs,8 conditions x6types x300. Neutral medians3.18-4.06yd. OL60 mean4.37 vsOL95 4.73; local seals and visible handoff recognition fixed. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.3c - Movement and route prediction

- **Objective:** Attribute-based kinematics.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.2 implementation validated
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Use acceleration/agility for movement and matching routeAhead predictions; preserve authored speed overrides where specified.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Source/dist and mirrored movement tests; no instant direction changes, no new aiming regression.
- **Evidence:** Source-position speed across fronts, shared acceleration/turn and routeAhead; browser hitch forecast vs live hold passes. Equal-summary pure contrasts all9positions. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.3d - Receiver release and route breaks

- **Objective:** Distinct release and route ability.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3c
- **Status:** in-progress
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Separate release vs press from routes vs coverage/agility; use observed leverage, assignment and bounded noise; remove duplicate OVR terms.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Seeded mirrored release/break curves meet spec; archetype differences remain meaningful.
- **Evidence:** Canonical release/press and route/coverage; pure3x100k gap curves pass. Go-ball whole-profile fixture corrected to install roster attrs before setup/scouting; final calibration ongoing. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.3e - Throwing and catching

- **Objective:** Distinct QB and receiver/DB skills.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3d
- **Status:** in-progress
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Use accuracy, arm, pressure handling and mobility with actual movement/weather; catch/contested catch vs coverage/ball skills and actual separation; remove OVR double-counting.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Spatial passing measures accuracy, pressure, sacks, YPA, drops, picks, contested catches and deep outcomes; no hidden target cheating.
- **Evidence:** Canonical throw/catch skills active. Final regression investigation identified catch-point reach/initial-separation double bonus; radial geometry fix independently reviewed, full600/profile test underway. Prior real go63% vs40-46 target, no final pass claimed. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.3f - Tackles and security

- **Objective:** Contact, pursuit and possession integrity.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3b, B-018/4.3c
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Use break tackle/strength/agility vs tackling/pursuit and contact geometry; preserve user moves. Implement bounded security/fumble path only with correct recovery, clock, possession, stats and heat.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Mirrored rush/contact tests and explicit turnover fixtures pass; retain nonzero upsets and no double-counted OVR.
- **Evidence:** Live lost/recovered fumble stats,clock,possession tests pass source/dist;10000 CPU goal-line spot fixtures. EqualOVR80 power/elusive/speed break739/2539,347/2147,234/2034 contacts; meanYAC.84/.47/.32yd. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.4a - Observation boundary

- **Objective:** Fair pre-snap and live AI.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3a–f
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Separate public coordinator inputs and currently observed player cues from hidden play ID, future routes and throw intent; use completed plays only for labels.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Same visible state and seed with different hidden plays yields same pre-snap decision; no reaction before cue.
- **Evidence:** No current hidden card/name/personnel in decisions. Actual identical HEAVY/ACE/SPREAD lineups allreadbase/.50. Whitelisted delayed kinematics; source/dist fairness checks. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.4b - Individual IQ and AWR

- **Objective:** Learning and immediate recognition separately.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.4a
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Implement bounded, decaying per-defender/context memory, IQ-based choice/learning and single AWR reaction timers; log actual cues/responses. Follow position effects in spec including QB/RB human control.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** IQ/AWR isolation experiments show distinct effects; no speed or physical ability boost; no teleportation or illegal help.
- **Evidence:** IQ60/75/95 adjust after11/5/3 supplied deep catches, reverse5/8/8quiet plays. 1000 cue phases/AWR mean.412/.305/.156sec withno pre-cue response; independent ReviewerB evidence. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.4c - Position adaptation and counters

- **Objective:** Make football intelligence position-specific.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.4b
- **Status:** in-progress
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Apply legal QB/RB/WR/TE/OL/DL/LB/CB/S decisions from spec, assignment-preserving cushion/leverage and single-help budget. Ensure decay and tactical costs.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Counter tests show short/opposite-side/PA opportunities and strategy reversal; no automatic human target, audible or movement override.
- **Evidence:** All position cognition consumers implemented. 1000 matched fed-history/cell: short892->969 catches,4.83->5.58yd; deep442->217,17.80->8.20. Remaining opposite-seam/safety-shade and individualPA acceptance cells. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.5a - Starting-unit summaries

- **Objective:** OL-inclusive team ratings.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3a–f
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Use specified offense/defense weights and eligible starting depth chart; distinguish display summaries from runtime ability.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** OL strength changes offense summary; ratings and cards reflect actual packages; no extra speed/OVR multiplier.
- **Evidence:** Specified OL-inclusive weighted units; source positions/depth charts preserved; tests prove displayOVR hasno CPU effect. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.5b - CPU matchup contract

- **Objective:** Matchup-driven simulated possessions.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.5a, B-018/4.4c
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Implement versioned CPU matchup inputs, personnel-aware concept choice, neutral defaults and remove str talent scalar after migration. Separate difficulty planning/assistance from physical ability.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Pure CPU sims show separate skill effects; difficulty never rewrites roster physical ability/IQ/AWR; game flow and possession remain valid.
- **Evidence:** Version1 attribute contract and personnel run/pass choice; str/difficulty physical scaling removed. Seed1 100k drives/level2.11-2.12pts/drive. Supporting cognition contract inputs partly reserved. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.5c - Full-game calibration

- **Objective:** Realistic emergent competitive win rates.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.5b
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Create production-equivalent kickoff/OT mirrored simulations and tune mechanics across talent centers and gaps, separate difficulty/weather/clutch/heat.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Use full-game bands 45–55/60–70/75–85/85–95/90–98% at gaps 0/5/10/15/20, with uncertainty and raw counts. No win-probability lookup, scripted comeback or rubber banding.
- **Evidence:** 180000 mirrored CPU kickoff/OT games:12000/gap at centers60/75/85, all bands. Gap0/5/10/15/20 winshares50.0-50.8/67.9-69.0/81.8-83.5/91.8-93.0/97.0-97.1%; clustered95%CI/raw counts in report. Uneven real rosters pending; not human odds. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.6a - Attribute editing and cards

- **Objective:** Readable, editable position attributes.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.2 implementation validated, B-018/4.5a
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Finish full attribute editor; preserve stable IDs, OVR vs derived summary, provisional/hybrid labels, strengths/weaknesses, imports and reset. Verify any new imported fields in menus.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Browser edit/save/reload/swap/reset fixtures and small landscape/portrait views; no data loss or misleading labels.
- **Evidence:** Identity-bound all-attribute editors, cached reset/clutch fixes;18 groups before final catch fixture, source/dist real UI saves/reload/swaps/reset and3mobile viewports pass. Physical iPhone unplaytested. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.6b - Coaching captions

- **Objective:** Explain meaningful adjustments without hidden odds.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.4c
- **Status:** validated
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Use existing coachfx/captions for material cushion, shading and other legal changes; keep HUD clear and avoid cinematics.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Caption reflects observed behavior; no new hidden information or blocked controls.
- **Evidence:** Existing caption/creep/shade layer communicates bounded positioning; no new cinematics/HUD layer. Phone visual checks still open. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.7a - Seeded acceptance matrix

- **Objective:** Validate full Phase 4 mechanics.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3a–f, B-018/4.4a–c, B-018/4.5a–c, B-018/4.6a–b
- **Status:** in-progress
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Execute every experiment in the 4.7 specification, including pure 100k reps/cell, spatial passing/rushing, IQ/AWR, same-OVR profiles, counters, full games, compatibility and live exhibition. Fix biased go-ball lab setup; reset RNGs and pair seeds.
- **Toolbox:** Gridline `skills/gridline-validation/SKILL.md`; private publication procedure in AGENTS.md and reports; Chrome/Playwright, Git, Node.
- **Acceptance criteria:** Required samples, raw denominators, uncertainty and before/after report; no omitted/hung reps, no new unrecorded regressions. Resolve failures or record explicit blockers; do not claim a pass without evidence.
- **Evidence:** Substantial seeded matrix recorded; final catch calibration underway. Missing full two-context spatial archetypes/position, opposite-seam/PA individual counters, uneven-roster games, phone performance. No targets weakened. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.7b - Build, review and private release

- **Objective:** Deliver tested build and physical playtest package.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.7a
- **Status:** blocked
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Review changed code for regressions and exploits; run required build and checks, push and verify remote commit and CI. Coordinate authorized private Claude artifact/site sync from disk; verify exact commit. Do not publish real nicknames publicly.
- **Toolbox:** Gridline `skills/gridline-validation/SKILL.md`; private publication procedure in AGENTS.md and reports; Chrome/Playwright, Git, Node.
- **Acceptance criteria:** Test evidence and commit recorded; private artifact confirmed or task stays validated/blocked; phone checklist and signoff recorded separately. No next core phase before required signoff.
- **Evidence:** 341f48e,cba3941 pushed andCIgreen. Private publication/Site sync andphysical iPhone signoff unverified. Repo madePRIVATE with Seph explicit approval before gameplay push. Legacy claim remainsactive until final handoff; no central claim. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

### B-024 - Advanced offensive playbooks

- Objective: full play selection, selectable styles and formation-based calls without losing quick suggestions.
- Approval: 2026-11-26 in [B-024 board entry](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); commit 90bffd7 adds roadmap only, not implementation.
- Dependencies: B-018 phase gate. Before or alongside playable defense, before new modes.
- Phase gate: every selectable play executes correctly and passes balance, fairness and mobile checks.

#### B-024/a1 - Formation and concept data

- **Objective:** Independent stable formation/personnel and play/concept IDs.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-018 gate
- **Status:** pending
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Audit existing paired cards, define reusable IDs and backward-compatible data. Expose only supported formations; implement actual alignments and assignments for any newly supported formation.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** No legacy call breaks; every formation has valid personnel and assignments.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/a2 - Selectable offensive styles

- **Objective:** Balanced, run-heavy, pass-heavy and spread/mobile QB playbooks.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/a1
- **Status:** pending
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Define selectable offensive books from supported formations/concepts; ensure styles reflect actual personnel and choices.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** Style selection changes available calls coherently; no fictitious formation or cosmetic-only difference.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/b1 - Suggested play calling

- **Objective:** Situation/personnel-aware suggestions.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/a2
- **Status:** pending
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Keep quick calls; use down/distance, field position, score/clock, strengths and completed-play tendencies, never hidden opponent calls.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** Same visible situation with hidden defense differences yields same suggestions; full book never restricted.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/b2 - Full playbook browsing

- **Objective:** Landscape-friendly formations/concepts view.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/a2, B-024/b1
- **Status:** pending
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Build Suggested Plays and Formations views, explicit selection and accurate route/block diagrams. Preserve quick play and existing controls.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** Browser shows all supported calls by formation/concept; no overlap; diagram matches actual execution.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/c1 - Concepts and audibles

- **Objective:** Expand actual scheme variety.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/b2
- **Status:** pending
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Expand supported run/pass/PA/screen concepts with real assignments and tactical purpose; implement formation-appropriate audibles without changing personnel magically.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** Every selectable play executes legally; counter value and audible behavior verified.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/c2 - Playbook validation

- **Objective:** Balance and fairness against Phase 4.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/c1
- **Status:** pending
- **Claim:** none (legacy phase claim must be reconciled before activation)
- **Instructions:** Test every call, mobile navigation, existing quick play, AI fairness and Phase 4 regression targets. Build, push and verify private release according to AGENTS.md.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** All supported calls validated; relevant sims, browser checks and release evidence recorded.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

### B-014 - Phase 5: Playable defense (blocked design gate)

- Objective: offense-only, defense-only and both sides with simulated possessions.
- Approval: direction agreed 2026-11-26; implementation explicitly requires review of [defense draft](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-playable-defense.md).
- Dependencies: B-018 and B-024; design approval.
- Phase gate: user approves controls, drive participation and quarter lengths; then Duet creates detailed tasks from the existing draft. No implementation until approved. Dream Board B-014 tracks questions.

### B-019 - Phase 6: Presentation and polish (blocked by Phase 5)

- Objective: approved roadmap direction for comic-book presentation, smooth animations, short/skippable cinematics, mobile usability and performance.
- Approval: 2026-11-26 roadmap; detailed scope remains to be refined where needed.
- Dependencies: B-014 completion and core balance.
- Phase gate: complete exhibition testing and user playtest; device-specific B-015 and screen priorities B-016 require clarification. Duet will expand approved work at the proper time, not guess feature requirements. B-017d hot kick effect requires a visible kicker.

## Later ideas

Season B-013, player/roster simulation B-020, Dynasty B-021, Coach Career B-022 and Player Career B-023 are roadmap direction pending design review and earlier phase completion. They remain in the project Dream Board, not executable tasks. Do not implement until promoted.

## Run handoffs

- 2026-11-26 migration preparation: legacy snapshot b92883f; no game changes, no new tests or publication claimed. Existing B-018 4.3–4.7 claim remains unresolved. 4.1 complete, 4.2 implementation validated; B-024 planned. Activate only after verified cutover. The detailed breakdown is a decomposition of approved specifications, not new feature approval.

- 2026-11-27 Codex reconciliation: Gridline PR2 merged. PM PR14/15 open; Activation remains pending. Continued original B-018/4.3-4.7 legacy claim, no new central claim. Source341f48e/cba3941 and CI verified, report c3c559c records measurements. Final go-ball repair remains in that existing claim. Release/reconcile the legacy claim before activation; do not begin a competing run.
