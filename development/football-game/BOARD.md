# Development Board: Gridline

## Project routing

- Project ID: football-game
- Target repository: Sgilmore186/gridline
- Target branch: main
- Push policy: verified direct pushes to main, explicitly authorized 2026-11-24 in Gridline AGENTS.md. No force pushes; private build only for private publication.
- Project rules: https://github.com/Sgilmore186/gridline/blob/main/AGENTS.md
- Dream Board: https://github.com/Sgilmore186/gridline/blob/main/docs/DREAM_BOARD.md
- Enrollment approval/source: Seph requested Gridline integration following shared workflow setup, 2026-11-26.
- Activation: active

## Cutover safety

This board was activated on 2026-11-27 after the verified cutover recorded below. The original Codex B-018/4.3-4.7 legacy claim is released in Gridline commit [59ab8fe](https://github.com/Sgilmore186/gridline/commit/59ab8fe0df1e50f6f0fb43edb32466f68d659a74), 2026-11-27. Run ID: codex-phase4-20261126-b92883f. Gameplay/save code is pushed through 7bf8ae3, with green CI and20 test groups. The [final report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md) records actual measurements, corrections and remaining limits. No active legacy or central claim remains. Do not rebuild validated tasks or begin another legacy run. Activation still requires the integration merges and routing checks below.

After both integration PRs are merged: fetch the latest Gridline main and PM main, confirm the legacy agent has stopped/released its claim, reconcile its commits, test results, publication and new board entries, and verify Gridline's AGENTS.md points here. Perform a read-only routing pass (active primary, correct repo, skills accessible, valid dependencies, no competing claim). Then change Activation to active and record the handoff in this board, using a normal non-force push under the reviewed enrollment. Only the cutover coordinator may activate after those checks; if uncertain, leave pending. Do not run both queues. For pending activation, the nightly trigger may perform read-only checks and report what is missing but must not modify game code.

## Run claim

- Owner: Codex
- Run ID: codex-phase4-final-20261127-1800
- Claimed/renewed UTC: 2026-11-27T18:17:00Z
- Starting target commit: 59ab8fe0df1e50f6f0fb43edb32466f68d659a74

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
- **Claim:** none (legacy claim released)
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
- **Claim:** none (legacy claim released)
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
- **Claim:** none (legacy claim released)
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
- **Claim:** none (legacy claim released)
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
- **Claim:** none (legacy claim released)
- **Instructions:** Use acceleration/agility for movement and matching routeAhead predictions; preserve authored speed overrides where specified.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Source/dist and mirrored movement tests; no instant direction changes, no new aiming regression.
- **Evidence:** Source-position speed across fronts, shared acceleration/turn and routeAhead; browser hitch forecast vs live hold passes. Equal-summary pure contrasts all9positions. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.3d - Receiver release and route breaks

- **Objective:** Distinct release and route ability.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3c
- **Status:** validated
- **Claim:** none (legacy claim released)
- **Instructions:** Separate release vs press from routes vs coverage/agility; use observed leverage, assignment and bounded noise; remove duplicate OVR terms.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Seeded mirrored release/break curves meet spec; archetype differences remain meaningful.
- **Evidence:** Canonical release/press and route/coverage,3x100k gap cells. Final whole-profile go fixture installed before setup; elite146/49329.6% and average86/48817.6% in-phase catches. Catch-point and initial-separation duplicate advantage fixed; field air yards separated from flightlength. Residual event-mix limits remain4.7. [Final report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.3e - Throwing and catching

- **Objective:** Distinct QB and receiver/DB skills.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3d
- **Status:** validated
- **Claim:** none (legacy claim released)
- **Instructions:** Use accuracy, arm, pressure handling and mobility with actual movement/weather; catch/contested catch vs coverage/ball skills and actual separation; remove OVR double-counting.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Spatial passing measures accuracy, pressure, sacks, YPA, drops, picks, contested catches and deep outcomes; no hidden target cheating.
- **Evidence:** Final1200 attempts/QB: elite794/1200,8.63YPA,40INT; weak476/1200,4.49YPA,89INT. Real362/600,9.44YPA,30INT. All selected outcomes and fumble yardage retained. Real go235/60039.2%, with point/rare-event misses recorded, not called a full balance pass. [Final report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.3f - Tackles and security

- **Objective:** Contact, pursuit and possession integrity.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3b, B-018/4.3c
- **Status:** validated
- **Claim:** none (legacy claim released)
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
- **Claim:** none (legacy claim released)
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
- **Claim:** none (legacy claim released)
- **Instructions:** Implement bounded, decaying per-defender/context memory, IQ-based choice/learning and single AWR reaction timers; log actual cues/responses. Follow position effects in spec including QB/RB human control.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** IQ/AWR isolation experiments show distinct effects; no speed or physical ability boost; no teleportation or illegal help.
- **Evidence:** IQ60/75/95 adjust after11/5/3 supplied deep catches, reverse5/8/8quiet plays. 1000 cue phases/AWR mean.412/.305/.156sec withno pre-cue response; independent ReviewerB evidence. Commits341f48e/cba3941; [development report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.4c - Position adaptation and counters

- **Objective:** Make football intelligence position-specific.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.4b
- **Status:** validated
- **Claim:** none (legacy claim released)
- **Instructions:** Apply legal QB/RB/WR/TE/OL/DL/LB/CB/S decisions from spec, assignment-preserving cushion/leverage and single-help budget. Ensure decay and tactical costs.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Counter tests show short/opposite-side/PA opportunities and strategy reversal; no automatic human target, audible or movement override.
- **Evidence:** 1000 matched short/deep cells: cushion makes short892->969 catches and4.83->5.58yd, deep442->217 and17.80->8.20. 1000 cold/learned shade cells: opposite helpdist26.10->29.56yd,<=4yd,singlebudget andquiet reversal pass;0/1000 Cover0 orbracket extrahelp. PA5concepts x1002/condition,10020 outcomes:42%/12.7YPA->47%/14.8, IQ/AWR75. Disguise/shade interaction fixed. [Final report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.5a - Starting-unit summaries

- **Objective:** OL-inclusive team ratings.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.3a–f
- **Status:** validated
- **Claim:** none (legacy claim released)
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
- **Claim:** none (legacy claim released)
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
- **Claim:** none (legacy claim released)
- **Instructions:** Create production-equivalent kickoff/OT mirrored simulations and tune mechanics across talent centers and gaps, separate difficulty/weather/clutch/heat.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Use full-game bands 45–55/60–70/75–85/85–95/90–98% at gaps 0/5/10/15/20, with uncertainty and raw counts. No win-probability lookup, scripted comeback or rubber banding.
- **Evidence:** 228000 mirrored CPU full games,3seed batches:180000 uniform across centers60/75/85 withclutch75, all provisional bands;48000 actual uneven-roster games. Gap0/5/10/15/20 uniform winshare ranges50.0-50.8/67.7-69.0/81.8-82.8/91.6-92.8/96.6-96.9%. Uneven SEA/SF54.1%,SF/MIA91.7%,SEA/TEN84.1%,SF/JAX64.8%; full clustered95%CI/raw counts inreport. CPU-only, nothuman odds. [Final report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.6a - Attribute editing and cards

- **Objective:** Readable, editable position attributes.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.2 implementation validated, B-018/4.5a
- **Status:** validated
- **Claim:** none (legacy claim released)
- **Instructions:** Finish full attribute editor; preserve stable IDs, OVR vs derived summary, provisional/hybrid labels, strengths/weaknesses, imports and reset. Verify any new imported fields in menus.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; relevant source paths and https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md
- **Acceptance criteria:** Browser edit/save/reload/swap/reset fixtures and small landscape/portrait views; no data loss or misleading labels.
- **Evidence:** 20 Node groups plus actual source/dist UI saves, swaps, reload/reset, canonical andlegacy clutch40->81->reset withpermanentID, and3mobile viewports pass. No data loss observed. Physical iPhone unplaytested. [Final report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.6b - Coaching captions

- **Objective:** Explain meaningful adjustments without hidden odds.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.4c
- **Status:** validated
- **Claim:** none (legacy claim released)
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
- **Claim:** Codex / codex-phase4-final-20261127-1800 / 2026-11-27T18:00:12Z / start 59ab8fe
- **Instructions:** Execute every experiment in the 4.7 specification, including pure 100k reps/cell, spatial passing/rushing, IQ/AWR, same-OVR profiles, counters, full games, compatibility and live exhibition. Fix biased go-ball lab setup; reset RNGs and pair seeds.
- **Toolbox:** Gridline `skills/gridline-validation/SKILL.md`; private publication procedure in AGENTS.md and reports; Chrome/Playwright, Git, Node.
- **Acceptance criteria:** Required samples, raw denominators, uncertainty and before/after report; no omitted/hung reps, no new unrecorded regressions. Resolve failures or record explicit blockers; do not claim a pass without evidence.
- **Evidence:** Extensive seeded matrix andindependent final review delivered; noCritical/High correctness findings. Remaining: rare-event point misses (real40+22/600=3.7%,20+98/600=16.3%,INT5%; go39.2%,drops/eventmix), full across-position spatial style coverage andphysical performance/feel. No test targets relaxed; loose tool flags tightened tospec. [Final report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

#### B-018/4.7b - Build, review and private release

- **Objective:** Deliver tested build and physical playtest package.
- **Approval:** 2026-11-26, B-018 in the [legacy board](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); scope in [Phase 4 specification](https://github.com/Sgilmore186/gridline/blob/main/docs/spec-phase4-ratings.md).
- **Dependencies:** B-018/4.7a
- **Status:** blocked
- **Claim:** Codex / codex-phase4-final-20261127-1800 / 2026-11-27T18:00:12Z / start 59ab8fe
- **Instructions:** Review changed code for regressions and exploits; run required build and checks, push and verify remote commit and CI. Coordinate authorized private Claude artifact/site sync from disk; verify exact commit. Do not publish real nicknames publicly.
- **Toolbox:** Gridline `skills/gridline-validation/SKILL.md`; private publication procedure in AGENTS.md and reports; Chrome/Playwright, Git, Node.
- **Acceptance criteria:** Test evidence and commit recorded; private artifact confirmed or task stays validated/blocked; phone checklist and signoff recorded separately. No next core phase before required signoff.
- **Evidence:** Final gameplay/save7bf8ae3 andhandoff59ab8fe pushed; CIgreen20groups, rebuilt exactdistSHA08fa27a8893ef7ef2c2da6bbca47863fd7a2803b0be2b5ce95cde5da2617cf80. GitHubPRIVATE verified afterSeph approval. A final combined+targeted independent reviews foundnoCritical/High; B/C earlier evidence retained. Private artifact/Site sync andiPhone signoff unverified. Legacy claim released; no central claim. PM14/15 mergers androuting verification still required beforeactivation. [Final report](https://github.com/Sgilmore186/gridline/blob/main/docs/reports/2026-11-27.md).
- **Handoff:** Complete only missing work; record checks and commit.

### B-025 - Pre-season gameplay foundations

- Objective: fix route execution, passing physics and extended-play behavior before new playbooks or season mode.
- Approval: 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- Dependencies: B-018 phase gate, including private publication and physical user signoff. Do not interrupt its current run or relax its acceptance targets.
- Phase gate: all B-025 tasks validated, required build, tests, seeded regressions, private delivery and physical review recorded. Do not start B-024 until this gate passes.
- Boundaries: preserve canonical attributes, saves, player IDs, existing fair defense, intentional receiver settles, press and stumbles. Existing passing has soft range and movement/pressure penalties; verify and extend instead of rebuilding. Numeric tuning is provisional, not fixed by the checklist. No season code.

#### B-025/r1 - Route audit and fixtures

- **Objective:** Reproduce corner/go stops, out geometry and slant/drag interference.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-018 gate
- **Status:** pending
- **Claim:** none
- **Instructions:** Capture route waypoints, movement, cut timing, LOS-relative coordinates and prediction vs actual trajectory across receivers, mirrored sides, field spots, frame rates and coverage. Isolate legitimate press, intentional settles and stumbles from defects. Record seeds and baseline.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, game/loop.js, game/passing.js, engine/duels.js, tools/sim_passing.py.
- **Acceptance criteria:** Reproduce each reported issue or document non-reproduction and conditions; retain deterministic fixtures and before data.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-025/r2 - Route geometry and continuous movement

- **Objective:** Make every called route predictable and correct.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-025/r1
- **Status:** pending
- **Claim:** none
- **Instructions:** Use shared geometry for diagram, live steering and throw prediction. Fix corner cut hesitation, premature go termination, incorrect out breaks, slants/drags crossing the OL at unintended depth. Define stem depth, cut angle and continuation; preserve designed curls/hitches/zone settles, screens/flats and legitimate football events. Mirror sides and handle boundaries; no teleporting.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, game/loop.js, game/passing.js, ui/playcall.js, tools/sim_passing.py.
- **Acceptance criteria:** Seeded trajectories verify go, corner, out, slant, drag, dig, post, curl and comeback; no unplanned stops; route predictor agrees with real catch-time movement; source/dist parity.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-025/r3 - Route ratings and separation

- **Objective:** Improve separation through skill rather than broken geometry.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-025/r2
- **Status:** pending
- **Claim:** none
- **Instructions:** Reuse position attributes and release/break duels; evaluate acceleration through cuts, speed retention, release and separation for same-speed/same-OVR players, press/off and weather. Do not double-count OVR or make weak receivers run the wrong route.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; engine/physical.js, engine/duels.js, data/attribute-schema.js, tools/sim_duels.mjs, tools/sim_phase4_spatial.py.
- **Acceptance criteria:** Paired fixtures isolate route skill, preserve correct geometry at low ratings, and show no unrecorded coverage, catch or explosive-play regression.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-025/p1 - Finite arm range

- **Objective:** Limit actual air distance by QB throw power.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-025/r2, B-025/r3
- **Status:** pending
- **Claim:** none
- **Instructions:** Audit existing soft range, ball velocity and lead projection. Cap true release-to-landing air distance under ideal and compromised conditions using canonical throw power; out-of-range throws land short with consistent trajectory and catch point. No lead, loft, UI or frame-step bypass. Tune values from seeded evidence, not illustrative 40–75 yard numbers.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/passing.js, engine/physical.js, tools/sim_qb_throws.py, tools/sim_go_balls.py.
- **Acceptance criteria:** Weak/average/elite QBs show monotonic finite range under identical conditions. All throw types stay within their cap; normal short/deep and boundary throws remain valid.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-025/p2 - Throwing conditions and accuracy

- **Objective:** Reward clean pockets and punish difficult body positions.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-025/p1
- **Status:** pending
- **Claim:** none
- **Instructions:** Audit distance-based accuracy and existing motion/pressure logic; extend canonical short/medium/deep accuracy, throw-on-run and pressure resistance. Account for planted feet, speed, retreat, cross-body direction, QB handedness (document compatible default; no guessed player data) and weather. Do not guarantee elite completions or double-count attributes.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/passing.js, game/stick.js, engine/physical.js, tools/sim_phase4_passing.py.
- **Acceptance criteria:** Paired fixed-seed tests show clean-pocket advantage, cross-body and retreat penalties, skilled QB mitigation and mirrored handedness behavior; finite range and Phase 4 targets checked.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-025/p3 - Throw away and grounding

- **Objective:** Give QB a legal alternative to forced throws or sacks.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-025/p2
- **Status:** pending
- **Claim:** none
- **Instructions:** Add dedicated mobile control without hijacking tap/hold/joystick. Apply game rules for tackle box, reaching LOS and eligible receiver vicinity; enforce intentional grounding spot/loss of down/safety as applicable. Route through normal ball, down, clock and stats resolution. Document control and rule abstraction; do not make all throwaways penalty-free.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; ui/input.js, ui/controls.js, render/hud.js, game/passing.js, game/plays.js, game/clock.js.
- **Acceptance criteria:** Browser tests cover legal outside-box throw past LOS, in-box no receiver, short-of-LOS outside box, eligible receiver nearby, post-LOS/repeated action, end zone and down/clock/stats; no input conflicts or exploits.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-025/s1 - Scramble drill

- **Objective:** Coordinate receivers instead of all running vertically.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-025/r3, B-025/p3
- **Status:** pending
- **Claim:** none
- **Instructions:** Activate on sustained extension after normal route development, not ordinary dropback, tiny stick movement or planned boot/run. Assign short/intermediate/deep outlets by route, QB rollout side, observable coverage and open space. Keep open receivers viable; near-side comeback, backside crossing, RB checkdown if not blocking. Avoid clustering, oscillation, boundary violations and omniscience; keep prediction aligned.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/loop.js, game/passing.js, engine/cognition.js, ui/badges.js.
- **Acceptance criteria:** Fixtures cover left/right extension, delayed trigger, distinct route depths, preserved open receiver, RB block responsibility, no all-vertical fallback and no off-field movement.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-025/s2 - Integrated foundation validation

- **Objective:** Prove route, QB and scramble changes coexist with existing gameplay.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-025/s1
- **Status:** pending
- **Claim:** none
- **Instructions:** Run matched seeded passing, route, sack, catch, coverage, full-game and explosive regressions against accepted Phase 4 baseline. Test controls, saves and source/dist parity. Build, push, verify CI and private publication; record physical review separately. Do not weaken targets or claim unperformed tests.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; node v2/build.mjs, node tests/check_scripts.mjs, node --test tests/player_attributes.test.mjs tests/phase4_gameplay.test.mjs, tests/check_phase4_browser.py, tools/sim_qb_throws.py, tools/sim_go_balls.py, tools/sim_explosive.py, tools/sim_full_game.py.
- **Acceptance criteria:** Repro cases pass; regression results and denominators recorded; remote commit and CI verified; private release and physical signoff confirmed or phase remains blocked.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

### B-024 - Advanced offensive playbooks

- Objective: full play selection, selectable styles and formation-based calls without losing quick suggestions.
- Approval: 2026-11-26 in [B-024 board entry](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md); commit 90bffd7 adds roadmap only, not implementation.
- Dependencies: B-018 and B-025 phase gates. Before playable defense and new modes.
- Scope refinement: 2026-11-27 pre-season checklist request; retain prior approval and task IDs.
- Phase gate: every selectable play executes correctly and passes balance, fairness and mobile checks.

#### B-024/a1 - Formation and concept data

- **Objective:** Independent stable formation/personnel and play/concept IDs.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-018 gate B-025 gate also required.
- **Status:** pending
- **Claim:** none (legacy claim released)
- **Instructions:** Audit existing paired cards, define reusable IDs and backward-compatible data. Expose only supported formations; implement actual alignments and assignments for any newly supported formation. Separate ordinary calls into fixed PASS or RUN with stable play IDs. Explicitly model RPO/option decisions and actual resolved outcomes; special teams are separate. Migrate paired cards, RUN IT! and RUN/PASS toggle with compatibility mapping. Ordinary pass may legally scramble, never become an arbitrary handoff. Share formation/personnel/concept/ballcarrier/type/assignment metadata across UI, game and CPU.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** No legacy call breaks; every formation has valid personnel and assignments. No ordinary call flips type at snap; old saves/debug fixtures have documented mapping; legal outcomes counted correctly.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/a2 - Selectable offensive styles

- **Objective:** Balanced, run-heavy, pass-heavy and spread/mobile QB playbooks.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/a1
- **Status:** pending
- **Claim:** none (legacy claim released)
- **Instructions:** Define selectable offensive books from supported formations/concepts; ensure styles reflect actual personnel and choices. Differentiate books by actual roster strengths. Candidate identities: Balanced, West Coast, Air Raid, Vertical, Power Run, Spread Option, Multiple. Final count/names are proposals; preserve existing approved styles and avoid cosmetic-only variants.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** Style selection changes available calls coherently; no fictitious formation or cosmetic-only difference. Mobile QB books offer genuine non-RB carries once implemented; pocket QB and power-run units have fitting call mixes; selected book persists and uses valid catalog.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/b1 - Suggested play calling

- **Objective:** Situation/personnel-aware suggestions.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/a2
- **Status:** pending
- **Claim:** none (legacy claim released)
- **Instructions:** Keep quick calls; use down/distance, field position, score/clock, strengths and completed-play tendencies, never hidden opponent calls. Present three distinct legal suggested plays where available; consider down/distance, field position, score/clock, personnel, visible tendencies and strengths. Graceful fallback for fewer than three.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** Same visible situation with hidden defense differences yields same suggestions; full book never restricted.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/b2 - Full playbook browsing

- **Objective:** Landscape-friendly formations/concepts view.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/a2, B-024/b1
- **Status:** pending
- **Claim:** none (legacy claim released)
- **Instructions:** Build Suggested Plays and Formations views, explicit selection and accurate route/block diagrams. Preserve quick play and existing controls. Three tabs: Suggested, Formation, Play Type. Types: Quick Game, Intermediate & Deep, RPO, Option, Run, Special Teams where appropriate. Screen and play-action are pass tags. Run has RB Runs and QB & WR Runs filter for actual QB power/draw/counter and jet sweep/end-around/reverse as supported. Hide unsupported calls; preserve mobile navigation and audibles.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** Browser shows all supported calls by formation/concept; no overlap; diagram matches actual execution. Three tabs, three suggestions where legal, accurate filters/diagrams, no overflow; QB/WR run filter shows real ballcarriers.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/c1 - Concepts and audibles

- **Objective:** Expand actual scheme variety.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/b2
- **Status:** pending
- **Claim:** none (legacy claim released)
- **Instructions:** Expand supported run/pass/PA/screen concepts with real assignments and tactical purpose; implement formation-appropriate audibles without changing personnel magically. Implement actual QB carries and jet sweeps, blocking, handoffs and motion; no relabeled RB handoffs. Ordinary audibles select separate compatible calls. RPO/option decisions wait for c1a approval.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** Every selectable play executes legally; counter value and audible behavior verified.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

#### B-024/c1a - RPO and option design gate

- **Objective:** Resolve controls and explicit decision mechanics.
- **Approval:** 2026-11-27: RPO and Option requested; exact decision controls unresolved.
- **Dependencies:** B-024/c1
- **Status:** blocked
- **Claim:** none
- **Instructions:** Propose mobile controls, read defender, decision window, defaults, give/keep/throw/pitch, blocking and illegal downfield handling, AI and diagrams. Present to Seph for approval; do not implement fake decisions or permit every ordinary call to switch.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/runs.js, game/plays.js, ui/input.js, game/playbook.js.
- **Acceptance criteria:** Explicit user approval of decision controls and rules recorded.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-024/c1b - Implement approved RPO and options

- **Objective:** Deliver genuine read-based plays.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-024/c1a
- **Status:** pending
- **Claim:** none
- **Instructions:** Implement only approved decision states; enforce one resolved ball outcome, legal blocking, stats and audibles. Expose only working concepts in Play Type. AI uses observed reads.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, game/runs.js, game/plays.js, game/passing.js, ui/input.js.
- **Acceptance criteria:** Test give/keep/throw/pitch where approved, expired decisions, no double possession/extra pass, correct stats and no hidden-state AI.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-024/c1c - Specialist personnel and CPU schemes

- **Objective:** Make player strengths and book selection affect actual CPU calls.
- **Approval:** 2026-11-27: Seph requested the pre-season gameplay checklist be added to PM with task instructions for automations; reported gameplay defects and requested playbook features. Unsettled design choices remain gated.
- **Dependencies:** B-024/a2, B-024/c1b
- **Status:** pending
- **Claim:** none
- **Instructions:** Use stable IDs and canonical attrs, eligible formation packages and no duplicate or magical substitutions. Make CPU and drive sim respect approved scheme tendencies; do not add unrelated advanced packages.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; data/player-store.js, game/plays.js, engine/coach.js, engine/cpusim.js, tools/sim_cpu_drives.mjs.
- **Acceptance criteria:** Paired situations show differentiated scheme calls, valid personnel, no hidden information and no CPU balance regression.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### B-024/c2 - Playbook validation

- **Objective:** Balance and fairness against Phase 4.
- **Approval:** 2026-11-26, [B-024 legacy backlog](https://github.com/Sgilmore186/gridline/blob/b92883f6280afce066ab100e3a882c7017ca4059/docs/BOARD.md).
- **Dependencies:** B-024/c1 B-024/c1b, B-024/c1c.
- **Status:** pending
- **Claim:** none (legacy claim released)
- **Instructions:** Test every call, mobile navigation, existing quick play, AI fairness and Phase 4 regression targets. Build, push and verify private release according to AGENTS.md. Enumerate every legal call across books and filters; verify real routes, blocks, carrier, classification, options, audibles, suggestions, AI fairness and mobile navigation. Compare multiple seeds to B-025 and Phase 4 baselines.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/playbook.js, ui/playcall.js, game-design.md and B-024 legacy specification.
- **Acceptance criteria:** All supported calls validated; relevant sims, browser checks and release evidence recorded.
- **Evidence:** None recorded in central board; inspect latest implementation before starting.
- **Handoff:** Complete only missing work; record checks and commit.

### PRE-OPTIONAL - Additional proposed gameplay improvements (design review)

- Objective: evaluate checklist proposals without silently authorizing new features.
- Dependencies: B-024 gate for integration.
- Phase gate: explicitly approve or defer each proposal before season readiness; verify existing functionality rather than rebuild. Blocked tasks are not unattended implementation authorization.

#### PRE-OPTIONAL/a - Pass leading and trajectories

- **Objective:** Evaluate existing lead prediction, touch/bullet; consider manual lead and separate lob.
- **Approval:** 2026-11-27 checklist: proposed additions, not finalized controls.
- **Dependencies:** B-024 gate
- **Status:** blocked
- **Claim:** none
- **Instructions:** Audit leadSpot/routeAhead, touch and hold bullet. Document existing behavior and any gaps. Propose gesture and trajectory design only if needed; obtain approval before new controls.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/passing.js, ui/input.js, tools/sim_passing.py.
- **Acceptance criteria:** Current behavior demonstrated; new manual lead/lob approved or deferred.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### PRE-OPTIONAL/b - Pocket and additional personnel

- **Objective:** Review pocket and packages after core work.
- **Approval:** 2026-11-27 checklist: proposed additions beyond existing work not finalized.
- **Dependencies:** B-024 gate
- **Status:** blocked
- **Claim:** none
- **Instructions:** Audit Phase 4 pass protection, pocket shape, assignments and B-024 personnel; document actual residual issues. Propose targeted changes, no wholesale rewrite.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; engine/physical.js, game/loop.js, game/plays.js, tools/sim_runs_and_sacks.py.
- **Acceptance criteria:** Existing behavior and gaps recorded; new mechanics approved or deferred.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

#### PRE-OPTIONAL/c - Play and route testing mode

- **Objective:** Decide if dedicated practice UI is needed.
- **Approval:** 2026-11-27 checklist: proposed practice mode not finalized.
- **Dependencies:** B-024 gate
- **Status:** blocked
- **Claim:** none
- **Instructions:** Audit Quick Drive/debug harness. Propose repeatable snap/reset, controlled field position/coverage and route inspection; don't expose release debug cheats or build new mode without approval.
- **Toolbox:** Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; game/exhibition.js, main.js, ui/menus.js, tests/check_phase4_browser.py.
- **Acceptance criteria:** Existing repeatable workflow documented; practice UI approved or deferred.
- **Evidence:** None recorded for this task; inspect latest implementation and Phase 4 evidence before starting.
- **Handoff:** Record commands, outcomes, remote commit and outstanding checks; do not repeat validated work.

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

### PRE-GATE - Season readiness review

- Objective: ensure gameplay is ready before season is promoted.
- Approval: 2026-11-27 checklist request; no season implementation authorization.
- Dependencies: B-018, B-025, B-024, B-014 and B-019 gates; PRE-OPTIONAL decisions approved/validated or deferred.
- Status: blocked until all required phases, decisions and physical review complete.
- Claim: none
- Instructions: Review all supported formations/routes, QB archetypes, range/accuracy, QB/WR runs, approved RPO/options, CPU decision-making, scheme balance, full exhibitions, mobile controls and saves. Run required build, tests and seeded regressions against accepted baselines. Record remote commit, CI, exact private publication and phone review. Ask Seph to approve B-013 season design separately; no season implementation yet.
- Toolbox: Gridline `skills/gameplay-engineering/SKILL.md`, `skills/gridline-validation/SKILL.md`; Phase 4 spec, game-design.md, browser tests, seeded sims and shared agent-execution skill.
- Acceptance criteria: all required gates passed with evidence; no unresolved critical gameplay regressions; optional decisions resolved and explicit season approval recorded.
- Evidence: none yet.
- Handoff: season remains a Dream Board design.

## Later ideas

Season B-013, player/roster simulation B-020, Dynasty B-021, Coach Career B-022 and Player Career B-023 are roadmap direction pending design review and earlier phase completion. They remain in the project Dream Board, not executable tasks. Do not implement until promoted. Season additionally requires PRE-GATE.

## Run handoffs

- 2026-11-26 migration preparation: legacy snapshot b92883f; no game changes, no new tests or publication claimed. Existing B-018 4.3–4.7 claim remains unresolved. 4.1 complete, 4.2 implementation validated; B-024 planned. Activate only after verified cutover. The detailed breakdown is a decomposition of approved specifications, not new feature approval.

- 2026-11-27 Codex reconciliation: Gridline PR2 merged. PM PR14/15 open; Activation remains pending. Continued original B-018/4.3-4.7 legacy claim, no new central claim. Source341f48e/cba3941 and CI verified, report c3c559c records measurements. Final go-ball repair remains in that existing claim. Release/reconcile the legacy claim before activation; do not begin a competing run.

- 2026-11-27 final handoff: legacy claim released in59ab8fe; code7bf8ae3;20-groupCI success. All measured evidence reconciled above. Initial go-ball regression was corrected; residual statistical targets, full spatial style coverage, private publication andphysical iPhone signoff remainopen. Registry milestone/nextstep updated throughpm.py. Activation remains pending whilePM14/15 areopen. No competing queue ornew claim; no B024/defense/cinematics/modes started. After required merges, fetch bothmain branches, verifyrelease androuting, then activateunder the reviewed enrollment.

- 2026-11-27 cutover coordinator: activated after fresh fetch of both main branches. Verified PM14 merged2224241, PM15 merged8ac5782, Gridline2 mergedb53a87a, active primary football-game, released legacy59ab8fe, no competing claims, valid dependencies, accessible canonical skills and AGENTS routing. Existing implementation/evidence retained; current user authorizes residual Phase4 only. Acquired single run codex-phase4-final-20261127-1800. Physical signoff remains required.

- 2026-11-27 run progress, codex-phase4-final-20261127-1800: committed5c5a793 harness evidence repairs and413371b spatial contact repairs. Independent reviewers reproduced/resolved unreachable dives, remote/duplicate catch tackles, downed catch contestants, assignment/backside blocking and acceptance-tool errors. New22-group tests and source/dist browser suite pass; AWR/possession/clutch unchanged. Rerunning fixed-seed, animation-reset passing and all9-position spatial matrix; rare-event/safety calibration is still under holdout testing. No statistical acceptance or publication claimed yet.

- 2026-11-27 planning proposal: added B-025 foundations, extended B-024, recorded optional design gates and PRE-GATE per Seph's pre-season checklist request. Preserved B-018 run claim, evidence and gates; no game code, tests, publication, registry or scheduler changes. Reconcile with latest main and coordinate with the active run holder before merge; never overwrite its claim or progress.
