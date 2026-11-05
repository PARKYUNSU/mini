"""pytorch_model.bin 의 pickle import 목록을 불러오지 않고 본다. 허용 밖이 있으면 exit 1. README §2.

  ~/dev/jeff_1105/venv/bin/python -I check_weights.py ~/dev/jeff_1105/models/gliformer-large-v1/pytorch_model.bin
"""
import collections, pickletools, sys, zipfile

STORAGES = ("Float", "Double", "Half", "BFloat16", "Long", "Int", "Short", "Char", "Byte", "Bool")
ALLOWED = {("collections", "OrderedDict"), ("torch._utils", "_rebuild_tensor_v2"), ("torch._utils", "_rebuild_parameter")}
ALLOWED |= {("torch", s + "Storage") for s in STORAGES}


def scan(data):
    found, bad = collections.Counter(), []
    for op, arg, _pos in pickletools.genops(data):
        if op.name == "GLOBAL":
            mod, name = arg.split(" ", 1)
            found[(mod, name)] += 1
        elif op.name in ("STACK_GLOBAL", "INST", "OBJ", "EXT1", "EXT2", "EXT4"):
            bad.append(op.name)
    return found, bad


def main():
    z = zipfile.ZipFile(sys.argv[1])
    names = z.namelist()
    pkls = [n for n in names if n.endswith(".pkl")]
    other = collections.Counter(n.split("/")[1] if "/" in n else n for n in names if not n.endswith(".pkl"))
    print("zip 항목", len(names), "· pkl", pkls, "· 그 밖", other.most_common(6))
    ok = bool(pkls)
    for n in pkls:
        found, bad = scan(z.read(n))
        print(n, "참조", sorted(found.items()), "· 판단 못 하는 opcode", bad)
        outside = [k for k in found if k not in ALLOWED]
        if outside or bad:
            print("허용 밖:", outside, bad)
            ok = False
    print("통과" if ok else "중단")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
