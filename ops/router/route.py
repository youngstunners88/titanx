"""Routing. Rules first (free, auditable), typed LLM decision second, human review last."""
import json, re
from pathlib import Path
from ops.lib import llm, state

RULES = json.loads((Path(__file__).parent / "rules.json").read_text())


def _hits(text, words):
    """(match count, matched characters). Longer, more specific phrases win ties."""
    t = text.lower()
    m = [w for w in words if re.search(r"(?<![a-z])" + re.escape(w) + r"(?:s|es)?(?![a-z])", t)]
    return len(m), sum(len(w) for w in m)


def route(text, live=False):
    scored = sorted(((_hits(text, r["any"]), r) for r in RULES["rules"]), key=lambda x: x[0], reverse=True)
    (top, top_chars), rule = scored[0]
    second = scored[1][0]
    if top >= RULES["min_hits"] and (top, top_chars) > second:
        out = {"route": rule["id"], "skill": rule["skill"], "workflow": rule["workflow"], "tier": rule["tier"],
               "stakes": rule["stakes"], "via": "rules", "hits": top}
    elif live:
        crit = {r["id"]: ", ".join(r["any"][:6]) for r in RULES["rules"]}
        crit["other"] = "None of the above"
        d = llm.decide({"request": text}, {"route": {"type": "choice", "instructions": "Which area does the `request` belong to?", "criteria": crit}}, live=True)
        dec = d["decisions"]["route"]
        rid = dec.get("value")
        if dec["status"] == "selected" and rid in {r["id"] for r in RULES["rules"]}:
            r = next(x for x in RULES["rules"] if x["id"] == rid)
            out = {"route": rid, "skill": r["skill"], "workflow": r["workflow"], "tier": r["tier"], "stakes": r["stakes"], "via": "llm", "probability": dec["probability"]}
        else:
            out = {"route": "review", "via": "review", "reason": "ambiguous after LLM"}
    else:
        out = {"route": "review", "via": "review", "reason": "no unique rule match (use --live for an LLM decision)"}
    state.append_event("routed", request=text[:120], **{k: v for k, v in out.items() if k != "hits"})
    return out
