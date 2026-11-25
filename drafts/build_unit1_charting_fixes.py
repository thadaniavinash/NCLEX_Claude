"""NURS 1021 Unit 1: professional charting (user request, 25 Nov 2026).

- No client names: "the client" (and "the newborn" / family members by role) everywhere.
- Nurses' Notes in complete, professional sentences without abbreviations such as H/O, VS, RA.
- Long admission entries split into a Health History tab and a Physical Assessment tab.

Case Studies 2-10 were rewritten in their generators (build_1021_unit1_case<n>_*.py); this script rebuilds the chart
of Case Study 1 (DVT/PE) and University of Maryland CS10 (DVT) from the database copy, and writes one workflow patch
(drafts/unit1_charting_patch.json) that replaces the `screens` of all 11 Unit 1 case studies. The patch refuses to
apply if any item changed in the database after this script read cases-data.js.
Run after `download`: python3 drafts/build_unit1_charting_fixes.py
"""
import copy, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
sys.path.insert(0, HERE)
import bank
from unit6_common import note_rows
from nurs1021_common import sec

cases, _ = bank.load()
by_id = {c["id"]: c for c in cases}


def row(label, text):
    return note_rows([(label, text)])


def title(text):
    return f"<div><b>{text}</b></div>"


# ------------------------------------------------------------------ Case Study 1 (DVT progressing to PE)
C1 = by_id["case_1786010000001"]
c1_notes = [
    row("0825", "The client was brought to the emergency department by a partner, reporting a painful right lower leg "
        "that is red, warm and swollen. The client is unable to walk without leg pain. The health history and physical "
        "assessment were completed."),
    row("1010", "STAT blood work was drawn and sent to the laboratory. The right leg was elevated on two pillows."),
    row("1055", "Ultrasound confirmed a deep vein thrombosis (DVT) in the right lower leg. A heparin 5,880-unit IV bolus "
        "was given, and a continuous IV heparin infusion was started in the left forearm at 1,323 units/h per protocol. "
        "The client is being prepared for transfer to the medical unit."),
    title("Medical Unit") + row("1152", "The client was admitted to the medical unit with a continuous heparin infusion "
        "at 1,323 units/h for a right leg DVT. The client is alert and oriented. Vital signs: T 36.7° C (98° F), HR 82 "
        "beats/min, RR 16 breaths/min, BP 164/90 mm Hg, SpO<sub>2</sub> 97% on room air."),
    title("Day 2") + row("0700", "The nurse began the initial shift assessment. The client reports chest discomfort that "
        "started about 1 hour ago, with mild shortness of breath, and states feeling very anxious. Vital signs: "
        "T 36.7° C (98° F), HR 102 beats/min, RR 20 breaths/min, BP 98/62 mm Hg, SpO<sub>2</sub> 90% on room air."),
    title("Day 4") + row("0645", "Oxygen therapy was discontinued last evening. Vital signs: T 36.9° C (98.4° F), HR 80 "
        "beats/min, RR 18 breaths/min, BP 124/76 mm Hg, SpO<sub>2</sub> 95% on room air. Lung sounds are clear in all "
        "fields, with no adventitious sounds. S1 and S2 are present. Bowel sounds are present in all quadrants. The "
        "client reports occasional shortness of breath but no chest discomfort and states still feeling very anxious. "
        "The heparin infusion is running at 1,323 units/h in the left forearm per protocol. The morning stool is negative "
        "for occult blood, and there is no bleeding or bruising. The client is to start enoxaparin this afternoon after "
        "blood work."),
]
c1_hx = "".join([
    sec("Reason for visit", "Painful, red, warm and swollen right lower leg; the client is unable to walk without leg "
        "pain."),
    sec("Recent surgery", "Colon resection for stage 2 colorectal cancer; discharged from hospital 2 weeks ago."),
    sec("Medical history", "Type 2 diabetes mellitus, now controlled by diet and exercise after a recent weight loss of "
        "31.7 kg (70 lb); DVT 10 years ago after a total knee arthroplasty; hypercholesterolemia treated with lovastatin."),
    sec("Weight", "73.5 kg (162 lb).")])
c1_pa = "".join([
    sec("Neurological", "The client is alert and oriented × 3."),
    sec("Peripheral vascular", "The right lower leg is red, warm and swollen. Pedal pulses are 1+ in both feet, and both "
        "feet are cool."),
    sec("Abdomen", "The abdominal incision is approximated and healing, with no redness or drainage."),
    sec("Vital signs", "T 36.7° C (98° F), HR 80 beats/min, RR 18 breaths/min, BP 178/92 mm Hg, SpO<sub>2</sub> 96% on "
        "room air. Blood glucose 6.54 mmol/L (118 mg/dL).")])
c1_counts = [2, 2, 3, 4, 5, 6]   # notes entries shown on each screen (carry forward, never removed)
c1_screens = copy.deepcopy(C1["screens"])
for i, sc in enumerate(c1_screens):
    tabs = sc["leftContent"]["tabs"]
    assert [t["id"] for t in tabs] == ["nn_dvt_pe"], tabs
    tabs[0]["content"] = "".join(c1_notes[:c1_counts[i]])
    tabs.extend([{"id": "hx_dvt_pe", "title": "Health History", "content": c1_hx},
                 {"id": "pa_dvt_pe", "title": "Physical Assessment", "content": c1_pa}])
OLD_PRE = "The nurse reviews the 0825 nurses’ notes for a 71-year-old client who was admitted to the ED."
NEW_PRE = ("The nurse reviews the Nurses' Notes from 0825, the Health History and the Physical Assessment for a "
           "71-year-old client admitted to the emergency department.")
LABELS = {"SpO2 96% on RA": "SpO₂ 96% on room air", "H/O type 2 diabetes mellitus": "History of type 2 diabetes mellitus",
          "SpO2 90% on RA → SpO2 95% on RA": "SpO₂ 90% on room air → SpO₂ 95% on room air"}
for sc in c1_screens:
    q = sc["question"]
    for o in q.get("options") or []:
        o["text"] = LABELS.get(o["text"], o["text"])
    for r in (q.get("matrix") or {}).get("rows", []):
        r["text"] = LABELS.get(r["text"], r["text"])
for sc in c1_screens[:2]:
    assert sc["question"]["preamble"] == OLD_PRE, sc["question"]["preamble"]
    sc["question"]["preamble"] = NEW_PRE

# ------------------------------------------------------------------ University of Maryland CS10 (DVT, heparin)
U10 = by_id["case_1790776800010"]
u10_notes = [
    row("Day 1 0930", "<b>Admission note:</b> The client was admitted from the emergency department by stretcher and "
        "transferred to bed. The physical assessment was completed. The client was informed of the prescribed complete "
        "bed rest."),
    row("Day 1 1010", "Radiology reported the results of the right leg ultrasound: deep vein thrombosis of the right "
        "posterior tibial vein. The provider was notified, and new orders are pending."),
    row("Day 1 1018", "The orders have been entered."),
]
u10_pa = "".join([
    sec("Neurological", "The client is alert and oriented."),
    sec("IV access", "A saline lock in the right antecubital vein is patent."),
    sec("Right lower extremity", "2+ pedal edema is present. The client rates pain in the right calf at 8/10. Warmth is "
        "noted in the right calf. Motion and sensation are intact. The right pedal pulse is 2+ and palpable. The right "
        "leg is elevated on 2 pillows."),
    sec("Weight", "80 kg (176 lb)."),
    sec("Vital signs", "BP 145/82 mm Hg, HR 96 beats/min, RR 16 breaths/min, T 36.7° C (98° F).")])
u10_progress = row("Day 3 1015", "The client was cleared for discharge home. Heparin was discontinued as ordered, and "
    "warfarin was started. Discharge instructions were provided on warfarin therapy, prevention of deep vein thrombosis "
    "and risk reduction (health and weight management). The client was able to describe self-management from the "
    "discharge teaching, and clarification was provided as needed. The client is to follow up in 1 week. The client "
    "was discharged by wheelchair with all belongings.")
u10_counts = [1, 1, 1, 2, 3, 3]
u10_screens = copy.deepcopy(U10["screens"])
for i, sc in enumerate(u10_screens):
    tabs = sc["leftContent"]["tabs"]
    assert tabs[0]["id"] == "nn_umd10"
    tabs[0]["content"] = "".join(u10_notes[:u10_counts[i]])
    tabs.insert(1, {"id": "pa_umd10", "title": "Physical Assessment", "content": u10_pa})
    for t in tabs:
        if t["id"] == "pn_umd10":
            t["content"] = u10_progress
        if t["id"] == "ord_umd10":
            t["content"] = t["content"].replace("Activity: bedrest until", "Activity: bed rest until")

# ------------------------------------------------------------------ patch
patch = [{"row": "cases", "id": C1["id"], "path": ["screens"], "before": C1["screens"], "after": c1_screens},
         {"row": "cases", "id": U10["id"], "path": ["screens"], "before": U10["screens"], "after": u10_screens}]
for f in sorted(glob.glob(os.path.join(HERE, "case_17860100000[0-9]*_NURS_1021_Unit_1_Case_Study_*.json"))):
    new = json.load(open(f))
    if new["id"] == C1["id"]:
        continue
    old = by_id[new["id"]]
    for key in ("screens", "description"):
        if old[key] != new[key]:
            patch.append({"row": "cases", "id": new["id"], "path": [key], "before": old[key], "after": new[key]})
out = os.path.join(HERE, "unit1_charting_patch.json")
with open(out, "w") as fh:
    json.dump(patch, fh, ensure_ascii=False, indent=1)
# Copies of the two rebuilt items for checking in the app (set PREVIEW_DIR; not written to the repo)
if os.environ.get("PREVIEW_DIR"):
    for item, screens in ((C1, c1_screens), (U10, u10_screens)):
        with open(os.path.join(os.environ["PREVIEW_DIR"], f"{item['id']}.json"), "w") as fh:
            json.dump(dict(item, screens=screens), fh, ensure_ascii=False)
print(f"wrote {out}: {len(patch)} entries for", sorted({e['id'] for e in patch}))
