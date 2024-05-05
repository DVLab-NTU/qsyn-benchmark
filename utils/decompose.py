from argparse import ArgumentParser, Namespace
from pathlib import Path
import re

def decomposeCRZ(w, ang, ctrl, targ):
    w.write(
        "p(pi/{ang}) q[{ctrl}];\n".format(ang=format(ang * 2, ".1E"), ctrl=ctrl))
    w.write(
        "p(pi/{ang}) q[{targ}];\n".format(ang=format(ang * 2, ".1E"), targ=targ))
    w.write("cx q[{ctrl}],q[{targ}];\n".format(ctrl=ctrl, targ=targ))
    w.write(
        "p(-pi/{ang}) q[{targ}];\n".format(ang=format(ang * 2, ".1E"), targ=targ))
    w.write("cx q[{ctrl}],q[{targ}];\n".format(ctrl=ctrl, targ=targ))


def HGate(w, qb, type):
    if type == "IBM":
        w.write("rz(pi/2) q[{}];\n".format(qb))
        w.write("sx q[{}];\n".format(qb))
        w.write("rz(pi/2) q[{}];\n".format(qb))
    else:
        w.write("h q[{}];\n".format(qb))


def CCXGate(w, qb, type):
    if type == "":
        w.write("ccx q[{c0}],q[{c1}],q[{t}];\n".format(
            c0=qb[0], c1=qb[1], t=qb[2]))
    else:
        HGate(w, qb[2], type)
        w.write("cx q[{c}],q[{t}];\n".format(c=qb[1], t=qb[2]))
        w.write("tdg q[{}];\n".format(qb[2]))
        w.write("cx q[{c}],q[{t}];\n".format(c=qb[0], t=qb[2]))
        w.write("t q[{}];\n".format(qb[2]))
        w.write("cx q[{c}],q[{t}];\n".format(c=qb[1], t=qb[2]))
        w.write("t q[{}];\n".format(qb[1]))
        w.write("tdg q[{}];\n".format(qb[2]))
        w.write("cx q[{c}],q[{t}];\n".format(c=qb[0], t=qb[2]))
        w.write("cx q[{c}],q[{t}];\n".format(c=qb[0], t=qb[1]))
        w.write("t q[{}];\n".format(qb[2]))
        w.write("t q[{}];\n".format(qb[0]))
        w.write("tdg q[{}];\n".format(qb[1]))
        HGate(w, qb[2], type)
        w.write("cx q[{c}],q[{t}];\n".format(c=qb[0], t=qb[1]))

def main(args):
    if args.type not in ["ibm", "clif-rz"]:
        print("Wrong type. Type should be either ibm or clif-rz (default)")
        exit()

    with open(
        "{root}/{name}_{type}.qasm".format(
            root=args.output_root, name=args.file.stem, type=args.type
        ),
        "w",
    ) as qasmf:
        qasmf.write('OPENQASM 2.0;\ninclude "qelib1.inc";\n')
        for line in open(args.file):
            if not len(line):
                continue
            type = line.split()[0]
            detail = line.split()[1]
            res = [int(val[1:-1]) for val in re.findall(r'\[.*?\]', detail)]
            if type == "qreg":
                qasmf.write("qreg q[{}];\n".format(res[0]))
            elif type == "h":
                HGate(qasmf, res[0], args.type)
            elif type == "ccx":
                CCXGate(qasmf, res, args.type)
            elif type == "cx":
                qasmf.write("cx q[{c}],q[{t}];\n".format(c=res[0], t=res[1]))


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--file", type=Path, help="Output file directory", required=True)
    parser.add_argument("--type", type=str,
                        help="Decomposition type",
                        default="clif-rz"
                        )
    parser.add_argument(
        "--output-root", type=Path, help="Output file directory", default="./"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
