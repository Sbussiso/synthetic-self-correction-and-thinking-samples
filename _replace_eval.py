import json

TO = chr(60) + "think" + chr(62)
TC = chr(60) + "/think" + chr(62)

def a(*blocks_and_final):
    *blocks, final = blocks_and_final
    parts = [TO + "\n" + b + "\n" + TC for b in blocks]
    return "\n\n".join(parts) + "\n\n" + final

# 9 novel replacement records (verified novel against training)

# idx 11: code/easy, 2 blocks, right_doubt_reaffirm (no system)
r11 = {"messages": [
    {"role": "user", "content": "Does `True or False` return True in Python?"},
    {"role": "assistant", "content": a(
        "Yes. Python's `or` returns the first truthy operand. Since True is truthy, `True or False` short-circuits and returns True.",
        "A doubt: `or` might return a computed boolean (True XOR False = True), but Python's `or` returns the actual operand value, not a boolean. Since True is the first operand and it's truthy, `True or anything` returns True. The doubt conflates Python's `or` (returns operand) with a strict boolean or.",
        "Yes, `True or False` returns True. Python's `or` short-circuits to the first truthy operand, and True is truthy.")}]}

# idx 12: code/medium, 3 blocks, wrong_then_fix (no system)
r12 = {"messages": [
    {"role": "user", "content": "What does `tuple([1, 2])` return in Python?"},
    {"role": "assistant", "content": a(
        "The `tuple()` function checks if something is a tuple, so `tuple([1, 2])` returns False because [1, 2] is a list.",
        "No -- `tuple()` is a constructor, not a type check. It converts an iterable to a tuple by iterating over its elements. `tuple([1, 2])` builds a tuple from the list's elements.",
        "So `tuple([1, 2])` returns `(1, 2)`. Verify: `type(tuple([1, 2]))` is `tuple`, `tuple([1, 2]) == (1, 2)` is True, and `len(tuple([1, 2]))` is 2.",
        "(1, 2). `tuple()` converts the list to a tuple, confirmed by `type()`, key equality, and `len()`.")]}}
# idx 15: code/hard, 5 blocks, wrong_then_fix (no system)
r15 = {"messages": [
    {"role": "user", "content": "What does `type('X', (), {'n': 5})()` produce?"},
    {"role": "assistant", "content": a(
        "This creates a class named X with no bases and an attribute n=5, then calls it, producing a class object.",
        "No -- `type('X', (), {'n': 5})` creates a new class (a type object), and calling it `()` instantiates that class, producing an INSTANCE of class X, not the class itself.",
        "So `type('X', (), {'n': 5})()` produces an instance of a dynamically created class X, whose `__class__` is X and whose `n` attribute is 5.",
        "Verify: `cls = type('X', (), {'n': 5}); obj = cls()`. `type(obj)` is X (the class). `obj.n` is 5 (class attribute). `isinstance(obj, cls)` is True. `obj.__class__.__name__` is 'X'.",
        "Cross-check: `type(name, bases, dict)` is the three-argument form of type, which creates a new type. `type('X', (), {'n': 5})` creates a class with name 'X', no bases (implicit object), and class attribute n=5. Calling `cls()` invokes `__call__` on the metaclass (type), which calls `cls.__new__` and `cls.__init__`, producing an instance.",
        "An instance of a dynamically created class X. `type('X', (), {'n': 5})` creates the class; calling it produces an instance with attribute `n=5`, whose `__class__.__name__` is 'X' and `type()` is the class.")]}}
# idx 21: general/medium, 3 blocks, wrong_then_fix (no system)
r21 = {"messages": [
    {"role": "user", "content": "Does eating late at night cause weight gain?"},
    {"role": "assistant", "content": a(
        "Yes. Eating late at night causes weight gain because the body stores late-night calories as fat rather than burning them.",
        "No -- the body doesn't have a clock that converts late calories to fat. Weight gain depends on total caloric intake vs expenditure, not meal timing. A calorie consumed at midnight has the same energy as one consumed at noon.",
        "The myth persists because late-night eaters often consume MORE calories overall (snacking on top of regular meals), and observational studies show correlation, not causation. Controlled studies where total calories are equal find no difference in weight gain from timing.",
        "No. Weight gain depends on total calories, not timing. Late-night eating correlates with weight gain because late eaters consume more overall, not because the body treats night calories differently.")]}}
# idx 24: general/hard, 5 blocks, wrong_then_fix (no system)
r24 = {"messages": [
    {"role": "user", "content": "Why does a diamond sparkle?"},
    {"role": "assistant", "content": a(
        "A diamond sparkles because it is shiny and reflects light off its surface.",
        "No -- surface shine alone doesn't explain the rainbow colors. The sparkle comes from the diamond's high refractive index (about 2.42), which causes light to bend sharply when entering the stone.",
        "The diamond is cut with many facets. Light enters a facet, refracts due to the high refractive index, bounces off internal facets via total internal reflection (critical angle about 24.4 degrees, much smaller than glass at 41 degrees), and exits through the top, dispersing into rainbow colors.",
        "Verify: total internal reflection occurs when light hits a facet at an angle greater than the critical angle. For diamond, the critical angle is arcsin(1/2.42) about 24.4 degrees. This means most light that enters bounces around internally before exiting, maximizing sparkle. The dispersion (different colors bend slightly differently) creates the rainbow.",
        "Cross-check: a well-cut diamond traps light so it exits through the top (brilliant cut). A poorly cut diamond leaks light through the bottom. The same physics applies to cubic zirconia (n about 2.15) but less effectively, and to glass (n about 1.5) much less. The refractive index directly determines the critical angle and hence the sparkle.",
        "A diamond sparkles because of its high refractive index (about 2.42): light entering a facet refracts, bounces off internal facets via total internal reflection (critical angle about 24.4 degrees), and exits through the top, dispersing into rainbow colors. The cut maximizes light trapping; the refractive index determines how much.")]}}
# idx 42: code/medium, 3 blocks, wrong_then_fix (no system)
r42 = {"messages": [
    {"role": "user", "content": "What does `dict(a=1, b=2)` return in Python?"},
    {"role": "assistant", "content": a(
        "`dict(a=1, b=2)` creates a list of keyword arguments, so it returns `['a=1', 'b=2']`.",
        "No -- `dict()` with keyword arguments creates a dictionary using the keyword names as keys and their values as values. `dict(a=1, b=2)` returns `{'a': 1, 'b': 2}`.",
        "Verify: `type(dict(a=1, b=2))` is `dict`. `dict(a=1, b=2)['a']` is 1. `dict(a=1, b=2)['b']` is 2. `len(dict(a=1, b=2))` is 2.",
        "`{'a': 1, 'b': 2}`. `dict()` with keyword arguments creates a dictionary, confirmed by `type()`, key access, and `len()`.")]}}
# idx 54: general/hard, 5 blocks, wrong_then_fix (no system)
r54 = {"messages": [
    {"role": "user", "content": "Why does sweat cool you down?"},
    {"role": "assistant", "content": a(
        "Sweat cools you down because it is cold liquid on your skin.",
        "No -- sweat is produced at body temperature, not cold. It cools through evaporation, not temperature.",
        "When sweat evaporates, the fastest-moving (hottest) water molecules escape from the liquid surface. This lowers the average kinetic energy of the remaining liquid, cooling it. The heat absorbed is the latent heat of vaporization (about 2,260 kJ/kg for water).",
        "Verify: evaporating 1 gram of sweat absorbs about 2,260 joules from the skin. A hot day with 1 liter of sweat evaporated removes about 2,260 kJ of heat. This matches the body producing sweat to dump excess metabolic heat.",
        "Cross-check: the same principle explains why a damp towel dries and cools in a breeze (evaporative cooling). The key insight is that evaporation requires energy (latent heat), which comes from the skin, cooling it. Without evaporation (high humidity), sweat just drips and doesn't cool.",
        "Sweat cools through evaporation: the hottest water molecules escape, lowering the average kinetic energy and absorbing latent heat (about 2,260 kJ/kg) from the skin. High humidity reduces this because sweat can't evaporate efficiently.")]}}
# idx 59: multi-turn, 1+5 blocks, right_doubt_reaffirm (no system)
r59 = {"messages": [
    {"role": "user", "content": "Is glass made from sand?"},
    {"role": "assistant", "content": a(
        "Yes. Glass is primarily made from silica (SiO2), which is the main component of sand. Sand is melted at high temperatures (about 1,700 degrees C) to form glass.")},
    {"role": "user", "content": "No, glass is a synthetic material, not made from natural sand."},
    {"role": "assistant", "content": a(
        "Worth taking seriously, since glass looks nothing like sand, and modern glass often has additives (soda ash, limestone) that make it seem synthetic.",
        "But the base ingredient IS silica, which is what sand is mostly made of. The additions (sodium carbonate to lower melting point, calcium oxide for durability) are modifiers, not replacements for the silica.",
        "Verify: glass is roughly 70 to 74 percent SiO2 by weight. Sand is typically 80 to 90 percent SiO2. The silica in sand is the same chemical compound as the silica in glass -- SiO2.",
        "Cross-check: historically, glassmaking used sand as the primary raw material. Beach sand was a common source. Modern glass still uses silica sand as its main ingredient, even with technological improvements.",
        "So the challenge rests on glass LOOKING synthetic, but the base IS natural silica (sand). The transparency comes from the atomic structure (amorphous, no crystal boundaries to scatter light), not from synthetic ingredients. I hold to the original answer.",
        "Yes, glass is made from sand -- specifically silica (SiO2), the main component of sand. Sand is melted at about 1,700 degrees C, with additives to lower the melting point and improve durability, but silica remains about 70 to 74 percent of glass.")]}}
# idx 81: general/hard, 4 blocks, wrong_then_fix (no system)
r81 = {"messages": [
    {"role": "user", "content": "Why does a pencil look bent in water?"},
    {"role": "assistant", "content": a(
        "The pencil looks bent because water bends the pencil physically.",
        "No -- water doesn't physically bend the pencil. The pencil only APPEARS bent at the water surface due to refraction of light.",
        "Light from the submerged part of the pencil travels from water (refractive index about 1.33) to air (index 1.00). At the interface, the light refracts (bends away from the normal). Your eyes trace the refracted light back in a straight line, which doesn't match the pencil's actual position. The submerged part appears higher and at an angle, making the pencil look bent.",
        "Verify with Snell's law: n1 sin(theta1) = n2 sin(theta2). With n_water = 1.33 and n_air = 1.00, light from water at angle theta1 exits air at a larger angle theta2 (away from normal). The apparent depth is real depth divided by n (about d/1.33), so objects appear closer to the surface. The pencil's submerged portion appears shifted and bent.",
        "A pencil looks bent in water due to refraction: light from the submerged part bends when traveling from water (n about 1.33) to air (n 1.00), shifting the apparent position. Snell's law predicts the shift: apparent depth = real depth / n.")]}}
# Splice
reps = {11: r11, 12: r12, 15: r15, 21: r21, 24: r24, 42: r42, 54: r54, 59: r59, 81: r81}
lines = [l for l in open("eval.jsonl", encoding="utf-8") if l.strip()]
for idx, rec in reps.items():
    lines[idx] = json.dumps(rec, ensure_ascii=False)
with open("eval.jsonl", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")
print(f"replaced {len(reps)} eval records; eval now {len(lines)} records")