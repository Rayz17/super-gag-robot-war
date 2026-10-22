# C01E02 Runtime / Graybox Deterministic Paper Run r2

> Seat: orchestration-side executable contract verification  
> Scope: current `C01E02-runtime-contract-v1.tsv`, `C01E02-graybox-constants-v1.tsv`, Episode and downstream input contracts  
> Verdict: `PASS_FOR_ORIGINAL_SEAT_RECHECK`  
> This is not a creative-seat acceptance and does not replace the independent gameplay or Canon verdict.

## 1. Why r2 Exists

The original gameplay review found that the readable story could not yet be replayed as one deterministic map: bridge deployment looked like a false order choice, Diedie teleported out during R4, F2 entry and five-person egress were undeclared, R5 appeared to bank an old support point, tool contacts had no complete body state, and the success snapshot could be written in two steps.

r2 verifies the patched contract rather than reusing the earlier r1 conclusion.

## 2. Static Contract Checks

- Runtime TSV: `9` columns on every row; IDs unique.
- Graybox TSV: `4` columns on every row; IDs unique.
- Grid: `12x14`, eight-neighbor movement, no diagonal corner cutting.
- Fire Bridge: fixed body and four fixed leg cells for all five rounds. SEG yaw may change inside the rig envelope; no leg changes cells.
- Bridge deployment: one previewed legal sequence, `SEG1 -> SEG2 -> SEG3`; no equivalent-order fake choice.
- Persistent write: only `RT038`, after `BAIHAN_REMOTE_PRESET_COMPLETE`; `RT039` is read-only assertion.

## 3. Population And Route Replay

Initial people are exactly `A11 + B10 + C3 + D5 = 29`, plus Jicun, Tangjiao and Doudeng. D5 contains the same repair worker already counted in E01. Robot Dog shares C3 after the R1 harness and never becomes another person. Diedie is equipment, not a human token.

| Round receipt | A11 | B10 | C3 + Dog | D5 | Diedie |
|---|---|---|---|---|---|
| R1 | `(8,5)` | `(9,5)` | `(7,6)` | `(9,6)` | `(10,10)` clutch prepared |
| R2 | `(7,7)` | `(7,8)` | `(5,6)` | `(9,8)` | `(10,10)` latch reset |
| R3 | `(4,7)` | `(4,8)` | `(3,6)` | `(5,8)` | `(10,10)` clutch locked |
| R4 | `(1,5)` | `(1,6)` | `(1,7)` | `(1,8)` | `(9,9)` protected pump recess |

Every route edge is adjacent, every listed endpoint equals the sum of declared per-round steps, and synchronous priority `C3 > B10 > D5 > A11` produces the same receipts without an illegal settled-cell collision. The side strip only permits the declared transient queue of at most two tokens.

## 4. R2 Choice And R3 Closure

| R2 choice | Immediate gain | Immediate cost | R3 matching action | End of R3 |
|---|---|---|---|---|
| `WATER_CURTAIN` | D5 remains at smoke `1` | Needle contacts SEG3 interface | interface flush | Needle recoiled; D5 safe |
| `PREEMPTIVE_INTERFACE_FLUSH` | Needle recoils before contact | D5 reaches smoke `2` | delayed water curtain | Needle safe; D5 safe |

Both routes spend exactly one R2 point and one R3 point. They converge on tool safety and a manual-low B1 pump without changing the representative route scar. A D5 route gate failure leaves it at `(9,8)` and can raise smoke to `3`, so the failure state is reachable rather than decorative.

Ruler contact is resolved in the R2 enemy phase: body at `(11,11)`, arm at `(11,10)`, physical contact with Tangjiao's angled barrier, then recoil to body `(11,12)` with arm retracted. Needle contact/recoil likewise carries body, arm and endpoint state; neither tool has HP or personality.

## 5. Phase Guards And Failure Behavior

- R1 blocks auto movement if C3 harness, all three bridge segments or population guard is missing.
- R2 requires two-sided manual door release, latch reset, Ruler deflection and one recorded fire-support choice.
- R3 requires mechanical clutch lock before Doudeng's low-voltage bypass, manual-low pump state, tool safety and smoke below `3`.
- R4 requires four exact endpoints, C3 intact, D5 population intact, pump manual-low and exactly one scar: `FIRE_SUPPLY_BURNED`.
- Any R1-R4 failure restarts from SRPG setup with zero persistent people, scar, map, permission or relationship write.

`END_PHASE` remains available. Missing gates stop the affected token or equipment, the environment still resolves, and the local guard then produces the declared failure instead of allowing a route to pass through missing geometry.

## 6. R5 Checkpoint And Egress

After R4, all four people tokens are hidden outside and the R1-R4 fire pool is zero. Jicun cancels automatic site clear; this keeps the public channel open but does not preserve a point. F2 then enters along two declared zero-AP routes:

- F2A: `(1,7) -> (2,7) -> (3,7)`
- F2B: `(1,8) -> (2,8) -> (3,8)`

Only after the two handoff adults enter does city fire issue one new emergency point for the new falling-beam incident. Reversing SEG3 blocks central cells `(7,7)` and `(8,7)` but leaves the service strip and y6 lane open. The declared paths for Jicun, Tangjiao, Doudeng, F2A and F2B all remain adjacent and reach the inside edge of the west door. Diedie remains in the protected `(9,9)` equipment recess and is not counted as a sixth human.

R5 failure returns to the local checkpoint. The 29 original evacuees remain hidden outside and no story state is committed.

## 7. Physical And Lifecycle Assertions

- Fire Bridge reverses SEG3 inside one fixed support rig. The left-front suspension compresses and its footpad slips inside cell `(3,10)`; it never moves to another grid cell.
- Brave Fist's request originates from the transport fall-arrest system and dies at the external license relay. Haosi is absent; body pressure and displacement remain zero.
- Guardian Z stays half-kneeling with main power and chest light off, right arm attached, and no body motion.
- Baihan has no cell, HP, hit or full body in E02. The final sound is its deployment lock beginning to open, not Brave Fist unlocking.
- E03 receives exactly `C01E02_PHYSICAL_SNAPSHOT`; S03 and S04 downstream contracts now explicitly forbid re-spawning the 29 people or turning people into cargo.

## 8. Machine Check Result

The deterministic checker reported:

```text
TSV_SHAPE PASS
ROUTES PASS
ROUND_RECEIPTS PASS
F2_ENTRY PASS
FIVE_PERSON_EGRESS PASS
ATOMIC_COMMIT PASS
ALL E02 RUNTIME/GRAYBOX CHECKS PASS
```

V35.8 strict also passes after adding the exact Guardian Z E02 animation override: `passive_temperature_sensor_and_low_voltage_relay_fx_no_body_motion`.

## 9. Verdict Boundary

The current contract is executable on paper and is ready for the original gameplay/production seat and Canon/macro/physical seat to recheck. Acceptance still requires both seats to return `PASS` against the patched source, followed by the full repository validation and one joint acceptance receipt.
